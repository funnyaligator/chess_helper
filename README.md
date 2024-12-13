
# Chess Bot for Lichess

This Python project automates playing chess on Lichess (https://lichess.org) using Selenium and the Stockfish chess engine. It observes the game, computes the best moves using Stockfish, and visually overlays the suggestions on the chessboard.

## Features
- Automates game interaction by detecting moves and player colors.
- Uses the Stockfish chess engine to calculate the best moves.
- Draws suggestions directly on the chessboard.
- Utilizes multithreading for smooth operation.

## Requirements
- Python 3.10+
- Selenium
- Stockfish executable
- Chromium browser and ChromeDriver

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/chess-bot.git
   cd chess-bot
   ```

2. Install required Python libraries:
   ```bash
   pip install selenium chess stockfish
   ```

3. Download the Stockfish engine:
   - Visit Stockfish Download (https://stockfishchess.org/download/) and download the executable for your system.
   - Update the Stockfish path in the script:
     ```python
     stockfish_process = Popen(['/path/to/stockfish'], stdin=PIPE, stdout=PIPE)
     ```

4. Set up Chromium and ChromeDriver:
   - Ensure you have Chromium installed.
   - Update the `chrome_options.binary_location` in the code if needed:
     ```python
     chrome_options.binary_location = "/path/to/chromium"
     ```

5. Verify ChromeDriver compatibility with your Chromium version.

## Usage

1. Run the script:
   ```bash
   python chess_bot.py
   ```

2. The bot will:
   - Open Lichess in Chromium.
   - Wait for you to start a game.
   - Analyze moves and suggest the best responses.

3. Follow the suggestions drawn on the board and enjoy better gameplay!

## Code Overview

- `raw_to_uci(driver)`: Extracts current game moves in UCI format.
- `get_color(chessboard)`: Determines whether you play as white or black.
- `get_fen(moves)`: Converts moves into FEN notation.
- `get_best_move(fen)`: Queries Stockfish to get the best move.
- `draw_canvas()`: Adds a canvas overlay to show move suggestions.
- `play_game()`: Monitors moves, computes responses, and updates the board.

## Contributing

Feel free to fork the project, create a branch, and submit a pull request!
