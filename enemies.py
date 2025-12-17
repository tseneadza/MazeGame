"""
Enemy system for the maze game
"""

import random
import pygame
from typing import List, Tuple, Optional


class Enemy:
    """Enemy that patrols the maze"""
    
    def __init__(self, x: int, y: int, enemy_type: str, theme):
        self.x = x
        self.y = y
        self.type = enemy_type  # 'slow', 'fast', 'patrol'
        self.theme = theme
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.move_timer = 0
        
        # Movement speed based on type
        self.move_delay = {'slow': 60, 'fast': 30, 'patrol': 45}[enemy_type]
        self.size = 15 if enemy_type == 'fast' else 18
    
    def update(self, maze):
        """Update enemy position"""
        self.move_timer += 1
        
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            
            # Try to move in current direction
            dx, dy = self.direction
            new_x = self.x + dx
            new_y = self.y + dy
            
            if maze.is_path(new_x, new_y):
                self.x = new_x
                self.y = new_y
            else:
                # Hit a wall, choose new direction
                possible_dirs = []
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    if maze.is_path(self.x + dx, self.y + dy):
                        possible_dirs.append((dx, dy))
                
                if possible_dirs:
                    self.direction = random.choice(possible_dirs)
    
    def draw(self, screen: pygame.Surface, cell_size: int, offset_x: int, offset_y: int):
        """Draw enemy with high visibility"""
        center_x = offset_x + self.x * cell_size + cell_size // 2
        center_y = offset_y + self.y * cell_size + cell_size // 2
        
        # Enemy color based on type - make them VERY visible
        if self.type == 'slow':
            color = (255, 0, 0)  # Bright red
            glow_color = (255, 100, 100)
        elif self.type == 'fast':
            color = (255, 50, 50)  # Bright red
            glow_color = (255, 150, 150)
        else:  # patrol
            color = (200, 0, 200)  # Bright purple
            glow_color = (255, 100, 255)
        
        # Draw glow effect
        pygame.draw.circle(screen, glow_color, (center_x, center_y), self.size // 2 + 3)
        
        # Draw enemy
        pygame.draw.circle(screen, color, (center_x, center_y), self.size // 2)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.size // 2, 2)
        
        # Draw warning symbol (skull or X)
        font = pygame.font.Font(None, 16)
        warning_text = font.render("!", True, (255, 255, 0))
        warning_rect = warning_text.get_rect(center=(center_x, center_y))
        screen.blit(warning_text, warning_rect)
        
        # Draw eyes
        eye_size = 3
        pygame.draw.circle(screen, (255, 255, 255), (center_x - 4, center_y - 4), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (center_x + 4, center_y - 4), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (center_x - 4, center_y - 4), 1)
        pygame.draw.circle(screen, (0, 0, 0), (center_x + 4, center_y - 4), 1)
    
    def check_collision(self, player_x: int, player_y: int) -> bool:
        """Check if enemy collided with player"""
        return self.x == player_x and self.y == player_y


class EnemyManager:
    """Manages all enemies in the game"""
    
    def __init__(self, maze, theme, difficulty='medium'):
        self.maze = maze
        self.theme = theme
        self.enemies: List[Enemy] = []
        
        # Spawn enemies based on difficulty
        spawn_count = {'easy': 1, 'medium': 2, 'hard': 4}[difficulty]
        self.spawn_enemies(spawn_count, difficulty)
    
    def spawn_enemies(self, count: int, difficulty: str):
        """Spawn enemies randomly in the maze"""
        enemy_types = ['slow'] if difficulty == 'easy' else ['slow', 'fast', 'patrol']
        
        for _ in range(count):
            # Find random path cell
            attempts = 0
            while attempts < 100:
                x = random.randint(1, self.maze.width - 2)
                y = random.randint(1, self.maze.height - 2)
                
                # Don't spawn on entry, exit, or near entry
                if (self.maze.is_path(x, y) and
                    (x, y) != (self.maze.entry.x, self.maze.entry.y) and
                    (x, y) != (self.maze.exit.x, self.maze.exit.y) and
                    abs(x - self.maze.entry.x) + abs(y - self.maze.entry.y) > 5 and
                    not any(e.x == x and e.y == y for e in self.enemies)):
                    
                    enemy_type = random.choice(enemy_types)
                    self.enemies.append(Enemy(x, y, enemy_type, self.theme))
                    break
                
                attempts += 1
    
    def update(self):
        """Update all enemies"""
        for enemy in self.enemies:
            enemy.update(self.maze)
    
    def check_collisions(self, player_x: int, player_y: int) -> bool:
        """Check if player collided with any enemy"""
        for enemy in self.enemies:
            if enemy.check_collision(player_x, player_y):
                return True
        return False
    
    def draw(self, screen: pygame.Surface, cell_size: int, offset_x: int, offset_y: int):
        """Draw all enemies"""
        for enemy in self.enemies:
            enemy.draw(screen, cell_size, offset_x, offset_y)
