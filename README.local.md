# Maze Game

A Python-based maze game built with Pygame. Navigate through procedurally generated mazes to reach the exit!

## Features

### Phase 1: Core Prototype ✅
- **Procedural Maze Generation**: Each game features a unique maze generated using recursive backtracking
- **Smooth Controls**: Use WASD or arrow keys to navigate
- **Win Condition**: Reach the exit to win the game
- **Simple & Fun**: Clean, minimalist design focused on gameplay

### Phase 2: Visual Polish & UI ✅
- **Main Menu**: Beautiful menu with difficulty and theme selection
- **HUD Overlay**: Real-time timer and move counter
- **Win Screen**: Completion stats with play again option
- **Pause Menu**: Pause and resume functionality
- **Theme System**: 4 different visual themes (Classic, Dark, Colorful, Neon)
- **Difficulty Levels**: Easy, Medium, and Hard with different maze sizes

### Phase 3: Advanced Features ✅
- **Power-ups**: 
  - Speed Boost: Move faster for a limited time
  - Hint: See path to exit
  - Time Bonus: Add extra time to your timer
- **Enemies**: Moving enemies that patrol the maze
  - Slow enemies (red)
  - Fast enemies (bright red)
  - Patrol enemies (purple)
- **Collision System**: Touch an enemy to reset to start

### Phase 4: Audio & Polish ✅
- **Audio System**: Framework for sound effects and music
- **Enhanced Graphics**: Shadows, highlights, and visual effects
- **Smooth Animations**: Pulsing power-ups and visual feedback

## Installation

1. Create and activate virtual environment:
```bash
cd MazeGame
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

### Direct Launch:
```bash
python main.py
```

### Via Web Interface:
1. Start the launcher: `python3 launcher.py` (from Codehome root)
2. Open http://localhost:8080
3. Click "Start App" on Maze Game card
4. Click "Launch Game" in the web interface

## Controls

### In-Game:
- **WASD** or **Arrow Keys**: Move player
- **P** or **ESC**: Pause/Resume game
- **R**: Restart game (after winning)
- **ESC**: Quit to menu (from pause)

### Menu:
- **Mouse**: Click buttons to navigate
- **Difficulty**: Select Easy, Medium, or Hard
- **Theme**: Choose visual style (Classic, Dark, Colorful, Neon)

## Difficulty Levels

- **Easy**: 15x10 maze, 1 enemy, 3 power-ups
- **Medium**: 20x15 maze, 2 enemies, 5 power-ups
- **Hard**: 30x20 maze, 4 enemies, 7 power-ups

## Power-ups

- **⚡ Speed Boost** (Green): Move 2x faster for 5 seconds
- **❓ Hint** (Yellow): See path indicators to exit
- **⏰ Time Bonus** (Blue): Add 10 seconds to your timer

## Enemies

- **Slow Enemy** (Dark Red): Moves slowly, easy to avoid
- **Fast Enemy** (Bright Red): Moves quickly, more challenging
- **Patrol Enemy** (Purple): Medium speed, patrols maze

## Themes

- **Classic**: Traditional blue and gray color scheme
- **Dark**: Darker tones for reduced eye strain
- **Colorful**: Vibrant colors for a fun experience
- **Neon**: Cyberpunk-style neon colors

## Project Structure

```
MazeGame/
├── main.py              # Main entry point
├── app.py               # Flask web interface
├── game.py              # Core game loop and state management
├── maze_generator.py    # Maze generation algorithm
├── player.py            # Player class and movement
├── powerups.py          # Power-up system
├── enemies.py           # Enemy system
├── ui.py                # UI components (menu, HUD, etc.)
├── themes.py            # Theme system
├── audio.py             # Audio management
├── config.py            # Game configuration
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── assets/              # Game assets (sprites, sounds, themes)
    ├── sprites/
    ├── sounds/
    └── themes/
```

## Technical Details

- **Framework**: Pygame 2.6+
- **Language**: Python 3
- **Algorithm**: Recursive backtracking for maze generation
- **Rendering**: 60 FPS game loop
- **Window Size**: 800x600 pixels
- **Maze Sizes**: Configurable (15x10 to 30x20)

## Future Enhancements

- [ ] Multiple levels progression
- [ ] Save/load game state
- [ ] High score system
- [ ] Custom player skins
- [ ] More power-up types
- [ ] Boss enemies
- [ ] Sound effects and background music
- [ ] Particle effects
- [ ] Achievement system

## Development Status

✅ **Phase 1**: Core Prototype - Complete
✅ **Phase 2**: Visual Polish & UI - Complete
✅ **Phase 3**: Advanced Features - Complete
✅ **Phase 4**: Audio & Polish - Complete

The game is fully playable with all planned features implemented!

## Tips

- Take your time - there's no time limit (unless you want the challenge)
- Collect power-ups to make the game easier
- Avoid enemies - they'll reset you to the start
- Use hints when stuck to find the path
- Try different themes to find your favorite style
- Higher difficulties offer more challenge and rewards

Enjoy playing! 🎮
