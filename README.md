# Interactive Calculator — Command-Line Application

A command-line calculator built in Python that supports a range of arithmetic operations, calculation history with undo/redo, logging, and CSV persistence. It's built using several classic design patterns (Factory, Memento, Observer, Command, and Decorator) and runs as an interactive REPL.

## Features

- **Operations:** add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
- **Undo / redo** using the Memento pattern
- **Automatic logging** and **CSV auto-save** using the Observer pattern
- **History management** — view, clear, save, and load past calculations
- **Color-coded output** for a better terminal experience (colorama)
- **Robust error handling** with custom exceptions and input validation

## Installation

Clone the repository:

```bash
git clone https://github.com/laa7422-maker/Interactive_Calculator-_Command-Line-_Application.git
cd Interactive_Calculator-_Command-Line-_Application
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The application loads settings from a `.env` file at startup via `python-dotenv`. All variables are optional — if omitted, the defaults below are used. Copy `.env.example` to `.env` to get started.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CALCULATOR_LOG_DIR` | path | `logs` | Directory where log files are written. Created automatically if missing. |
| `CALCULATOR_HISTORY_DIR` | path | `history` | Directory where the CSV calculation history is persisted. |
| `CALCULATOR_MAX_HISTORY_SIZE` | int | `1000` | Maximum number of calculations retained in memory/history. |
| `CALCULATOR_AUTO_SAVE` | bool | `true` | If true, history is written to CSV automatically after each operation. |
| `CALCULATOR_PRECISION` | int | `10` | Number of decimal places results are rounded to. |
| `CALCULATOR_MAX_INPUT_VALUE` | number | `1e12` | Rejects operands whose absolute value exceeds this limit (input validation). |
| `CALCULATOR_DEFAULT_ENCODING` | string | `utf-8` | Encoding used when reading/writing log and CSV files. |

### Example `.env`

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e12
CALCULATOR_DEFAULT_ENCODING=utf-8
```

> **Note:** Booleans accept `true`/`false`, `1`/`0`, or `yes`/`no` (case-insensitive). Invalid values raise a `ConfigurationError` at startup.

## Usage

Start the calculator:

```bash
python main.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| `add`, `subtract`, `multiply`, `divide` | Basic arithmetic operations |
| `power`, `root`, `modulus`, `int_divide`, `percent`, `abs_diff` | Advanced operations |
| `history` | Display the calculation history |
| `clear` | Clear the calculation history |
| `undo` | Undo the last calculation |
| `redo` | Redo the last undone calculation |
| `save` | Manually save history to a CSV file |
| `load` | Load history from a CSV file |
| `help` | Display all available commands |
| `exit` | Exit the application gracefully |

Each operation prompts for two numbers, then displays the result. Invalid input (non-numeric values, division by zero, out-of-range numbers) is caught and reported with a clear error message instead of crashing.

## Testing

Run the full test suite with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

The project enforces a minimum of 90% test coverage. The `--cov-report=term-missing` flag lists any lines not covered by tests.

## CI/CD

This project uses GitHub Actions (`.github/workflows/python-app.yml`). On every push or pull request to `main`, the workflow automatically:

1. Checks out the code
2. Sets up the Python environment
3. Installs dependencies from `requirements.txt`
4. Runs the test suite with `pytest` and enforces 90% coverage

The build fails automatically if test coverage drops below 90%, ensuring code quality is maintained on every change.
