"""
Main entry point for the Maze Game with full UI integration
"""

import pygame
import sys
import config
from game import Game
from ui import Menu
from themes import get_theme


def main():
    """Main game loop"""
    # Initialize Pygame
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    clock = pygame.time.Clock()
    
    # Initialize game state
    current_theme = 'classic'
    current_difficulty = 'medium'
    current_visual_style = 'lines'
    game = None
    menu = Menu(get_theme(current_theme))
    state = 'menu'  # 'menu' or 'game'
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            
            elif state == 'menu':
                # Handle menu events
                action = menu.handle_event(event)
                
                if action == 'start':
                    # Start new game
                    try:
                        game = Game(menu.selected_difficulty, menu.selected_theme, menu.selected_visual_style)
                        current_difficulty = menu.selected_difficulty
                        current_theme = menu.selected_theme
                        current_visual_style = menu.selected_visual_style
                        state = 'game'
                    except Exception as e:
                        print(f"Error starting game: {e}")
                        import traceback
                        traceback.print_exc()
                        # Keep in menu state if game fails to start
                        state = 'menu'
                
                elif action == 'quit':
                    running = False
                
                elif action and action.startswith('difficulty_'):
                    # Difficulty already handled in menu
                    pass
                
                elif action and action.startswith('theme_'):
                    # Theme already handled in menu
                    theme_name = action.replace('theme_', '')
                    current_theme = theme_name
                    menu.update_theme(get_theme(theme_name))
                
                elif action and action.startswith('style_'):
                    # Visual style already handled in menu
                    pass
            
            elif state == 'game':
                # Handle game events
                if event.type == pygame.KEYDOWN:
                    action = game.handle_key(event.key)
                    
                    if action == 'restart':
                        game.reset(visual_style=current_visual_style)
                    elif action == 'menu':
                        state = 'menu'
                        menu.selected_difficulty = current_difficulty
                        menu.selected_theme = current_theme
                        menu.selected_visual_style = current_visual_style
                        menu.update_theme(get_theme(current_theme))
                
                elif event.type == pygame.KEYUP:
                    game.handle_key_up(event.key)
                
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                    action = game.handle_mouse(event)
                    
                    if action == 'restart':
                        game.reset(visual_style=current_visual_style)
                    elif action == 'menu':
                        state = 'menu'
                        menu.selected_difficulty = current_difficulty
                        menu.selected_theme = current_theme
                        menu.selected_visual_style = current_visual_style
                        menu.update_theme(get_theme(current_theme))
                    elif action == 'resume':
                        game.state = config.STATE_PLAYING
        
        # Update game
        if state == 'game' and game:
            game.update()
        
        # Draw everything
        if state == 'menu':
            menu.draw(screen)
        elif state == 'game' and game:
            game.draw(screen)
        
        pygame.display.flip()
        
        # Cap framerate
        clock.tick(60)
    
    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
