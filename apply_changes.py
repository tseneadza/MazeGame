#!/usr/bin/env python3
"""
Script to apply all changes to the maze game:
- Add visual style option (blocks vs lines)
- Place entry/exit on borders
- Add mouse/trackpad navigation
"""

import os
import re

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def update_config():
    """Add visual style constants to config.py"""
    filepath = os.path.join(SCRIPT_DIR, 'config.py')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add visual style constants after ENABLE_ENEMIES
    if 'VISUAL_STYLE_BLOCKS' not in content:
        content = content.replace(
            'ENABLE_ENEMIES = True\n\n# Game states',
            'ENABLE_ENEMIES = True\n\n# Visual style options\nVISUAL_STYLE_BLOCKS = \'blocks\'\nVISUAL_STYLE_LINES = \'lines\'\n\n# Game states'
        )
        with open(filepath, 'w') as f:
            f.write(content)
        print("✓ Updated config.py")
    else:
        print("✓ config.py already updated")

def update_maze_generator():
    """Update maze_generator.py to place entry/exit on borders"""
    filepath = os.path.join(SCRIPT_DIR, 'maze_generator.py')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace __init__ method
    old_init = r'    def __init__\(self, width: int, height: int\):.*?self\.exit = \(max\(1, exit_x\), max\(1, exit_y\)\)'
    new_init = '''    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # 0 = wall, 1 = path
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        # Entry and exit will be placed on borders in generate()
        self.entry = None
        self.exit = None'''
    
    content = re.sub(old_init, new_init, content, flags=re.DOTALL)
    
    # Replace generate method - need to be careful with the regex
    old_generate_start = r'    def generate\(self\):'
    old_generate_end = r'        # Verify and fix any connectivity issues\n        self\._verify_connectivity\(\)'
    
    # Find the generate method and replace it
    generate_pattern = r'(    def generate\(self\):.*?)(        # Verify and fix any connectivity issues\n        self\._verify_connectivity\(\))'
    
    new_generate = '''    def generate(self):
        """Generate maze using recursive backtracking - ensures single solution path"""
        # Initialize all cells as walls
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        
        # Place entry on top border (prefer left side)
        entry_x = 1 if self.width > 2 else 0
        entry_y = 0
        self.entry = (entry_x, entry_y)
        
        # Place exit on bottom border (prefer right side)
        exit_x = self.width - 2 if self.width > 2 else self.width - 1
        exit_y = self.height - 1
        self.exit = (exit_x, exit_y)
        
        # Ensure entry and exit are paths
        self.grid[self.entry[1]][self.entry[0]] = 1
        self.grid[self.exit[1]][self.exit[0]] = 1
        
        # Start from a cell adjacent to entry (inside the maze)
        start_x = self.entry[0]
        start_y = self.entry[1] + 1 if self.entry[1] == 0 else self.entry[1] - 1
        if start_y < 0 or start_y >= self.height:
            start_y = self.entry[1]
            start_x = self.entry[0] + 1 if self.entry[0] == 0 else self.entry[0] - 1
        
        # Ensure start is within bounds and is a valid path cell
        start_x = max(1, min(start_x, self.width - 2))
        start_y = max(1, min(start_y, self.height - 2))
        # Make sure it's an odd coordinate for proper maze structure
        if start_x % 2 == 0:
            start_x = max(1, start_x - 1)
        if start_y % 2 == 0:
            start_y = max(1, start_y - 1)
        
        # Connect entry to start
        self.grid[start_y][start_x] = 1
        if start_x != self.entry[0]:
            # Connect horizontally
            for x in range(min(start_x, self.entry[0]), max(start_x, self.entry[0]) + 1):
                self.grid[start_y][x] = 1
        if start_y != self.entry[1]:
            # Connect vertically
            for y in range(min(start_y, self.entry[1]), max(start_y, self.entry[1]) + 1):
                self.grid[y][self.entry[0]] = 1
        
        # Start from entry point
        stack = [(start_x, start_y)]
        visited = {(start_x, start_y), self.entry}
        
        # Directions: up, right, down, left (step by 2 to create walls between)
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        
        # Track if we've reached the exit
        exit_reached = False
        
        while stack:
            current = stack[-1]
            x, y = current
            
            # Check if we're near exit
            if abs(x - self.exit[0]) <= 1 and abs(y - self.exit[1]) <= 1:
                exit_reached = True
            
            # Find unvisited neighbors (must be odd coordinates for proper maze structure)
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Ensure we stay within bounds (but allow reaching exit area)
                if (1 <= nx < self.width - 1 and 
                    1 <= ny < self.height - 1 and 
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx // 2, dy // 2))
            
            if neighbors:
                # Choose random neighbor
                nx, ny, wall_x, wall_y = random.choice(neighbors)
                next_cell = (nx, ny)
                
                # Carve path to neighbor (including the wall between)
                self.grid[y + wall_y][x + wall_x] = 1  # Remove wall
                self.grid[ny][nx] = 1  # Create path
                
                visited.add(next_cell)
                stack.append(next_cell)
            else:
                # Backtrack
                stack.pop()
        
        # Connect exit to nearest path
        if not exit_reached:
            self._connect_exit_to_path()
        
        # Verify and fix any connectivity issues
        self._verify_connectivity()'''
    
    # Use a more targeted replacement
    if 'Place entry on top border' not in content:
        # Find the generate method by looking for its start and the verify_connectivity call
        pattern = r'(    def generate\(self\):.*?)(        # Verify and fix any connectivity issues\n        self\._verify_connectivity\(\))'
        content = re.sub(pattern, r'\1' + new_generate.split('def generate')[1].split('_verify_connectivity')[0] + '        # Verify and fix any connectivity issues\n        self._verify_connectivity())', content, flags=re.DOTALL)
        
        # Actually, let's do a simpler approach - replace the whole method
        start_marker = '    def generate(self):'
        end_marker = '        self._verify_connectivity()'
        
        start_idx = content.find(start_marker)
        if start_idx != -1:
            # Find the end of the method (next method or end of class)
            end_idx = content.find(end_marker, start_idx)
            if end_idx != -1:
                end_idx = content.find('\n    def ', end_idx)
                if end_idx == -1:
                    end_idx = content.find('\n\n    def ', end_idx)
                if end_idx == -1:
                    end_idx = len(content)
                else:
                    end_idx = content.rfind('\n', start_idx, end_idx) + 1
                
                # Replace the method
                before = content[:start_idx]
                after = content[end_idx:]
                content = before + new_generate + '\n    ' + after
    
    # Replace _ensure_exit_path with _connect_exit_to_path
    old_method_pattern = r'    def _ensure_exit_path\(self\):.*?self\.grid\[ey\]\[ex\] = 1'
    new_method = '''    def _connect_exit_to_path(self):
        """Connect exit to the nearest path in the maze"""
        # Find the closest path cell to the exit
        closest = None
        min_dist = float('inf')
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1 and (x, y) != self.exit:  # If it's a path
                    dist = abs(x - self.exit[0]) + abs(y - self.exit[1])
                    if dist < min_dist:
                        min_dist = dist
                        closest = (x, y)
        
        if closest:
            # Create a path from closest point to exit
            cx, cy = closest
            ex, ey = self.exit
            
            # Create path connecting them
            step_x = 1 if ex > cx else -1 if ex < cx else 0
            step_y = 1 if ey > cy else -1 if ey < cy else 0
            
            # Connect horizontally first, then vertically
            x = cx
            while x != ex:
                self.grid[cy][x] = 1
                x += step_x
            
            # Connect vertically
            y = cy
            while y != ey:
                self.grid[y][ex] = 1
                y += step_y
            
            self.grid[ey][ex] = 1'''
    
    if '_connect_exit_to_path' not in content:
        content = re.sub(old_method_pattern, new_method, content, flags=re.DOTALL)
    
    # Update _verify_connectivity to call _connect_exit_to_path
    content = content.replace('self._ensure_exit_path()', 'self._connect_exit_to_path()')
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("✓ Updated maze_generator.py")

def update_game():
    """Update game.py with visual style, mouse navigation, and line drawing"""
    filepath = os.path.join(SCRIPT_DIR, 'game.py')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Update __init__ to accept visual_style parameter
    content = content.replace(
        "    def __init__(self, difficulty='medium', theme_name='classic'):",
        "    def __init__(self, difficulty='medium', theme_name='classic', visual_style='blocks'):"
    )
    
    # Add visual_style and mouse navigation after difficulty_config
    if 'self.visual_style = visual_style' not in content:
        content = content.replace(
            "        self.difficulty_config = config.DIFFICULTIES[difficulty]\n        \n        # Initialize maze",
            "        self.difficulty_config = config.DIFFICULTIES[difficulty]\n        self.visual_style = visual_style  # 'blocks' or 'lines'\n        \n        # Initialize maze"
        )
        
        # Add mouse navigation after player initialization
        content = content.replace(
            "        self.player.size = int(self.difficulty_config['cell_size'] * 0.65)\n        \n        # Game state",
            "        self.player.size = int(self.difficulty_config['cell_size'] * 0.65)\n        \n        # Mouse navigation\n        self.mouse_navigation_enabled = True\n        self.last_mouse_pos = None\n        \n        # Game state"
        )
    
    # Update reset method
    content = content.replace(
        "    def reset(self, difficulty=None, theme_name=None):",
        "    def reset(self, difficulty=None, theme_name=None, visual_style=None):"
    )
    
    if 'if visual_style:' not in content:
        content = content.replace(
            "        if theme_name:\n            self.theme = get_theme(theme_name)\n            self.hud.theme = self.theme",
            "        if theme_name:\n            self.theme = get_theme(theme_name)\n            self.hud.theme = self.theme\n        \n        if visual_style:\n            self.visual_style = visual_style"
        )
        
        # Reset mouse navigation
        content = content.replace(
            "        # Reset player\n        self.player.set_position(self.maze.entry[0], self.maze.entry[1])\n        self.player.size = int(self.difficulty_config['cell_size'] * 0.65)\n        \n        # Reset state",
            "        # Reset player\n        self.player.set_position(self.maze.entry[0], self.maze.entry[1])\n        self.player.size = int(self.difficulty_config['cell_size'] * 0.65)\n        \n        # Reset mouse navigation\n        self.last_mouse_pos = None\n        \n        # Reset state"
        )
    
    # Update handle_mouse to add navigation
    if '_handle_mouse_navigation' not in content:
        old_handle_mouse = r'    def handle_mouse\(self, event\):.*?        return None'
        new_handle_mouse = '''    def handle_mouse(self, event):
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
        """Handle mouse/trackpad navigation"""
        if self.last_mouse_pos is None:
            self.last_mouse_pos = mouse_pos
            return
        
        cell_size = self.difficulty_config['cell_size']
        maze_pixel_width = self.maze.width * cell_size
        maze_pixel_height = self.maze.height * cell_size
        
        # Calculate offset to center maze
        offset_x = (config.WINDOW_WIDTH - maze_pixel_width) // 2
        offset_y = (config.WINDOW_HEIGHT - maze_pixel_height) // 2
        
        # Convert mouse position to maze coordinates
        maze_x = (mouse_pos[0] - offset_x) // cell_size
        maze_y = (mouse_pos[1] - offset_y) // cell_size
        
        # Check if mouse is over a valid path cell
        if (0 <= maze_x < self.maze.width and 
            0 <= maze_y < self.maze.height and
            self.maze.is_path(maze_x, maze_y)):
            
            # Calculate direction to move
            dx = maze_x - self.player.x
            dy = maze_y - self.player.y
            
            # Move one step at a time toward mouse position
            moved = False
            if abs(dx) > abs(dy):
                # Move horizontally
                if dx > 0:
                    moved = self.player.move_right(self.maze, 1.0)
                elif dx < 0:
                    moved = self.player.move_left(self.maze, 1.0)
            else:
                # Move vertically
                if dy > 0:
                    moved = self.player.move_down(self.maze, 1.0)
                elif dy < 0:
                    moved = self.player.move_up(self.maze, 1.0)
            
            if moved:
                self.hud.increment_move()
                audio_manager.play_sound('move', 0.1)
                
                # Check power-up collection
                if self.enable_powerups:
                    player_pos = self.player.get_position()
                    powerup_type = self.powerup_manager.check_collections(player_pos[0], player_pos[1])
                    if powerup_type:
                        audio_manager.play_sound('powerup', 0.5)
                
                self.update()
        
        self.last_mouse_pos = mouse_pos'''
        
        content = re.sub(old_handle_mouse, new_handle_mouse, content, flags=re.DOTALL)
    
    # Update draw method to use visual style
    if '_draw_maze_blocks' not in content:
        # Replace the maze drawing loop with a call to the appropriate method
        old_draw_maze = r'        # Draw maze\n        for y in range\(self\.maze\.height\):.*?                    pygame\.draw\.rect\(screen, \(0, 0, 0, 50\), rect, 1\)'
        new_draw_maze = '''        # Draw maze based on visual style
        if self.visual_style == config.VISUAL_STYLE_LINES:
            self._draw_maze_lines(screen, cell_size, offset_x, offset_y)
        else:
            self._draw_maze_blocks(screen, cell_size, offset_x, offset_y)'''
        
        content = re.sub(old_draw_maze, new_draw_maze, content, flags=re.DOTALL)
        
        # Add drawing methods at the end of the draw method, before the exit drawing
        drawing_methods = '''
    def _draw_maze_blocks(self, screen, cell_size, offset_x, offset_y):
        """Draw maze using block-based walls"""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(
                    offset_x + x * cell_size,
                    offset_y + y * cell_size,
                    cell_size,
                    cell_size
                )
                
                if self.maze.is_wall(x, y):
                    # Draw wall with high visibility
                    pygame.draw.rect(screen, self.theme['wall'], rect)
                    wall_border = self.theme.get('wall_border', (80, 80, 100))
                    pygame.draw.rect(screen, wall_border, rect, 2)
                    inner_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
                    highlight = tuple(min(255, c + 30) for c in self.theme['wall'])
                    pygame.draw.rect(screen, highlight, inner_rect)
                else:
                    # Draw path
                    pygame.draw.rect(screen, self.theme['path'], rect)
                    pygame.draw.rect(screen, (0, 0, 0, 50), rect, 1)
    
    def _draw_maze_lines(self, screen, cell_size, offset_x, offset_y):
        """Draw maze using line-based walls"""
        wall_color = self.theme['wall']
        path_color = self.theme['path']
        line_width = max(2, cell_size // 15)
        
        # Draw background paths
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.is_path(x, y):
                    rect = pygame.Rect(
                        offset_x + x * cell_size,
                        offset_y + y * cell_size,
                        cell_size,
                        cell_size
                    )
                    pygame.draw.rect(screen, path_color, rect)
        
        # Draw walls as lines between cells
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell_x = offset_x + x * cell_size
                cell_y = offset_y + y * cell_size
                
                # Check each direction for walls
                # Top wall
                if y == 0 or (y > 0 and (self.maze.is_wall(x, y - 1) or self.maze.is_wall(x, y))):
                    pygame.draw.line(screen, wall_color, 
                                   (cell_x, cell_y), 
                                   (cell_x + cell_size, cell_y), line_width)
                
                # Right wall
                if x == self.maze.width - 1 or (x < self.maze.width - 1 and (self.maze.is_wall(x + 1, y) or self.maze.is_wall(x, y))):
                    pygame.draw.line(screen, wall_color,
                                   (cell_x + cell_size, cell_y),
                                   (cell_x + cell_size, cell_y + cell_size), line_width)
                
                # Bottom wall
                if y == self.maze.height - 1 or (y < self.maze.height - 1 and (self.maze.is_wall(x, y + 1) or self.maze.is_wall(x, y))):
                    pygame.draw.line(screen, wall_color,
                                   (cell_x, cell_y + cell_size),
                                   (cell_x + cell_size, cell_y + cell_size), line_width)
                
                # Left wall
                if x == 0 or (x > 0 and (self.maze.is_wall(x - 1, y) or self.maze.is_wall(x, y))):
                    pygame.draw.line(screen, wall_color,
                                   (cell_x, cell_y),
                                   (cell_x, cell_y + cell_size), line_width)
'''
        
        # Insert before the last method or at the end of the class
        # Find where to insert (before the last closing of the class)
        insert_pos = content.rfind('            self.win_screen.draw(screen)')
        if insert_pos != -1:
            # Find the end of the draw method
            end_pos = content.find('\n\n', insert_pos)
            if end_pos == -1:
                end_pos = len(content)
            content = content[:end_pos] + drawing_methods + content[end_pos:]
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("✓ Updated game.py")

def update_ui():
    """Update ui.py to add visual style menu option"""
    filepath = os.path.join(SCRIPT_DIR, 'ui.py')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add selected_visual_style
    if 'self.selected_visual_style' not in content:
        content = content.replace(
            "        self.selected_difficulty = 'medium'\n        self.selected_theme = 'classic'",
            "        self.selected_difficulty = 'medium'\n        self.selected_theme = 'classic'\n        self.selected_visual_style = 'blocks'  # 'blocks' or 'lines'"
        )
    
    # Add visual style buttons after theme buttons
    if 'visual_style_buttons' not in content:
        content = content.replace(
            "            )\n        \n        self.quit_button = Button(",
            "            )\n        \n        # Visual style buttons\n        self.visual_style_buttons = {\n            'blocks': Button(center_x - 100, start_y + 190, 90, 35, \"Blocks\", theme, 'style_blocks'),\n            'lines': Button(center_x + 10, start_y + 190, 90, 35, \"Lines\", theme, 'style_lines'),\n        }\n        \n        self.quit_button = Button("
        )
        
        # Update quit button position
        content = content.replace(
            "            center_x - button_width // 2,\n            start_y + 200,",
            "            center_x - button_width // 2,\n            start_y + 250,"
        )
    
    # Update draw method to show visual style
    if 'Visual style label' not in content:
        content = content.replace(
            "            button.draw(screen, self.font_small)\n        \n        self.quit_button.draw(screen, self.font_medium)",
            "            button.draw(screen, self.font_small)\n        \n        # Visual style label\n        style_label = self.font_small.render(\"Style:\", True, self.theme['text_secondary'])\n        screen.blit(style_label, (config.WINDOW_WIDTH // 2 - 100, start_y + 170))\n        \n        for name, button in self.visual_style_buttons.items():\n            if name == self.selected_visual_style:\n                # Highlight selected\n                pygame.draw.rect(screen, self.theme['exit'], button.rect, 3)\n            button.draw(screen, self.font_small)\n        \n        self.quit_button.draw(screen, self.font_medium)"
        )
    
    # Update handle_event to handle visual style
    if 'for button in self.visual_style_buttons.values():' not in content:
        content = content.replace(
            "            for button in self.theme_buttons.values():\n                button.check_hover(pos)\n            self.quit_button.check_hover(pos)",
            "            for button in self.theme_buttons.values():\n                button.check_hover(pos)\n            for button in self.visual_style_buttons.values():\n                button.check_hover(pos)\n            self.quit_button.check_hover(pos)"
        )
        
        content = content.replace(
            "                    self.selected_theme = name\n                    return action\n            \n            action = self.quit_button.check_click(pos)",
            "                    self.selected_theme = name\n                    return action\n            \n            for name, button in self.visual_style_buttons.items():\n                action = button.check_click(pos)\n                if action:\n                    self.selected_visual_style = name\n                    return action\n            \n            action = self.quit_button.check_click(pos)"
        )
    
    # Update update_theme
    if 'for button in self.visual_style_buttons.values():' not in content.split('update_theme')[1] if 'update_theme' in content else True:
        content = content.replace(
            "        for button in self.theme_buttons.values():\n            button.theme = theme",
            "        for button in self.theme_buttons.values():\n            button.theme = theme\n        for button in self.visual_style_buttons.values():\n            button.theme = theme"
        )
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("✓ Updated ui.py")

def update_main():
    """Update main.py to pass visual style to game"""
    filepath = os.path.join(SCRIPT_DIR, 'main.py')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add current_visual_style
    if 'current_visual_style' not in content:
        content = content.replace(
            "    current_theme = 'classic'\n    current_difficulty = 'medium'",
            "    current_theme = 'classic'\n    current_difficulty = 'medium'\n    current_visual_style = 'blocks'"
        )
    
    # Update Game creation
    content = content.replace(
        "                    game = Game(menu.selected_difficulty, menu.selected_theme)",
        "                    game = Game(menu.selected_difficulty, menu.selected_theme, menu.selected_visual_style)"
    )
    
    # Update current_visual_style assignment
    if 'current_visual_style = menu.selected_visual_style' not in content:
        content = content.replace(
            "                    current_difficulty = menu.selected_difficulty\n                    current_theme = menu.selected_theme",
            "                    current_difficulty = menu.selected_difficulty\n                    current_theme = menu.selected_theme\n                    current_visual_style = menu.selected_visual_style"
        )
    
    # Handle style actions
    if 'elif action and action.startswith(\'style_\'):' not in content:
        content = content.replace(
            "                elif action and action.startswith('theme_'):\n                    # Theme already handled in menu\n                    theme_name = action.replace('theme_', '')\n                    current_theme = theme_name\n                    menu.update_theme(get_theme(theme_name))",
            "                elif action and action.startswith('theme_'):\n                    # Theme already handled in menu\n                    theme_name = action.replace('theme_', '')\n                    current_theme = theme_name\n                    menu.update_theme(get_theme(theme_name))\n                \n                elif action and action.startswith('style_'):\n                    # Visual style already handled in menu\n                    pass"
        )
    
    # Update reset calls to pass visual_style
    content = content.replace(
        "                    if action == 'restart':\n                        game.reset()",
        "                    if action == 'restart':\n                        game.reset(visual_style=current_visual_style)"
    )
    
    # Update menu state restoration
    if 'menu.selected_visual_style = current_visual_style' not in content:
        content = content.replace(
            "                        menu.selected_difficulty = current_difficulty\n                        menu.selected_theme = current_theme",
            "                        menu.selected_difficulty = current_difficulty\n                        menu.selected_theme = current_theme\n                        menu.selected_visual_style = current_visual_style"
        )
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("✓ Updated main.py")

def main():
    """Apply all changes"""
    print("Applying changes to maze game files...")
    print()
    
    try:
        update_config()
        update_maze_generator()
        update_game()
        update_ui()
        update_main()
        
        print()
        print("✓ All changes applied successfully!")
        print("You can now test the game with:")
        print("  - Visual style option (Blocks/Lines) in menu")
        print("  - Entry/exit on borders")
        print("  - Mouse/trackpad navigation")
        
    except Exception as e:
        print(f"✗ Error applying changes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
