# pygame-platformer

A small side-scrolling platformer prototype built with Pygame. It includes tilemap loading, gravity, jumping, platform collision, and a camera that follows the player across the level.

## Features

- Tile-based level loaded from a map file
- Horizontal movement with gravity and jump physics
- Platform collision handling
- Camera scrolling with level bounds
- Simple prototype-friendly structure

## Tech Stack

- Python
- Pygame

## Local Setup

1. Install dependencies.

```bash
pip install -r requirements.txt
```

2. Run the game.

```bash
python src/main.py
```

## Project Structure

```text
.
├── assets/
├── README.md
├── requirements.txt
└── src/
	└── main.py
```

## Notes

- The game is currently a prototype, so it is intentionally minimal.
- Good next steps are enemies, collectibles, a title screen, and a win or lose state.
