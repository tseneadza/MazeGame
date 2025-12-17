"""
Theme system for different visual styles
"""

THEMES = {
    'classic': {
        'name': 'Classic',
        'background': (20, 20, 30),
        'wall': (120, 120, 140),  # Much brighter, clearly visible
        'path': (40, 40, 60),      # Darker path for contrast
        'wall_border': (80, 80, 100),  # Border color for walls
        'player': (100, 200, 255),
        'exit': (255, 200, 100),
        'text': (255, 255, 255),
        'text_secondary': (200, 200, 200),
        'button': (100, 150, 255),
        'button_hover': (120, 170, 255),
        'menu_bg': (15, 15, 25),
    },
    'dark': {
        'name': 'Dark',
        'background': (10, 10, 15),
        'wall': (100, 100, 120),  # Brighter walls
        'path': (25, 25, 35),     # Darker paths
        'wall_border': (60, 60, 80),
        'player': (150, 220, 255),
        'exit': (255, 150, 50),
        'text': (240, 240, 240),
        'text_secondary': (180, 180, 180),
        'button': (80, 120, 200),
        'button_hover': (100, 140, 220),
        'menu_bg': (5, 5, 10),
    },
    'colorful': {
        'name': 'Colorful',
        'background': (25, 25, 50),
        'wall': (150, 100, 180),  # Bright purple walls
        'path': (50, 50, 90),     # Darker blue paths
        'wall_border': (120, 80, 150),
        'player': (100, 255, 200),
        'exit': (255, 100, 150),
        'text': (255, 255, 255),
        'text_secondary': (220, 220, 220),
        'button': (150, 100, 255),
        'button_hover': (170, 120, 255),
        'menu_bg': (20, 20, 40),
    },
    'neon': {
        'name': 'Neon',
        'background': (5, 5, 15),
        'wall': (100, 0, 200),    # Bright purple/neon walls
        'path': (20, 5, 40),      # Darker paths
        'wall_border': (150, 0, 255),  # Glowing border
        'player': (0, 255, 255),
        'exit': (255, 0, 255),
        'text': (255, 255, 255),
        'text_secondary': (200, 200, 255),
        'button': (0, 200, 255),
        'button_hover': (0, 255, 255),
        'menu_bg': (0, 0, 10),
    }
}

def get_theme(theme_name='classic'):
    """Get theme by name, default to classic"""
    return THEMES.get(theme_name, THEMES['classic'])

def get_all_themes():
    """Get list of all available theme names"""
    return list(THEMES.keys())
