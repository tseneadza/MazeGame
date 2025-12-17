"""
Power-up system for the maze game
"""

import random
import pygame
from typing import List, Tuple, Optional


class PowerUp:
    """Base power-up class"""
    
    def __init__(self, x: int, y: int, power_type: str, theme):
        self.x = x
        self.y = y
        self.type = power_type  # 'speed', 'hint', 'time'
        self.collected = False
        self.theme = theme
        self.animation_frame = 0
        
        # Power-up colors
        self.colors = {
            'speed': (100, 255, 100),
            'hint': (255, 255, 100),
            'time': (100, 200, 255)
        }
    
    def draw(self, screen: pygame.Surface, cell_size: int, offset_x: int, offset_y: int):
        """Draw power-up"""
        if self.collected:
            return
        
        center_x = offset_x + self.x * cell_size + cell_size // 2
        center_y = offset_y + self.y * cell_size + cell_size // 2
        radius = cell_size // 3
        
        # Animated pulsing effect
        pulse = int(2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
        radius = radius + pulse
        
        color = self.colors.get(self.type, (255, 255, 255))
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius, 2)
        
        # Icon based on type
        if self.type == 'speed':
            # Lightning bolt
            points = [
                (center_x - 3, center_y - 5),
                (center_x, center_y - 2),
                (center_x - 2, center_y),
                (center_x + 3, center_y + 5),
                (center_x, center_y + 2),
                (center_x + 2, center_y)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points)
        elif self.type == 'hint':
            # Question mark
            font = pygame.font.Font(None, 20)
            text = font.render("?", True, (0, 0, 0))
            text_rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, text_rect)
        elif self.type == 'time':
            # Clock icon
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), radius - 2, 2)
            pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (center_x, center_y - 4), 2)
            pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (center_x + 3, center_y), 2)
    
    def check_collection(self, player_x: int, player_y: int) -> bool:
        """Check if player collected this power-up"""
        if self.collected:
            return False
        
        if self.x == player_x and self.y == player_y:
            self.collected = True
            return True
        return False


class PowerUpManager:
    """Manages all power-ups in the game"""
    
    def __init__(self, maze, theme, difficulty='medium'):
        self.maze = maze
        self.theme = theme
        self.powerups: List[PowerUp] = []
        self.active_effects = {
            'speed': 0,  # Frames remaining
            'hint': False,
            'time': 0  # Seconds to add
        }
        
        # Spawn power-ups based on difficulty
        spawn_count = {'easy': 3, 'medium': 5, 'hard': 7}[difficulty]
        self.spawn_powerups(spawn_count)
    
    def spawn_powerups(self, count: int):
        """Spawn power-ups randomly in the maze"""
        power_types = ['speed', 'hint', 'time']
        
        for _ in range(count):
            # Find random path cell
            attempts = 0
            while attempts < 100:
                x = random.randint(1, self.maze.width - 2)
                y = random.randint(1, self.maze.height - 2)
                
                # Don't spawn on entry, exit, or existing power-ups
                if (self.maze.is_path(x, y) and
                    (x, y) != (self.maze.entry.x, self.maze.entry.y) and
                    (x, y) != (self.maze.exit.x, self.maze.exit.y) and
                    not any(p.x == x and p.y == y for p in self.powerups)):
                    
                    power_type = random.choice(power_types)
                    self.powerups.append(PowerUp(x, y, power_type, self.theme))
                    break
                
                attempts += 1
    
    def check_collections(self, player_x: int, player_y: int):
        """Check if player collected any power-ups"""
        for powerup in self.powerups:
            if powerup.check_collection(player_x, player_y):
                self.activate_powerup(powerup.type)
                return powerup.type
        return None
    
    def activate_powerup(self, power_type: str):
        """Activate a power-up effect"""
        if power_type == 'speed':
            self.active_effects['speed'] = 300  # 5 seconds at 60 FPS
        elif power_type == 'hint':
            self.active_effects['hint'] = True
        elif power_type == 'time':
            self.active_effects['time'] = 10  # Add 10 seconds
    
    def update(self):
        """Update power-up effects"""
        # Decrease speed boost timer
        if self.active_effects['speed'] > 0:
            self.active_effects['speed'] -= 1
    
    def get_speed_multiplier(self) -> float:
        """Get current speed multiplier"""
        return 2.0 if self.active_effects['speed'] > 0 else 1.0
    
    def has_hint(self) -> bool:
        """Check if hint is active"""
        return self.active_effects['hint']
    
    def get_time_bonus(self) -> int:
        """Get time bonus and reset"""
        bonus = self.active_effects['time']
        self.active_effects['time'] = 0
        return bonus
    
    def draw(self, screen: pygame.Surface, cell_size: int, offset_x: int, offset_y: int):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen, cell_size, offset_x, offset_y)
    
    def draw_hint_path(self, screen: pygame.Surface, cell_size: int, offset_x: int, offset_y: int, player_pos: Tuple[int, int], exit_pos: Tuple[int, int]):
        """Draw hint path to exit (simplified A* pathfinding)"""
        if not self.active_effects['hint']:
            return
        
        # Simple pathfinding - just show direction arrows
        px, py = player_pos
        ex, ey = exit_pos
        
        # Draw arrow pointing towards exit
        if abs(ex - px) > abs(ey - py):
            # Horizontal direction
            direction = 1 if ex > px else -1
            for x in range(px, ex, direction):
                if self.maze.is_path(x, py):
                    arrow_x = offset_x + x * cell_size + cell_size // 2
                    arrow_y = offset_y + py * cell_size + cell_size // 2
                    # Draw arrow
                    pygame.draw.circle(screen, (255, 255, 0, 100), (arrow_x, arrow_y), 3)
        else:
            # Vertical direction
            direction = 1 if ey > py else -1
            for y in range(py, ey, direction):
                if self.maze.is_path(px, y):
                    arrow_x = offset_x + px * cell_size + cell_size // 2
                    arrow_y = offset_y + y * cell_size + cell_size // 2
                    # Draw arrow
                    pygame.draw.circle(screen, (255, 255, 0, 100), (arrow_x, arrow_y), 3)
