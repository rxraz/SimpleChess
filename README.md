# Simple Chess

A two-player chess game built with [Pygame](https://www.pygame.org/). Both players
share the same keyboard and mouse on one computer; there is no computer opponent.

The board is drawn on the left, captured pieces are listed on the right, and the
current turn is shown in the status bar at the bottom. Piece images are downloaded
from the internet the first time the game starts.

## Features

- Full turn-based movement for all six piece types.
- Legal-move highlighting: only moves that keep your own king safe are shown.
- Check detection, with a flashing square around a king that is in check.
- Castling (king-side and queen-side) with correct rights tracking.
- Checkmate and stalemate detection, with a winner/draw message.
- Captured-piece display for both sides.
- Resign button.

## Requirements

- **Python 3.9** or newer.
- **Pygame** — window, rendering, and input.
- **Requests** — downloads the piece images.
- An **internet connection** on the first run (images are fetched from GitHub).
- The font file `freesansbold.ttf` must be available to Pygame (see
  [Troubleshooting](#troubleshooting)).

## Installation

It is recommended to install the dependencies inside a virtual environment.

### macOS / Linux

```bash
cd /path/to/SImpleChess

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pygame requests
```

### Windows (PowerShell)

```powershell
cd C:\path\to\SImpleChess

py -m venv .venv
.venv\Scripts\Activate.ps1

py -m pip install --upgrade pip
py -m pip install pygame requests
```

If you prefer, you can install the dependencies globally instead:

```bash
python -m pip install pygame requests
```

## Running the game

From the project directory:

```bash
python main.py
```

On macOS/Linux you may need `python3 main.py` instead of `python main.py`.

A window titled **Chess Game** opens. White moves first.

## How to play

1. **Select a piece** — click one of your own pieces. The square is outlined
   (red for White, blue for Black) and small dots mark its legal destinations.
2. **Move** — click one of the highlighted destination squares. The move is played
   and the turn passes to the other player.
3. **Capture** — move onto an enemy piece's square; the captured piece appears in
   the side panel.
4. **Castle** — select the king and click the highlighted castling square
   (two squares toward the rook). Castling is only available when neither the
   king nor the rook has moved, the path is clear, and the king is not in check.
5. **Resign** — click the **RESIGN** button in the bottom-right corner. The other
   player wins.
6. **Restart** — after a checkmate, stalemate, or resignation, press **Enter** to
   start a new game.

### Board layout

- White starts at the bottom of the board; Black starts at the top.
- White pieces are selected and moved on White's turn; Black pieces on Black's turn.
- The status bar reads either "Select A Piece To Move" or "Select A Destination"
  for whichever side is currently playing.

## Rules implemented

- Standard movement for pawns, knights, bishops, rooks, queens, and kings.
- Pawns move one square forward, two squares from their starting rank, and capture
  diagonally.
- You may not make a move that leaves your own king in check.
- Castling is supported with the usual restrictions.
- A player with no legal moves loses if their king is in check (checkmate) or
  draws if it is not (stalemate).

## Known limitations

- **No pawn promotion** — pawns that reach the last rank cannot move further.
- **No en passant.**
- **No draw by repetition or the fifty-move rule** (only stalemate is detected as
  a draw).
- **No undo, move history, or save/load.**
- The game is local two-player only; there is no AI opponent.

## Troubleshooting

**`ModuleNotFoundError: No module named 'pygame'` or `'requests'`**
The dependencies are not installed in the interpreter you are running. Activate
your virtual environment and re-run the install commands.

**Font error mentioning `freesansbold.ttf`**
The game requests that font by name. Either copy `freesansbold.ttf` into the
project directory, or use Pygame's built-in font by replacing the font lines in
`main.py` with:

```python
font = pygame.font.Font(None, 20)
medium_font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 50)
```

**Blank window or missing piece images**
The piece images are downloaded from GitHub at startup. Check your internet
connection, and make sure `requests` is installed. Restart the game after
connecting.

**Nothing happens when you click**
Click directly on a piece square to select it, then click on one of the marked
destination squares. You cannot select the opponent's pieces.

## Project structure

```
SImpleChess/
├── main.py        # Game logic, rendering, and the main loop
├── pyproject.toml # Project metadata
├── README.md
├── src/           # Reserved Python package
└── tests/         # Test package (currently empty)
```

## Credits

The Pygame setup and rendering follow the Pygame documentation and a chess-in-
Pygame tutorial. The move logic was written by the author; the castling and
checkmate logic was adapted from publicly available examples.
