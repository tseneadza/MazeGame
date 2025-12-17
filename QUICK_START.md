# Maze Game - Quick Start Guide

## 🚀 Quick Launch

### Option 1: Direct Launch (Recommended)
```bash
cd MazeGame
source venv/bin/activate
python3 main.py
```

Or use the start script:
```bash
./start.sh
```

### Option 2: Via Web Interface
1. Start the Codehome launcher: `python3 launcher.py` (from Codehome root)
2. Open http://localhost:8080 in your browser
3. Click "Start App" on the Maze Game card
4. Click "Launch Game" button in the web interface

## 🎮 How to Play

1. **Start**: Click "Start Game" in the main menu
2. **Navigate**: Use WASD or Arrow Keys to move
3. **Goal**: Reach the yellow exit square
4. **Power-ups**: Collect green (speed), yellow (hint), or blue (time) power-ups
5. **Avoid**: Red and purple enemies - they'll reset you to start
6. **Pause**: Press P or ESC to pause
7. **Win**: Complete the maze to see your stats!

## 🎯 Controls

| Action | Key |
|--------|-----|
| Move Up | W or ↑ |
| Move Down | S or ↓ |
| Move Left | A or ← |
| Move Right | D or → |
| Pause/Resume | P or ESC |
| Restart (after win) | R |
| Quit to Menu | ESC (from pause) |

## ⚙️ Settings

### Difficulty Levels
- **Easy**: 15x10 maze, 1 enemy, 3 power-ups
- **Medium**: 20x15 maze, 2 enemies, 5 power-ups  
- **Hard**: 30x20 maze, 4 enemies, 7 power-ups

### Themes
- **Classic**: Traditional blue/gray
- **Dark**: Darker tones
- **Colorful**: Vibrant colors
- **Neon**: Cyberpunk neon style

## 💡 Tips

- **Take your time** - No time limit unless you want the challenge
- **Collect power-ups** - They make the game easier
- **Use hints** - Yellow power-ups show the path
- **Watch for enemies** - They move predictably
- **Try different themes** - Find your favorite style
- **Higher difficulty** - More challenge, more rewards

## 🐛 Troubleshooting

### Game won't start
- Make sure virtual environment is activated: `source venv/bin/activate`
- Check dependencies: `pip install -r requirements.txt`
- Verify Python 3.9+ is installed

### No display/window
- Make sure you have a display (not SSH without X11)
- Pygame requires a graphical environment

### Web interface issues
- Ensure Flask is installed: `pip install flask flask-cors`
- Check port 5107 is available
- Verify launcher.py is running

## 📁 Project Structure

```
MazeGame/
├── main.py              # 🎮 Main game entry point
├── app.py               # 🌐 Web interface
├── game.py              # 🎯 Core game logic
├── maze_generator.py    # 🧩 Maze generation
├── player.py            # 👤 Player movement
├── powerups.py          # ⚡ Power-up system
├── enemies.py           # 👹 Enemy system
├── ui.py                # 🖼️ UI components
├── themes.py            # 🎨 Theme system
├── audio.py             # 🔊 Audio framework
├── config.py            # ⚙️ Configuration
└── README.md            # 📖 Full documentation
```

## 🎉 Features

✅ Procedural maze generation  
✅ 3 difficulty levels  
✅ 4 visual themes  
✅ Power-up system (speed, hints, time)  
✅ Enemy AI with collision  
✅ Real-time HUD (timer, moves)  
✅ Pause/Resume functionality  
✅ Win screen with stats  
✅ Main menu system  

## 🚧 Future Enhancements

- Multiple levels progression
- Save/load game state
- High score system
- Custom player skins
- Sound effects and music
- Particle effects
- Achievement system

Enjoy playing! 🎮
