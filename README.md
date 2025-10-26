## Kaun Banega Crorepati - Python Edition

A terminal-based quiz game inspired by "Kaun Banega Crorepati (KBC)" implemented in Python. The project demonstrates simple modular design, object-oriented programming, and CSV-driven question loading, and makes use of tuples, lists, loops, and random module.

---

## Project structure

- `main.py` - Handles user interaction, restart logic, checkpoints, and runs the game loop.
- `kbc_module.py` - Contains the `Question` class, `KBCGame` class (game logic and player state), and `load_questions_from_csv` function to load questions from a CSV file. Also provides `save_score_to_csv` to log results.
- `questions.csv` - The question bank (CSV) used by the game. Each row represents one question and its options.

---

## Requirements

- Python 3.8+ (should work on 3.7 as well but 3.8+ recommended).
- No external packages required (only standard library modules used).

---

## How it works (contract)

- Input: `questions.csv` (CSV file with question rows). The loader reads rows with the header: `id,category,question,a,b,c,d,answer`.
- Output: Interactive terminal quiz. Scores are appended to `scores.csv`.
- Error modes: missing `questions.csv` prints an error and exits gracefully. Malformed rows are skipped.

Edge cases considered:

- Not enough questions in a category raises an error when selecting a game.
- Malformed CSV rows are skipped (won't crash the loader).
- Scores file creation is handled with header insertion if missing.

---

## CSV format and sample

The CSV must have the following columns (header row):

`id,category,question,a,b,c,d,answer`

- `id` - a unique identifier for the question
- `category` - one of `hard`, `harder`, `hardest` (game picks 3/3/4 respectively)
- `question` - the question text
- `a`, `b`, `c`, `d` - option texts
- `answer` - one of `a`, `b`, `c`, or `d` (the correct option)

Example row:

```
H1,hard,Which river flows through the city of Paris?,Thames,Seine,Danube,Rhine,b
```

Note: The repository already contains a `questions.csv` sample with 10 `hard`, 10 `harder`, and 10 `hardest` questions.

---

## How to run (Windows PowerShell)

1. Open PowerShell in the project folder (where `main.py` sits).
2. Run:

```powershell
python main.py
```

The program will ask for your name and then start the quiz. Follow on-screen prompts to answer each question (enter `a`/`b`/`c`/`d`). You can quit at checkpoints and save your current winnings.

Scores are appended to `scores.csv` with columns: `player_name,winnings,timestamp`.

---

## Checkpoints and scoring

- The game uses prize levels and checkpoints. Prize values are defined in `kbc_module.py`.
- Checkpoints (safe amounts) occur at specific question numbers. If you answer incorrectly past a checkpoint, you fall back to the last passed checkpoint amount.

Default checkpoints configured in the code (can be changed in `kbc_module.py`):

- Question 4 -> ₹10,000
- Question 7 -> ₹100,000
- Question 10 -> Jackpot amount (the file uses a large amount by default)

---

## Notes on recent small fixes

While creating documentation I ran a quick code check and made small, low-risk fixes to `kbc_module.py` so the project runs as intended:

- Added a missing `import os` used by the score-saving routine.
- Replaced a mistaken call to `required_items()` with `required.items()` in question selection.
- Moved the `load_questions_from_csv` function to module level so `from kbc_module import load_questions_from_csv` works correctly with `main.py`.

These changes are minimal and intended to restore the intended behavior.

---

## Troubleshooting

- If `python main.py` prints "No questions loaded", ensure `questions.csv` exists in the same folder and the header matches (`id,category,question,a,b,c,d,answer`).
- If you see `Not enough <category> questions`, check `questions.csv` contains at least 3 `hard`, 3 `harder`, and 4 `hardest` rows.
- If `scores.csv` cannot be written, check file permissions in the project folder.

---

## Extending the game

- Add more questions to `questions.csv` using the same header/format.
- Modify `KBCGame` in `kbc_module.py` to change prize levels, checkpoint locations, or selection rules.
- Add lifelines or time limits by extending `KBCGame.ask_question` and adjusting `main.py` flow.

---

## License

This project is provided as-is. Feel free to fork and adapt for educational use.
