# Memory Scramble Game

A simple memory matching game developed using Python and Tkinter. The player flips cards to reveal symbols and attempts to match all pairs before the timer expires.


## Game Features

- Adjustable board dimensions (rows × columns)
- Configurable game timer
- Randomized card distribution
- Matching-pair gameplay
- Countdown timer display
- Win and Game Over messages
- Restart and replay support

## Requirements

- Python 3.7 or later
- Tkinter library (included with most Python installations)

No additional dependencies are needed.

## Running the Game

### Clone the Repository

git clone https://github.com/mostafakamal225/memory-scramble-game.git
cd memory-scramble

### Check Python Version

python --version

### Start the Game

python main.py

## Gameplay Instructions

1. Launch the application.
2. Enter the desired number of rows and columns.
3. Specify the game time limit.
4. Start the game.
5. Select two cards to reveal their symbols.
6. Matching cards remain visible.
7. Non-matching cards flip back after a short delay.
8. Match all pairs before the timer reaches zero.

## Project Structure

memory-scramble/
├── main.py
├── game/
│   ├── __init__.py
│   ├── board.py
│   ├── config_dialog.py
│   ├── timer.py
│   └── ui.py
├── README.md
└── .gitignore

## Development Notes

- The project was developed collaboratively using Git and GitHub.
- Feature branches and incremental commits were used during development.
- The repository includes the full source code and execution instructions.

## License

This project was created for educational purposes as part of the Software Construction Tools course.