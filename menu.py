import pygame
import math  # Import the standard math module
from constants import *

class Menu:
    def __init__(self, screen, title_font, button_font):
        self.screen = screen
        self.title_font = title_font
        self.button_font = button_font
        self.buttons = []
        self.resize(screen)
        self.animation_time = 0
    
    def resize(self, screen):
        """Recalculate button positions when screen is resized"""
        self.screen = screen
        width, height = screen.get_width(), screen.get_height()
        
        # Create buttons
        button_width = 200
        button_height = 60
        button_spacing = 20
        
        # Center buttons horizontally
        button_x = (width - button_width) // 2
        
        # Position buttons vertically
        start_y = height // 2
        
        self.buttons = [
            {
                'rect': pygame.Rect(button_x, start_y, button_width, button_height),
                'text': 'PLAY',
                'action': 'play',
                'hover': False
            },
            {
                'rect': pygame.Rect(button_x, start_y + button_height + button_spacing, button_width, button_height),
                'text': 'QUIT',
                'action': 'quit',
                'hover': False
            }
        ]
    
    def update(self):
        """Update menu state"""
        self.animation_time += 0.016  # Approximately 60 FPS
        
        # Update button hover state
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button['hover'] = button['rect'].collidepoint(mouse_pos)
    
    def handle_click(self, pos):
        """Handle mouse click"""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None
    
    def draw(self):
        """Draw the menu"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        # Draw title with animation
        title_text = self.title_font.render("TETRIS", True, WHITE)
        title_rect = title_text.get_rect(center=(width // 2, height // 3))
        
        # Add a subtle floating animation to the title - using standard math.sin
        title_offset = int(5 * (1 + math.sin(self.animation_time * 2)))
        title_rect.y -= title_offset
        
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.button_font.render("PYTHON EDITION", True, GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, height // 3 + 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            # Draw button background with hover effect
            if button['hover']:
                color = (60, 60, 80)
                border_color = WHITE
            else:
                color = (40, 40, 60)
                border_color = GRAY
            
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, border_color, button['rect'], 2, border_radius=5)
            
            # Draw button text
            text = self.button_font.render(button['text'], True, WHITE)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
        
        # Draw tetrimino decorations
        self.draw_decorations()
    
    def draw_decorations(self):
        """Draw tetrimino decorations around the menu"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        # Define some tetrimino shapes to draw as decorations
        decorations = [
            # L shape
            {'shape': [(0, 0), (0, 1), (0, 2), (1, 2)], 'color': COLORS['L'], 'pos': (width // 4, height // 5), 'rotation': 0},
            # T shape
            {'shape': [(0, 0), (-1, 0), (1, 0), (0, 1)], 'color': COLORS['T'], 'pos': (width * 3 // 4, height // 5), 'rotation': 0},
            # I shape
            {'shape': [(0, 0), (1, 0), (2, 0), (3, 0)], 'color': COLORS['I'], 'pos': (width // 5, height * 4 // 5), 'rotation': 0},
            # Z shape
            {'shape': [(0, 0), (1, 0), (1, 1), (2, 1)], 'color': COLORS['Z'], 'pos': (width * 4 // 5, height * 4 // 5), 'rotation': 0}
        ]
        
        cell_size = 20
        
        for decoration in decorations:
            # Add animation to rotate the pieces slowly
            rotation_speed = 0.2
            decoration['rotation'] = (decoration['rotation'] + rotation_speed) % 360
            angle = decoration['rotation']
            
            # Draw each block of the tetrimino
            for x, y in decoration['shape']:
                # Apply rotation - using standard math functions
                cos_a = math.cos(math.radians(angle))
                sin_a = math.sin(math.radians(angle))
                rot_x = x * cos_a - y * sin_a
                rot_y = x * sin_a + y * cos_a
                
                # Calculate position
                pos_x = decoration['pos'][0] + rot_x * cell_size
                pos_y = decoration['pos'][1] + rot_y * cell_size
                
                # Draw block
                block_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)
                pygame.draw.rect(self.screen, decoration['color'], block_rect)
                
                # Draw a slightly darker border
                darker_color = tuple(max(0, c - 40) for c in decoration['color'])
                pygame.draw.rect(self.screen, darker_color, block_rect, 1)