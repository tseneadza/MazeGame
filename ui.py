"""
UI components: Menu, HUD, Win Screen, Pause Menu
"""

import pygame
import config
from themes import get_theme


class Button:
    """Simple button class for UI"""
    
    def __init__(self, x, y, width, height, text, theme, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.theme = theme
        self.action = action
        self.hovered = False
        
    def draw(self, screen, font):
        """Draw button"""
        color = self.theme['button_hover'] if self.hovered else self.theme['button']
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.theme['text'], self.rect, 2)
        
        text_surface = font.render(self.text, True, self.theme['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        """Check if mouse is hovering over button"""
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos):
        """Check if button was clicked"""
        if self.rect.collidepoint(pos) and self.action:
            return self.action
        return None


class Menu:
    """Main menu screen"""
    
    def __init__(self, theme):
        self.theme = theme
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.selected_difficulty = 'medium'
        self.selected_theme = 'classic'
        self.selected_visual_style = 'blocks'  # 'blocks' or 'lines'
        
        # Create buttons
        button_width = 250
        button_height = 50
        center_x = config.WINDOW_WIDTH // 2
        start_y = 250
        
        self.start_button = Button(
            center_x - button_width // 2,
            start_y,
            button_width,
            button_height,
            "Start Game",
            theme,
            'start'
        )
        
        self.difficulty_buttons = {
            'easy': Button(center_x - 150, start_y + 80, 100, 40, "Easy", theme, 'difficulty_easy'),
            'medium': Button(center_x - 50, start_y + 80, 100, 40, "Medium", theme, 'difficulty_medium'),
            'hard': Button(center_x + 50, start_y + 80, 100, 40, "Hard", theme, 'difficulty_hard'),
        }
        
        self.theme_buttons = {}
        theme_names = ['classic', 'dark', 'colorful', 'neon']
        for i, theme_name in enumerate(theme_names):
            self.theme_buttons[theme_name] = Button(
                center_x - 200 + i * 100,
                start_y + 140,
                90,
                35,
                theme_name.capitalize(),
                theme,
                f'theme_{theme_name}'
            )
        
        # Visual style buttons
        self.visual_style_buttons = {
            'blocks': Button(center_x - 100, start_y + 190, 90, 35, "Blocks", theme, 'style_blocks'),
            'lines': Button(center_x + 10, start_y + 190, 90, 35, "Lines", theme, 'style_lines'),
        }
        
        self.quit_button = Button(
            center_x - button_width // 2,
            start_y + 250,
            button_width,
            button_height,
            "Quit",
            theme,
            'quit'
        )
    
    def draw(self, screen):
        """Draw menu"""
        screen.fill(self.theme['menu_bg'])
        
        # Title
        title = self.font_large.render("MAZE GAME", True, self.theme['text'])
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("Navigate to the exit!", True, self.theme['text_secondary'])
        subtitle_rect = subtitle.get_rect(center=(config.WINDOW_WIDTH // 2, 150))
        screen.blit(subtitle, subtitle_rect)
        
        # Draw buttons
        self.start_button.draw(screen, self.font_medium)
        self.quit_button.draw(screen, self.font_medium)
        
        # Difficulty label
        start_y = 250
        diff_label = self.font_small.render("Difficulty:", True, self.theme['text_secondary'])
        screen.blit(diff_label, (config.WINDOW_WIDTH // 2 - 150, start_y + 60))
        
        for name, button in self.difficulty_buttons.items():
            # Draw button first
            button.draw(screen, self.font_small)
            # Then highlight selected
            if name == self.selected_difficulty:
                highlight_rect = pygame.Rect(button.rect.x - 3, button.rect.y - 3, 
                                           button.rect.width + 6, button.rect.height + 6)
                pygame.draw.rect(screen, self.theme['exit'], highlight_rect, 5)
                inner_rect = pygame.Rect(button.rect.x - 1, button.rect.y - 1, 
                                        button.rect.width + 2, button.rect.height + 2)
                highlight_color = tuple(min(255, c + 50) for c in self.theme['exit'])
                pygame.draw.rect(screen, highlight_color, inner_rect, 2)
        
        # Theme label
        theme_label = self.font_small.render("Theme:", True, self.theme['text_secondary'])
        screen.blit(theme_label, (config.WINDOW_WIDTH // 2 - 200, start_y + 120))
        
        for name, button in self.theme_buttons.items():
            # Draw button first
            button.draw(screen, self.font_small)
            # Then highlight selected
            if name == self.selected_theme:
                highlight_rect = pygame.Rect(button.rect.x - 3, button.rect.y - 3, 
                                           button.rect.width + 6, button.rect.height + 6)
                pygame.draw.rect(screen, self.theme['exit'], highlight_rect, 5)
                inner_rect = pygame.Rect(button.rect.x - 1, button.rect.y - 1, 
                                        button.rect.width + 2, button.rect.height + 2)
                highlight_color = tuple(min(255, c + 50) for c in self.theme['exit'])
                pygame.draw.rect(screen, highlight_color, inner_rect, 2)
        
        # Visual style label
        style_label = self.font_small.render("Style:", True, self.theme['text_secondary'])
        screen.blit(style_label, (config.WINDOW_WIDTH // 2 - 100, start_y + 170))
        
        for name, button in self.visual_style_buttons.items():
            # Draw button first
            button.draw(screen, self.font_small)
            # Then highlight selected with a more visible border
            if name == self.selected_visual_style:
                highlight_rect = pygame.Rect(button.rect.x - 3, button.rect.y - 3, 
                                           button.rect.width + 6, button.rect.height + 6)
                # Draw a bright highlight border
                pygame.draw.rect(screen, self.theme['exit'], highlight_rect, 5)
                # Also draw inner highlight for extra visibility
                inner_rect = pygame.Rect(button.rect.x - 1, button.rect.y - 1, 
                                        button.rect.width + 2, button.rect.height + 2)
                highlight_color = tuple(min(255, c + 50) for c in self.theme['exit'])
                pygame.draw.rect(screen, highlight_color, inner_rect, 2)
        
        self.quit_button.draw(screen, self.font_medium)
    
    def handle_event(self, event):
        """Handle menu events"""
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.start_button.check_hover(pos)
            for button in self.difficulty_buttons.values():
                button.check_hover(pos)
            for button in self.theme_buttons.values():
                button.check_hover(pos)
            for button in self.visual_style_buttons.values():
                button.check_hover(pos)
            self.quit_button.check_hover(pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            button_num = event.button if hasattr(event, 'button') else 1
            
            # Only handle left mouse button (button 1)
            if button_num != 1:
                return None
            
            # Check start button FIRST (highest priority)
            if self.start_button.rect.collidepoint(pos) and self.start_button.action:
                return self.start_button.action
            
            # Check quit button (high priority)
            if self.quit_button.rect.collidepoint(pos) and self.quit_button.action:
                return self.quit_button.action
            
            # Check visual style buttons
            for name, button in self.visual_style_buttons.items():
                if button.rect.collidepoint(pos):
                    self.selected_visual_style = name
                    print(f"Visual style changed to: {name}")
                    return None  # Update selection, don't start game
            
            # Check difficulty buttons
            for name, button in self.difficulty_buttons.items():
                if button.rect.collidepoint(pos):
                    self.selected_difficulty = name
                    print(f"Difficulty changed to: {name}")
                    return None
            
            # Check theme buttons
            for name, button in self.theme_buttons.items():
                if button.rect.collidepoint(pos):
                    self.selected_theme = name
                    print(f"Theme changed to: {name}")
                    return None
        
        return None
    
    def update_theme(self, theme):
        """Update theme for all buttons"""
        self.theme = theme
        self.start_button.theme = theme
        self.quit_button.theme = theme
        for button in self.difficulty_buttons.values():
            button.theme = theme
        for button in self.theme_buttons.values():
            button.theme = theme
        for button in self.visual_style_buttons.values():
            button.theme = theme


class HUD:
    """Heads-up display showing game stats"""
    
    def __init__(self, theme):
        self.theme = theme
        self.font = pygame.font.Font(None, 24)
        self.start_time = None
        self.move_count = 0
    
    def start(self):
        """Start timer"""
        import time
        self.start_time = time.time()
        self.move_count = 0
    
    def increment_move(self):
        """Increment move counter"""
        self.move_count += 1
    
    def get_time(self):
        """Get elapsed time in seconds"""
        if self.start_time is None:
            return 0
        import time
        return int(time.time() - self.start_time)
    
    def format_time(self, seconds):
        """Format time as MM:SS"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def draw(self, screen):
        """Draw HUD"""
        if self.start_time is None:
            return
        
        # Background bar
        bar_rect = pygame.Rect(10, 10, config.WINDOW_WIDTH - 20, 40)
        pygame.draw.rect(screen, (0, 0, 0, 180), bar_rect)
        pygame.draw.rect(screen, self.theme['text'], bar_rect, 2)
        
        # Time
        time_text = self.font.render(f"Time: {self.format_time(self.get_time())}", True, self.theme['text'])
        screen.blit(time_text, (20, 18))
        
        # Moves
        moves_text = self.font.render(f"Moves: {self.move_count}", True, self.theme['text'])
        moves_rect = moves_text.get_rect()
        moves_rect.topleft = (config.WINDOW_WIDTH - moves_rect.width - 20, 18)
        screen.blit(moves_text, moves_rect)
    
    def reset(self):
        """Reset HUD stats"""
        self.start_time = None
        self.move_count = 0


class WinScreen:
    """Win screen showing completion stats"""
    
    def __init__(self, theme):
        self.theme = theme
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.time = 0
        self.moves = 0
        
        # Buttons
        button_width = 200
        button_height = 45
        center_x = config.WINDOW_WIDTH // 2
        
        self.restart_button = Button(
            center_x - button_width // 2,
            400,
            button_width,
            button_height,
            "Play Again",
            theme,
            'restart'
        )
        
        self.menu_button = Button(
            center_x - button_width // 2,
            460,
            button_width,
            button_height,
            "Main Menu",
            theme,
            'menu'
        )
    
    def set_stats(self, time, moves):
        """Set completion stats"""
        self.time = time
        self.moves = moves
    
    def draw(self, screen):
        """Draw win screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Win message
        win_text = self.font_large.render("YOU WON!", True, self.theme['exit'])
        win_rect = win_text.get_rect(center=(config.WINDOW_WIDTH // 2, 200))
        screen.blit(win_text, win_rect)
        
        # Stats
        hud = HUD(self.theme)
        time_text = self.font_medium.render(f"Time: {hud.format_time(self.time)}", True, self.theme['text'])
        time_rect = time_text.get_rect(center=(config.WINDOW_WIDTH // 2, 280))
        screen.blit(time_text, time_rect)
        
        moves_text = self.font_medium.render(f"Moves: {self.moves}", True, self.theme['text'])
        moves_rect = moves_text.get_rect(center=(config.WINDOW_WIDTH // 2, 320))
        screen.blit(moves_text, moves_rect)
        
        # Buttons
        self.restart_button.draw(screen, self.font_small)
        self.menu_button.draw(screen, self.font_small)
    
    def handle_event(self, event):
        """Handle win screen events"""
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.restart_button.check_hover(pos)
            self.menu_button.check_hover(pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            action = self.restart_button.check_click(pos)
            if action:
                return action
            
            action = self.menu_button.check_click(pos)
            if action:
                return action
        
        return None
    
    def update_theme(self, theme):
        """Update theme"""
        self.theme = theme
        self.restart_button.theme = theme
        self.menu_button.theme = theme


class PauseMenu:
    """Pause menu overlay"""
    
    def __init__(self, theme):
        self.theme = theme
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        
        # Buttons
        button_width = 200
        button_height = 45
        center_x = config.WINDOW_WIDTH // 2
        
        self.resume_button = Button(
            center_x - button_width // 2,
            250,
            button_width,
            button_height,
            "Resume",
            theme,
            'resume'
        )
        
        self.menu_button = Button(
            center_x - button_width // 2,
            310,
            button_width,
            button_height,
            "Main Menu",
            theme,
            'menu'
        )
    
    def draw(self, screen):
        """Draw pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, self.theme['text'])
        pause_rect = pause_text.get_rect(center=(config.WINDOW_WIDTH // 2, 180))
        screen.blit(pause_text, pause_rect)
        
        # Buttons
        self.resume_button.draw(screen, self.font_medium)
        self.menu_button.draw(screen, self.font_medium)
    
    def handle_event(self, event):
        """Handle pause menu events"""
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self.resume_button.check_hover(pos)
            self.menu_button.check_hover(pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            action = self.resume_button.check_click(pos)
            if action:
                return action
            
            action = self.menu_button.check_click(pos)
            if action:
                return action
        
        return None
    
    def update_theme(self, theme):
        """Update theme"""
        self.theme = theme
        self.resume_button.theme = theme
        self.menu_button.theme = theme
