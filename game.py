"""
Core game loop and state management with UI integration
"""

import pygame
import config
from maze_generator import Maze
from player import Player
from ui import HUD, WinScreen, PauseMenu
from themes import get_theme
from powerups import PowerUpManager
from enemies import EnemyManager
from audio import audio_manager


class Game:
    """Main game class managing game state and loop"""
    
    def __init__(self, difficulty='medium', theme_name='classic', visual_style='lines'):
        self.difficulty = difficulty
        self.theme = get_theme(theme_name)
        self.difficulty_config = config.DIFFICULTIES[difficulty]
        self.visual_style = visual_style  # Now always 'lines' (tutorial design)
        
        # Initialize maze with difficulty settings
        self.maze = Maze(
            self.difficulty_config['width'],
            self.difficulty_config['height']
        )
        self.maze.generate()
        
        # Initialize player at entry position (pixel coordinates)
        tile = self.difficulty_config['cell_size']
        entry_x = self.maze.entry.x * tile + tile // 3
        entry_y = self.maze.entry.y * tile + tile // 3
        self.player = Player(entry_x, entry_y)
        
        # Mouse navigation
        self.mouse_navigation_enabled = True
        self.last_mouse_pos = None
        
        # Game state
        self.state = config.STATE_PLAYING
        self.won = False
        
        # UI components
        self.hud = HUD(self.theme)
        self.win_screen = WinScreen(self.theme)
        self.pause_menu = PauseMenu(self.theme)
        
        # Power-ups and enemies (enemies disabled by default for less frustration)
        self.powerup_manager = PowerUpManager(self.maze, self.theme, difficulty)
        self.enemy_manager = EnemyManager(self.maze, self.theme, difficulty)
        self.enable_powerups = True
        self.enable_enemies = False  # Disabled by default - can enable in menu later
        
        # Start HUD timer
        self.hud.start()
        
    def reset(self, difficulty=None, theme_name=None, visual_style=None):
        """Reset game to initial state"""
        if difficulty:
            self.difficulty = difficulty
            self.difficulty_config = config.DIFFICULTIES[difficulty]
        
        if theme_name:
            self.theme = get_theme(theme_name)
            self.hud.theme = self.theme
        
        if visual_style:
            self.visual_style = visual_style
            self.win_screen.update_theme(self.theme)
            self.pause_menu.update_theme(self.theme)
        
        # Regenerate maze
        self.maze = Maze(
            self.difficulty_config['width'],
            self.difficulty_config['height']
        )
        self.maze.generate()
        
        # Reset player at entry position (pixel coordinates)
        tile = self.difficulty_config['cell_size']
        entry_x = self.maze.entry.x * tile + tile // 3
        entry_y = self.maze.entry.y * tile + tile // 3
        self.player.set_position(entry_x, entry_y)
        
        # Reset mouse navigation
        self.last_mouse_pos = None
        
        # Reset state
        self.won = False
        self.state = config.STATE_PLAYING
        
        # Reset HUD
        self.hud.reset()
        self.hud.start()
        
        # Reset power-ups and enemies
        if self.enable_powerups:
            self.powerup_manager = PowerUpManager(self.maze, self.theme, self.difficulty)
        if self.enable_enemies:
            self.enemy_manager = EnemyManager(self.maze, self.theme, self.difficulty)
        # Note: Enemies are disabled by default - they reset you to start on collision
    
    def update(self):
        """Update game state"""
        if self.state != config.STATE_PLAYING:
            return
        
        # Update player movement (pixel-based)
        tile = self.difficulty_config['cell_size']
        self.player.check_move(tile, self.maze.grid_cells, self.maze.thickness, 
                              self.maze.width, self.maze.height)
        self.player.update()
        
        # Track movement for HUD
        if self.player.velX != 0 or self.player.velY != 0:
            self.hud.increment_move()
            audio_manager.play_sound('move', 0.1)
        
        # Update enemies
        if self.enable_enemies:
            self.enemy_manager.update()
        
        # Update power-ups
        if self.enable_powerups:
            self.powerup_manager.update()
            # Apply time bonus if any
            time_bonus = self.powerup_manager.get_time_bonus()
            if time_bonus > 0:
                # Add time bonus (subtract from elapsed time)
                import time
                if self.hud.start_time:
                    self.hud.start_time -= time_bonus
        
        # Check enemy collision (only if enemies are enabled)
        if self.enable_enemies:
            player_pos = self.player.get_position()
            # Convert player pixel position to cell coordinates for collision check
            player_cell_x = int(player_pos[0] // tile)
            player_cell_y = int(player_pos[1] // tile)
            if self.enemy_manager.check_collisions(player_cell_x, player_cell_y):
                # Reset to entry on collision with enemy
                entry_x = self.maze.entry.x * tile + tile // 3
                entry_y = self.maze.entry.y * tile + tile // 3
                self.player.set_position(entry_x, entry_y)
                audio_manager.play_sound('hit', 0.6)
                return
        
        # Check power-up collection (convert pixel coords to cell coords)
        if self.enable_powerups:
            player_pos = self.player.get_position()
            player_cell_x = int(player_pos[0] // tile)
            player_cell_y = int(player_pos[1] // tile)
            powerup_type = self.powerup_manager.check_collections(player_cell_x, player_cell_y)
            if powerup_type:
                audio_manager.play_sound('powerup', 0.5)
        
        # Check win condition - check if player reached exit cell
        player_pos = self.player.get_position()
        exit_cell_x = self.maze.exit.x * tile
        exit_cell_y = self.maze.exit.y * tile
        if (exit_cell_x <= player_pos[0] < exit_cell_x + tile and 
            exit_cell_y <= player_pos[1] < exit_cell_y + tile):
            self.won = True
            self.state = config.STATE_WON
            # Set win screen stats
            self.win_screen.set_stats(self.hud.get_time(), self.hud.move_count)
            # Play win sound
            audio_manager.play_sound('win', 0.7)
    
    def handle_key(self, key):
        """Handle keyboard input"""
        if self.state == config.STATE_PLAYING:
            if key == pygame.K_LEFT or key == pygame.K_a:
                self.player.left_pressed = True
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                self.player.right_pressed = True
            elif key == pygame.K_UP or key == pygame.K_w:
                self.player.up_pressed = True
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.player.down_pressed = True
            elif key == pygame.K_p or key == pygame.K_ESCAPE:
                self.state = config.STATE_PAUSED
            
            # Check movement against walls
            tile = self.difficulty_config['cell_size']
            self.player.check_move(tile, self.maze.grid_cells, self.maze.thickness, 
                                  self.maze.width, self.maze.height)
        
        elif self.state == config.STATE_PAUSED:
            if key == pygame.K_p or key == pygame.K_ESCAPE:
                self.state = config.STATE_PLAYING
        
        elif self.state == config.STATE_WON:
            if key == pygame.K_r:
                return 'restart'
            elif key == pygame.K_m:
                return 'menu'
    
    def handle_key_up(self, key):
        """Handle key release events"""
        if self.state == config.STATE_PLAYING:
            if key == pygame.K_LEFT or key == pygame.K_a:
                self.player.left_pressed = False
            elif key == pygame.K_RIGHT or key == pygame.K_d:
                self.player.right_pressed = False
            elif key == pygame.K_UP or key == pygame.K_w:
                self.player.up_pressed = False
            elif key == pygame.K_DOWN or key == pygame.K_s:
                self.player.down_pressed = False
            
            # Check movement against walls
            tile = self.difficulty_config['cell_size']
            self.player.check_move(tile, self.maze.grid_cells, self.maze.thickness, 
                                  self.maze.width, self.maze.height)
    
    def handle_mouse(self, event):
        """Handle mouse events for UI and navigation"""
        if self.state == config.STATE_PLAYING and self.mouse_navigation_enabled:
            if event.type == pygame.MOUSEMOTION:
                self._handle_mouse_navigation(event.pos)
        
        if self.state == config.STATE_WON:
            action = self.win_screen.handle_event(event)
            return action
        elif self.state == config.STATE_PAUSED:
            action = self.pause_menu.handle_event(event)
            return action
        return None
    
    def _handle_mouse_navigation(self, mouse_pos):
        """Handle mouse/trackpad navigation - move player toward mouse position"""
        if self.last_mouse_pos is None:
            self.last_mouse_pos = mouse_pos
            return
        
        tile = self.difficulty_config['cell_size']
        maze_pixel_width = self.maze.width * tile
        maze_pixel_height = self.maze.height * tile
        
        # Calculate offset to center maze
        offset_x = (config.WINDOW_WIDTH - maze_pixel_width) // 2
        offset_y = (config.WINDOW_HEIGHT - maze_pixel_height) // 2
        
        # Convert mouse position to pixel coordinates relative to maze
        mouse_x = mouse_pos[0] - offset_x
        mouse_y = mouse_pos[1] - offset_y
        
        # Get player position
        player_pos = self.player.get_position()
        
        # Calculate direction to move toward mouse
        dx = mouse_x - player_pos[0]
        dy = mouse_y - player_pos[1]
        
        # Set movement direction based on mouse position
        if abs(dx) > abs(dy):
            # Move horizontally
            if dx > 5:  # Threshold to avoid jitter
                self.player.right_pressed = True
                self.player.left_pressed = False
            elif dx < -5:
                self.player.left_pressed = True
                self.player.right_pressed = False
            else:
                self.player.left_pressed = False
                self.player.right_pressed = False
        else:
            # Move vertically
            if dy > 5:
                self.player.down_pressed = True
                self.player.up_pressed = False
            elif dy < -5:
                self.player.up_pressed = True
                self.player.down_pressed = False
            else:
                self.player.up_pressed = False
                self.player.down_pressed = False
        
        self.last_mouse_pos = mouse_pos
    
    def draw(self, screen: pygame.Surface):
        """Draw game to screen"""
        tile = self.difficulty_config['cell_size']
        
        # Calculate offset to center maze
        maze_pixel_width = self.maze.width * tile
        maze_pixel_height = self.maze.height * tile
        offset_x = (config.WINDOW_WIDTH - maze_pixel_width) // 2
        offset_y = (config.WINDOW_HEIGHT - maze_pixel_height) // 2
        
        # Draw background
        screen.fill(self.theme['background'])
        
        # Draw maze - use cell.draw() for walls
        wall_color = self.theme['wall']
        for cell in self.maze.grid_cells:
            cell.draw(screen, tile, wall_color, offset_x, offset_y)
        
        # Draw exit (goal point) at exit cell
        exit_x = offset_x + self.maze.exit.x * tile
        exit_y = offset_y + self.maze.exit.y * tile
        exit_rect = pygame.Rect(
            exit_x + tile // 4,
            exit_y + tile // 4,
            tile // 2,
            tile // 2
        )
        pygame.draw.rect(screen, self.theme['exit'], exit_rect)
        # Add glow effect
        pygame.draw.rect(screen, (255, 255, 200), exit_rect, 2)
        
        # Draw hint path if active
        if self.enable_powerups and self.powerup_manager.has_hint():
            player_pos = self.player.get_position()
            # Convert player pixel pos to cell pos for hint path
            player_cell_x = int(player_pos[0] // tile)
            player_cell_y = int(player_pos[1] // tile)
            exit_cell_pos = (self.maze.exit.x, self.maze.exit.y)
            self.powerup_manager.draw_hint_path(
                screen, tile, offset_x, offset_y,
                (player_cell_x, player_cell_y), exit_cell_pos
            )
        
        # Draw power-ups
        if self.enable_powerups:
            self.powerup_manager.draw(screen, tile, offset_x, offset_y)
        
        # Draw enemies
        if self.enable_enemies:
            self.enemy_manager.draw(screen, tile, offset_x, offset_y)
        
        # Draw player at pixel coordinates (with offset)
        player_screen_x = offset_x + self.player.x
        player_screen_y = offset_y + self.player.y
        player_rect = pygame.Rect(
            int(player_screen_x),
            int(player_screen_y),
            self.player.player_size,
            self.player.player_size
        )
        
        # Shadow
        shadow_offset = 2
        shadow_rect = pygame.Rect(
            int(player_screen_x) + shadow_offset,
            int(player_screen_y) + shadow_offset,
            self.player.player_size,
            self.player.player_size
        )
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect)
        
        # Player (with speed boost effect)
        player_color = self.theme['player']
        if self.enable_powerups and self.powerup_manager.get_speed_multiplier() > 1.0:
            # Speed boost - brighter color
            player_color = tuple(min(255, c + 50) for c in player_color)
        
        pygame.draw.rect(screen, player_color, player_rect)
        # Player highlight
        highlight_rect = pygame.Rect(
            int(player_screen_x) - 2,
            int(player_screen_y) - 2,
            self.player.player_size + 4,
            self.player.player_size + 4
        )
        pygame.draw.rect(screen, (255, 255, 255, 100), highlight_rect, 2)
        
        # Draw HUD
        if self.state == config.STATE_PLAYING:
            self.hud.draw(screen)
        
        # Draw pause menu
        if self.state == config.STATE_PAUSED:
            self.pause_menu.draw(screen)
        
        # Draw win screen
        if self.state == config.STATE_WON:
            self.win_screen.draw(screen)

