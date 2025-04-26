# 🐍 Python Snake Game

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)](https://www.pygame.org/)

A modern reimagining of the classic Snake arcade game built with Python and Pygame, featuring vibrant visuals and enhanced gameplay mechanics.


## ✨ Features

- **Dynamic Visuals**  
  Snake color evolves based on score with rainbow gradient effects
- **Special Food Types**  
  - 🟢 Green: +1 point  
  - 🔵 Blue: +2 points (rare, time-limited)  
  - 🟡 Gold: +5 points (epic, time-limited)
- **Dual Difficulty System**
  - 🟢 Easy Mode: Slower gameplay for beginners
  - 🔥 Hard Mode: Faster speed with competitive scoring 
- **Comprehensive Leaderboards**
  - 📊 Score, Time, and Date tracking
  - 🏆 Separate rankings for each difficulty
  - 🕒 Chronological performance history
- **Customizable**  
  Easily modify game settings via `constants.py`


## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Python-Snake-Game.git
   ```
2. **Install dependencies**:
   ```bash
   pip install pygame
   ```
3. **Run the game**:
   ```bash
   python main.py
   ```

## 🎮 Controls

| Key          | Action           |
|--------------|------------------|
| ↑ ↓ ← →      | Move snake       |
| `P`          | Pause game       |
| Click `⏸️`   | Pause (button)   |
| `Q`          | Quit (game over) |
| `C`          | Continue (retry) |

## 📂 Project Structure

```
.
├── game.py            # Main game logic
├── constants.py       # Game settings & colors
├── buttons.py         # Pause button UI
├── food.py            # Food generation system
├── snake.py           # Snake behavior
├── ui.py              # All display rendering
├── utils.py           # Score saving utilities
└── assets/            # (Optional) For sound/graphics
```

## 🧑💻 Development

Want to contribute? Here are ideas:
- Add sound effects
- Add power-up items
- Create obstacle system
- Add multiplayer mode

Submit a pull request!

