import pygame
from constants import *

class Tetrimino:
    def __init__(self, shape_type, x, y):
        self.shape_type = shape_type
        self.color = COLORS[shape_type]
        self.shapes = SHAPES[shape_type]
        self.rotation = 0
        self.x = x
        self.y = y
        self.appearance_timer = PIECE_APPEAR_ANIMATION_DURATION
        self.ghost_y = 0
        # Initialize ghost position without checking grid
        self.ghost_y = self.y
    
    def get_blocks(self):
        """Returns the current blocks positions"""
        return [(self.x + block[0], self.y + block[1]) for block in self.shapes[self.rotation]]
    
    def get_ghost_blocks(self):
        """Returns the ghost piece blocks positions"""
        return [(self.x + block[0], self.ghost_y + block[1]) for block in self.shapes[self.rotation]]
    
    def move(self, dx, dy, grid):
        """Try to move the tetrimino by dx, dy"""
        self.x += dx
        self.y += dy
        
        # Check if the move is valid
        if self.collision(grid):
            # If not, move back
            self.x -= dx
            self.y -= dy
            return False
        
        self.update_ghost_position(grid)
        return True
    
    def rotate(self, grid, clockwise=True):
        """Rotate the tetrimino with wall kick"""
        old_rotation = self.rotation
        
        # Calculate new rotation
        if clockwise:
            self.rotation = (self.rotation + 1) % 4
        else:
            self.rotation = (self.rotation - 1) % 4
        
        # Get wall kick data
        if self.shape_type == 'I':
            kick_data = WALL_KICK_I
        else:
            kick_data = WALL_KICK_DATA
        
        # Determine which transition we're making
        if clockwise:
            transition = f"{old_rotation}->{self.rotation}"
        else:
            transition = f"{self.rotation}->{old_rotation}"
            # Reverse the offsets for counter-clockwise rotation
            if transition in kick_data:
                kick_offsets = [(-x, -y) for x, y in kick_data[transition]]
            else:
                # Fallback if transition not found
                kick_offsets = [(0, 0)]
        
        # Try each wall kick offset
        if transition in kick_data:
            kick_offsets = kick_data[transition]
        else:
            kick_offsets = [(0, 0)]
        
        for offset_x, offset_y in kick_offsets:
            self.x += offset_x
            self.y += offset_y
            
            if not self.collision(grid):
                # Found a valid position
                self.update_ghost_position(grid)
                return True
            
            # Reset position and try next offset
            self.x -= offset_x
            self.y -= offset_y
        
        # If no valid position found, revert rotation
        self.rotation = old_rotation
        return False
    
    def collision(self, grid):
        """Check if the tetrimino collides with the grid or boundaries"""
        # If grid is empty or not initialized, only check boundaries
        if not grid:
            for x, y in self.get_blocks():
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                    return True
            return False
            
        for x, y in self.get_blocks():
            # Check boundaries
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return True
            
            # Check collision with placed blocks (only if block is in the grid)
            if y >= 0 and grid[y][x]:
                return True
        
        return False
    
    def update_ghost_position(self, grid):
        """Update the ghost piece position"""
        # If grid is empty or not initialized, don't update ghost position
        if not grid:
            self.ghost_y = self.y
            return
            
        self.ghost_y = self.y
        
        # Move ghost piece down until collision
        while True:
            self.ghost_y += 1
            ghost_blocks = self.get_ghost_blocks()
            
            # Check if any block is out of bounds or collides
            collision = False
            for x, y in ghost_blocks:
                if y >= GRID_HEIGHT or x < 0 or x >= GRID_WIDTH:
                    collision = True
                    break
                if y >= 0 and grid[y][x]:
                    collision = True
                    break
            
            if collision:
                self.ghost_y -= 1
                break
    
    def hard_drop(self, grid):
        """Drop the tetrimino to the lowest possible position"""
        drop_distance = 0
        while self.move(0, 1, grid):
            drop_distance += 1
        return drop_distance
    
    def draw(self, screen, offset_x, offset_y, cell_size):
        """Draw the tetrimino on the screen"""
        # Draw ghost piece first (semi-transparent)
        ghost_color = (*self.color, 80)  # Add alpha for transparency
        for x, y in self.get_ghost_blocks():
            if y >= 0:  # Only draw if block is in the visible grid
                ghost_rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, ghost_color, ghost_rect)
                pygame.draw.rect(screen, (*ghost_color[:3], 120), ghost_rect, 1)
        
        # Draw actual piece with appearance animation
        alpha = min(255, int(255 * (1 - self.appearance_timer / PIECE_APPEAR_ANIMATION_DURATION)))
        for x, y in self.get_blocks():
            if y >= 0:  # Only draw if block is in the visible grid
                block_rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size, cell_size
                )
                
                # Create a surface for the block with alpha
                block_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                pygame.draw.rect(block_surface, (*self.color, alpha), (0, 0, cell_size, cell_size))
                
                # Draw a slightly darker border
                darker_color = tuple(max(0, c - 40) for c in self.color)
                pygame.draw.rect(block_surface, (*darker_color, alpha), (0, 0, cell_size, cell_size), 1)
                
                # Add a highlight on top/left edges
                lighter_color = tuple(min(255, c + 40) for c in self.color)
                pygame.draw.line(block_surface, (*lighter_color, alpha), (1, 1), (cell_size - 2, 1))
                pygame.draw.line(block_surface, (*lighter_color, alpha), (1, 1), (1, cell_size - 2))
                
                screen.blit(block_surface, block_rect)
    
    def update(self, dt):
        """Update the tetrimino's appearance animation"""
        if self.appearance_timer > 0:
            self.appearance_timer = max(0, self.appearance_timer - dt)