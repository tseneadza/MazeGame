"""
Player class for pixel-based movement with wall collision detection
"""

import pygame
from typing import Tuple
import config


class Player:
    """Represents the player in the maze with pixel-based movement"""
    
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.player_size = 10
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)
        self.color = (250, 120, 60)  # Orange color
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
    
    def get_current_cell(self, x, y, tile, grid_cells, cols, rows):
        """Get current cell position of the player"""
        cell_x = int(x // tile)
        cell_y = int(y // tile)
        find_index = lambda x, y: x + y * cols
        if cell_x < 0 or cell_x > cols - 1 or cell_y < 0 or cell_y > rows - 1:
            return None
        return grid_cells[find_index(cell_x, cell_y)]
    
    def check_move(self, tile, grid_cells, thickness, cols, rows):
        """Stop player from passing through walls"""
        current_cell_x = int(self.x // tile)
        current_cell_y = int(self.y // tile)
        current_cell = self.get_current_cell(self.x, self.y, tile, grid_cells, cols, rows)
        
        if not current_cell:
            return
        
        current_cell_abs_x = current_cell_x * tile
        current_cell_abs_y = current_cell_y * tile
        
        if self.left_pressed:
            if current_cell.walls['left']:
                if self.x <= current_cell_abs_x + thickness:
                    self.left_pressed = False
        
        if self.right_pressed:
            if current_cell.walls['right']:
                if self.x >= current_cell_abs_x + tile - (self.player_size + thickness):
                    self.right_pressed = False
        
        if self.up_pressed:
            if current_cell.walls['top']:
                if self.y <= current_cell_abs_y + thickness:
                    self.up_pressed = False
        
        if self.down_pressed:
            if current_cell.walls['bottom']:
                if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                    self.down_pressed = False
    
    def draw(self, screen):
        """Draw player to the screen"""
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self):
        """Update player position while moving"""
        self.velX = 0
        self.velY = 0
        
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        
        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)
    
    def get_position(self) -> Tuple[float, float]:
        """Get current position"""
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float):
        """Set player position"""
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)
