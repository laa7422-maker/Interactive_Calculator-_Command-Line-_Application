# Enhanced Calculator CLI

An advanced command-line calculator built with the Factory, Memento, Observer,
Command, and Decorator design patterns. Features undo/redo, logging, CSV
persistence (pandas), .env configuration, and CI via GitHub Actions.

## Features
- 10 operations: add, subtract, multiply, divide, power, root, modulus, int_divide, percent, abs_diff
- Undo / Redo (Memento pattern)
- Logging + Auto-Save observers (Observer pattern)
- Dynamic help menu (Decorator pattern)
- Color-coded output (Colorama)
- Command encapsulation (Command pattern)
- CSV history via pandas
- 90%+ test coverage enforced in CI

## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
