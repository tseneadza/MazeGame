"""
Game configuration and constants
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Maze Game"

# Maze settings (default - can be changed by difficulty)
MAZE_WIDTH = 20  # Number of cells horizontally
MAZE_HEIGHT = 15  # Number of cells vertically
CELL_SIZE = 30  # Size of each cell in pixels

# Difficulty settings
DIFFICULTIES = {
    'easy': {'width': 15, 'height': 10, 'cell_size': 35},
    'medium': {'width': 20, 'height': 15, 'cell_size': 30},
    'hard': {'width': 30, 'height': 20, 'cell_size': 25}
}

# Colors
COLOR_BACKGROUND = (20, 20, 30)
COLOR_WALL = (50, 50, 70)
COLOR_PATH = (30, 30, 40)
COLOR_PLAYER = (100, 200, 255)
COLOR_EXIT = (255, 200, 100)
COLOR_TEXT = (255, 255, 255)

# Player settings
PLAYER_SIZE = 20
PLAYER_SPEED = 1  # Cells per move

# Gameplay options
ENABLE_POWERUPS = True
ENABLE_ENEMIES = True

# Visual style options
VISUAL_STYLE_BLOCKS = 'blocks'
VISUAL_STYLE_LINES = 'lines'

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_PAUSED = 3
