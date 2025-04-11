import pygame
import sys
import os
from game import Game
from menu import Menu
from constants import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tetris")

# Load fonts
try:
    font_path = os.path.join('assets', 'fonts', 'Roboto-Regular.ttf')
    main_font = pygame.font.Font(font_path, 24)
    title_font = pygame.font.Font(font_path, 48)
except:
    main_font = pygame.font.SysFont('Arial', 24)
    title_font = pygame.font.SysFont('Arial', 48)

# Load sounds
try:
    place_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'place.wav'))
    line_clear_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'line_clear.wav'))
    game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game_over.wav'))
except:
    # Create silent sounds if files not found
    place_sound = pygame.mixer.Sound(buffer=bytearray(100))
    line_clear_sound = pygame.mixer.Sound(buffer=bytearray(100))
    game_over_sound = pygame.mixer.Sound(buffer=bytearray(100))

# Create game and menu instances
game = Game(screen, main_font, place_sound, line_clear_sound, game_over_sound)
menu = Menu(screen, title_font, main_font)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

current_state = MENU

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            game.resize(screen)
            menu.resize(screen)
        
        elif event.type == pygame.KEYDOWN:
            if current_state == MENU:
                if event.key == pygame.K_RETURN:
                    current_state = PLAYING
                    game.reset()
            
            elif current_state == PLAYING:
                if event.key == pygame.K_p:
                    current_state = PAUSED
                else:
                    game.handle_key_down(event.key)
            
            elif current_state == PAUSED:
                if event.key == pygame.K_p:
                    current_state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
            
            elif current_state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    current_state = PLAYING
                    game.reset()
                elif event.key == pygame.K_ESCAPE:
                    current_state = MENU
        
        elif event.type == pygame.KEYUP and current_state == PLAYING:
            game.handle_key_up(event.key)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == MENU:
            action = menu.handle_click(pygame.mouse.get_pos())
            if action == "play":
                current_state = PLAYING
                game.reset()
            elif action == "quit":
                running = False
    
    # Update and render based on current state
    screen.fill(BG_COLOR)
    
    if current_state == MENU:
        menu.update()
        menu.draw()
    
    elif current_state == PLAYING:
        game_over = game.update(dt)
        if game_over:
            current_state = GAME_OVER
            game_over_sound.play()
        game.draw()
    
    elif current_state == PAUSED:
        game.draw()
        # Draw pause overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        pause_text = title_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(pause_text, pause_rect)
        
        resume_text = main_font.render("Press P to resume or ESC for menu", True, WHITE)
        resume_rect = resume_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(resume_text, resume_rect)
    
    elif current_state == GAME_OVER:
        game.draw()
        # Draw game over overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        game_over_text = title_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(game_over_text, game_over_rect)
        
        score_text = main_font.render(f"Score: {game.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(score_text, score_rect)
        
        restart_text = main_font.render("Press ENTER to restart or ESC for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
        screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()

# Save high score before quitting
game.save_high_score()

# Clean up
pygame.quit()
sys.exit()