import pygame
import random
import os
from tetrimino import Tetrimino
from constants import *

class Game:
    def __init__(self, screen, font, place_sound, line_clear_sound, game_over_sound):
        self.screen = screen
        self.font = font
        self.place_sound = place_sound
        self.line_clear_sound = line_clear_sound
        self.game_over_sound = game_over_sound
        
        # Game state
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.zen_mode = False
        
        # Animation state
        self.clearing_lines = []
        self.clear_animation_timer = 0
        
        # Input handling
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_timer = 0
        self.fall_timer = 0
        self.fall_speed = INITIAL_FALL_SPEED
        
        # Initialize the bag of tetriminos for fair distribution
        self.tetrimino_bag = []
        self.refill_bag()
        
        # Calculate grid position
        self.resize(screen)
        
        # Create initial pieces
        self.spawn_piece()
        self.next_piece = self.get_next_tetrimino()
    
    def resize(self, screen):
        """Recalculate grid position when screen is resized"""
        self.screen = screen
        self.cell_size = min(
            (screen.get_width() - 300) // GRID_WIDTH,
            screen.get_height() // GRID_HEIGHT
        )
        self.cell_size = max(15, min(self.cell_size, 40))  # Constrain cell size
        
        # Center the grid horizontally
        self.grid_offset_x = (screen.get_width() - (GRID_WIDTH * self.cell_size + 200)) // 2
        
        # Center the grid vertically
        self.grid_offset_y = (screen.get_height() - GRID_HEIGHT * self.cell_size) // 2
    
    def refill_bag(self):
        """Refill the bag with one of each tetrimino and shuffle"""
        self.tetrimino_bag = list('IOTSZJL')
        random.shuffle(self.tetrimino_bag)
    
    def get_next_tetrimino(self):
        """Get the next tetrimino from the bag"""
        if not self.tetrimino_bag:
            self.refill_bag()
        
        shape_type = self.tetrimino_bag.pop()
        tetrimino = Tetrimino(shape_type, GRID_WIDTH // 2 - 1, 0)
        # Update ghost position with the current grid
        tetrimino.update_ghost_position(self.grid)
        return tetrimino
    
    def spawn_piece(self):
        """Spawn a new tetrimino at the top of the grid"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = self.get_next_tetrimino()
        
        self.next_piece = self.get_next_tetrimino()
        
        # Check if the new piece overlaps with existing blocks (game over)
        if self.current_piece.collision(self.grid) and not self.zen_mode:
            self.game_over = True
        
        # Update ghost position
        self.current_piece.update_ghost_position(self.grid)
    
    def place_piece(self):
        """Place the current piece on the grid"""
        for x, y in self.current_piece.get_blocks():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = self.current_piece.color
        
        self.place_sound.play()
        
        # Check for completed lines
        completed_lines = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                completed_lines.append(y)
        
        if completed_lines:
            self.clearing_lines = completed_lines
            self.clear_animation_timer = LINE_CLEAR_ANIMATION_DURATION
            self.line_clear_sound.play()
            
            # Update score based on number of lines cleared
            if len(completed_lines) == 1:
                self.score += SCORE_SINGLE * self.level
            elif len(completed_lines) == 2:
                self.score += SCORE_DOUBLE * self.level
            elif len(completed_lines) == 3:
                self.score += SCORE_TRIPLE * self.level
            elif len(completed_lines) == 4:
                self.score += SCORE_TETRIS * self.level
            
            # Update lines cleared and level
            self.lines_cleared += len(completed_lines)
            self.level = min(MAX_LEVEL, 1 + self.lines_cleared // LINES_PER_LEVEL)
            
            # Update fall speed based on level
            self.fall_speed = INITIAL_FALL_SPEED + (self.level - 1) * LEVEL_SPEED_FACTOR
        else:
            # No lines to clear, spawn next piece immediately
            self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines and move blocks down"""
        # Sort lines in descending order to avoid shifting issues
        self.clearing_lines.sort(reverse=True)
        
        for line in self.clearing_lines:
            # Remove the line
            self.grid.pop(line)
            # Add a new empty line at the top
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        self.clearing_lines = []
        self.spawn_piece()
    
    def handle_key_down(self, key):
        """Handle key press events"""
        if key == pygame.K_LEFT:
            self.move_left = True
            self.move_timer = 0
            self.current_piece.move(-1, 0, self.grid)
        
        elif key == pygame.K_RIGHT:
            self.move_right = True
            self.move_timer = 0
            self.current_piece.move(1, 0, self.grid)
        
        elif key == pygame.K_DOWN:
            self.move_down = True
        
        elif key == pygame.K_UP:
            self.current_piece.rotate(self.grid)
        
        elif key == pygame.K_SPACE:
            # Hard drop
            drop_distance = self.current_piece.hard_drop(self.grid)
            self.score += drop_distance * SCORE_HARD_DROP
            self.place_piece()
        
        elif key == pygame.K_z:
            # Counter-clockwise rotation
            self.current_piece.rotate(self.grid, clockwise=False)
    
    def handle_key_up(self, key):
        """Handle key release events"""
        if key == pygame.K_LEFT:
            self.move_left = False
        
        elif key == pygame.K_RIGHT:
            self.move_right = False
        
        elif key == pygame.K_DOWN:
            self.move_down = False
    
    def update(self, dt):
        """Update game state"""
        if self.game_over:
            return True
        
        # Update piece appearance animation
        if self.current_piece:
            self.current_piece.update(dt)
        
        # Handle line clearing animation
        if self.clearing_lines:
            self.clear_animation_timer -= dt
            if self.clear_animation_timer <= 0:
                self.clear_lines()
            return False
        
        # Handle continuous movement
        self.move_timer += dt * 1000  # Convert to milliseconds
        if self.move_timer >= KEY_REPEAT_INTERVAL:
            self.move_timer = 0
            if self.move_left:
                self.current_piece.move(-1, 0, self.grid)
            if self.move_right:
                self.current_piece.move(1, 0, self.grid)
        
        # Handle piece falling
        fall_speed = self.fall_speed
        if self.move_down:
            fall_speed *= SOFT_DROP_FACTOR
            if self.current_piece.move(0, 1, self.grid):
                self.score += SCORE_SOFT_DROP
        
        self.fall_timer += dt
        if self.fall_timer >= 1.0 / fall_speed:
            self.fall_timer = 0
            if not self.current_piece.move(0, 1, self.grid):
                self.place_piece()
        
        return False
    
    def draw(self):
        """Draw the game state"""
        # Draw background
        pygame.draw.rect(
            self.screen, 
            GRID_COLOR, 
            (
                self.grid_offset_x - 1, 
                self.grid_offset_y - 1, 
                GRID_WIDTH * self.cell_size + 2, 
                GRID_HEIGHT * self.cell_size + 2
            )
        )
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_rect = pygame.Rect(
                    self.grid_offset_x + x * self.cell_size,
                    self.grid_offset_y + y * self.cell_size,
                    self.cell_size, self.cell_size
                )
                
                # Draw placed blocks
                if self.grid[y][x]:
                    color = self.grid[y][x]
                    
                    # If this line is being cleared, animate it
                    if y in self.clearing_lines:
                        # Flash white and then fade out
                        progress = self.clear_animation_timer / LINE_CLEAR_ANIMATION_DURATION
                        if progress > 0.7:
                            # Flash white
                            flash_intensity = (progress - 0.7) / 0.3
                            color = tuple(int(c + (255 - c) * flash_intensity) for c in color)
                        else:
                            # Fade out
                            alpha = int(255 * progress / 0.7)
                            pygame.draw.rect(self.screen, (*color, alpha), cell_rect)
                            continue
                    
                    pygame.draw.rect(self.screen, color, cell_rect)
                    
                    # Draw a slightly darker border
                    darker_color = tuple(max(0, c - 40) for c in color)
                    pygame.draw.rect(self.screen, darker_color, cell_rect, 1)
                    
                    # Add a highlight on top/left edges
                    lighter_color = tuple(min(255, c + 40) for c in color)
                    pygame.draw.line(self.screen, lighter_color, 
                                    (cell_rect.left + 1, cell_rect.top + 1), 
                                    (cell_rect.right - 2, cell_rect.top + 1))
                    pygame.draw.line(self.screen, lighter_color, 
                                    (cell_rect.left + 1, cell_rect.top + 1), 
                                    (cell_rect.left + 1, cell_rect.bottom - 2))
                else:
                    # Draw empty cell
                    pygame.draw.rect(self.screen, BG_COLOR, cell_rect)
                    pygame.draw.rect(self.screen, GRID_COLOR, cell_rect, 1)
        
        # Draw current piece
        if self.current_piece and not self.clearing_lines:
            self.current_piece.draw(
                self.screen, 
                self.grid_offset_x, 
                self.grid_offset_y, 
                self.cell_size
            )
        
        # Draw sidebar
        sidebar_x = self.grid_offset_x + GRID_WIDTH * self.cell_size + 20
        sidebar_width = 180
        
        # Draw next piece preview
        next_piece_text = self.font.render("NEXT", True, WHITE)
        self.screen.blit(next_piece_text, (sidebar_x, self.grid_offset_y))
        
        preview_size = self.cell_size * 4
        preview_rect = pygame.Rect(
            sidebar_x, 
            self.grid_offset_y + 40, 
            preview_size, 
            preview_size
        )
        pygame.draw.rect(self.screen, GRID_COLOR, preview_rect)
        
        # Draw next piece in preview
        if self.next_piece:
            # Calculate offset to center the piece in the preview
            piece_width = max(x for x, _ in self.next_piece.shapes[0]) - min(x for x, _ in self.next_piece.shapes[0]) + 1
            piece_height = max(y for _, y in self.next_piece.shapes[0]) - min(y for _, y in self.next_piece.shapes[0]) + 1
            
            offset_x = sidebar_x + (preview_size - piece_width * self.cell_size) // 2
            offset_y = self.grid_offset_y + 40 + (preview_size - piece_height * self.cell_size) // 2
            
            # Adjust for I and O pieces which have special centering needs
            if self.next_piece.shape_type == 'I':
                offset_y += self.cell_size // 2
            elif self.next_piece.shape_type == 'O':
                offset_x -= self.cell_size // 2
            
            for x, y in self.next_piece.shapes[0]:
                block_rect = pygame.Rect(
                    offset_x + x * self.cell_size,
                    offset_y + y * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(self.screen, self.next_piece.color, block_rect)
                
                # Draw a slightly darker border
                darker_color = tuple(max(0, c - 40) for c in self.next_piece.color)
                pygame.draw.rect(self.screen, darker_color, block_rect, 1)
                
                # Add a highlight on top/left edges
                lighter_color = tuple(min(255, c + 40) for c in self.next_piece.color)
                pygame.draw.line(self.screen, lighter_color, 
                                (block_rect.left + 1, block_rect.top + 1), 
                                (block_rect.right - 2, block_rect.top + 1))
                pygame.draw.line(self.screen, lighter_color, 
                                (block_rect.left + 1, block_rect.top + 1), 
                                (block_rect.left + 1, block_rect.bottom - 2))
        
        # Draw score
        score_y = self.grid_offset_y + 160
        score_text = self.font.render("SCORE", True, WHITE)
        self.screen.blit(score_text, (sidebar_x, score_y))
        
        score_value = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(score_value, (sidebar_x, score_y + 30))
        
        # Draw high score
        high_score_y = score_y + 80
        high_score_text = self.font.render("HIGH SCORE", True, WHITE)
        self.screen.blit(high_score_text, (sidebar_x, high_score_y))
        
        high_score_value = self.font.render(str(max(self.high_score, self.score)), True, WHITE)
        self.screen.blit(high_score_value, (sidebar_x, high_score_y + 30))
        
        # Draw level
        level_y = high_score_y + 80
        level_text = self.font.render("LEVEL", True, WHITE)
        self.screen.blit(level_text, (sidebar_x, level_y))
        
        level_value = self.font.render(str(self.level), True, WHITE)
        self.screen.blit(level_value, (sidebar_x, level_y + 30))
        
        # Draw lines
        lines_y = level_y + 80
        lines_text = self.font.render("LINES", True, WHITE)
        self.screen.blit(lines_text, (sidebar_x, lines_y))
        
        lines_value = self.font.render(str(self.lines_cleared), True, WHITE)
        self.screen.blit(lines_value, (sidebar_x, lines_y + 30))
        
        # Draw controls help
        controls_y = lines_y + 80
        controls_text = self.font.render("CONTROLS", True, WHITE)
        self.screen.blit(controls_text, (sidebar_x, controls_y))
        
        controls = [
            "← → : Move",
            "↓ : Soft Drop",
            "↑ : Rotate",
            "Z : Rotate CCW",
            "SPACE : Hard Drop",
            "P : Pause"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, GRAY)
            self.screen.blit(control_text, (sidebar_x, controls_y + 30 + i * 25))
    
    def reset(self):
        """Reset the game state"""
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.clearing_lines = []
        self.clear_animation_timer = 0
        self.move_left = False
        self.move_right = False
        self.move_down = False
        self.move_timer = 0
        self.fall_timer = 0
        self.fall_speed = INITIAL_FALL_SPEED
        
        # Refill the bag and spawn new pieces
        self.tetrimino_bag = []
        self.refill_bag()
        self.spawn_piece()
        self.next_piece = self.get_next_tetrimino()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        if self.score > self.high_score:
            try:
                with open(HIGH_SCORE_FILE, 'w') as f:
                    f.write(str(self.score))
            except:
                pass