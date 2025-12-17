"""
Cell class representing a single cell in the maze grid
Each cell has walls on top, right, bottom, and left
"""

import pygame
import random


class Cell:
    """Represents a single cell within the maze grid"""
    
    def __init__(self, x, y, thickness):
        self.x = x
        self.y = y
        self.thickness = thickness
        # Walls: True means wall exists, False means no wall (path)
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw(self, screen, tile, wall_color, offset_x=0, offset_y=0):
        """Draw cell walls as lines"""
        x = offset_x + self.x * tile
        y = offset_y + self.y * tile
        
        # Draw each wall if it exists
        if self.walls['top']:
            pygame.draw.line(screen, wall_color, (x, y), (x + tile, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(screen, wall_color, (x + tile, y), (x + tile, y + tile), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(screen, wall_color, (x + tile, y + tile), (x, y + tile), self.thickness)
        if self.walls['left']:
            pygame.draw.line(screen, wall_color, (x, y + tile), (x, y), self.thickness)
    
    def check_cell(self, x, y, cols, rows, grid_cells):
        """Check if cell exists and return it"""
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self, cols, rows, grid_cells):
        """Check cell neighbors and return a random unvisited neighbor"""
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        
        return random.choice(neighbors) if neighbors else False
