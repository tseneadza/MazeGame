"""
Maze generation using recursive backtracking algorithm
Uses Cell-based system where each cell has walls that can be removed
"""

import random
from typing import List, Tuple, Set
from cell import Cell


class Maze:
    """Represents a maze with cells that have walls"""
    
    def __init__(self, width: int, height: int):
        self.width = width  # Number of columns
        self.height = height  # Number of rows
        self.thickness = 4  # Wall thickness
        # Create grid of cells
        self.grid_cells = [Cell(col, row, self.thickness) 
                          for row in range(self.height) 
                          for col in range(self.width)]
        # Entry and exit cells
        self.entry = None
        self.exit = None
        
    def remove_walls(self, current, next):
        """Remove walls between two adjacent cells"""
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False
    
    def generate(self):
        """Generate maze using recursive backtracking algorithm"""
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1
        
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.width, self.height, self.grid_cells)
            
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        
        # Set entry (top-left area) and exit (bottom-right area)
        self.entry = self.grid_cells[0]  # First cell
        self.exit = self.grid_cells[-1]  # Last cell
        
        # Remove entry wall (top of first cell)
        self.entry.walls['top'] = False
        # Remove exit wall (bottom of last cell)
        self.exit.walls['bottom'] = False
    
    def get_cell_at(self, x: int, y: int) -> Cell:
        """Get cell at grid coordinates"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        find_index = lambda x, y: x + y * self.width
        return self.grid_cells[find_index(x, y)]
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall (for backward compatibility)"""
        # In the Cell-based system, all cells are paths (walls are between cells)
        # This method is kept for compatibility but always returns False
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return False  # All cells are paths in this system
    
    def is_path(self, x: int, y: int) -> bool:
        """Check if position is a path"""
        # In Cell-based system, all valid cells are paths
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True  # All valid cells are paths
