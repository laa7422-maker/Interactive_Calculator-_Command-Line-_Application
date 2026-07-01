from decimal import Decimal
from typing import List

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError
from app.history import AutoSaveObserver, HistoryObserver, LoggingObserver, history_to_dataframe
from app.input_validators import InputValidator
from app.logger import Logger
from app.operations import OperationFactory


class Calculator:
    def __init__(self, config: CalculatorConfig = None):
        self.config = config or CalculatorConfig()
        self.logger = Logger(self.config)
        self.history: List[Calculation] = []
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
        self._observers: List[HistoryObserver] = []
        self.add_observer(LoggingObserver(self.logger))
        self.add_observer(AutoSaveObserver(self))
        self.logger.info("Calculator initialized.")

    def add_observer(self, observer):
        self._observers.append(observer)

    def _notify(self, calc):
        for o in self._observers:
            o.update(calc)

    def perform_operation(self, operation, a, b):
        op1 = InputValidator.validate_number(a, self.config)
        op2 = InputValidator.validate_number(b, self.config)
        OperationFactory.create(operation)
        self._undo_stack.append(CalculatorMemento.save(self.history))
        self._redo_stack.clear()
        calc = Calculation(operation, op1, op2)
        self.history.append(calc)
        if len(self.history) > self.config.max_history_size:
            self.history.pop(0)
        self._notify(calc)
        return calc.result

    def undo(self):
        if not self._undo_stack:
            return False
        self._redo_stack.append(CalculatorMemento.save(self.history))
        self.history = self._undo_stack.pop().restore()
        self.logger.info("Undo performed.")
        return True

    def redo(self):
        if not self._redo_stack:
            return False
        self._undo_stack.append(CalculatorMemento.save(self.history))
        self.history = self._redo_stack.pop().restore()
        self.logger.info("Redo performed.")
        return True

    def clear_history(self):
        self._undo_stack.append(CalculatorMemento.save(self.history))
        self._redo_stack.clear()
        self.history.clear()
        self.logger.info("History cleared.")

    def get_history(self):
        return list(self.history)

    def save_history(self):
        try:
            history_to_dataframe(self.history).to_csv(
                self.config.history_file, index=False, encoding=self.config.default_encoding)
            self.logger.info(f"History saved to {self.config.history_file}.")
        except OSError as exc:
            self.logger.error(f"Save failed: {exc}")
            raise OperationError(f"Could not save history: {exc}") from exc

    def load_history(self):
        path = self.config.history_file
        if not path.exists():
            self.logger.warning("No history file found.")
            raise OperationError(f"History file not found: {path}")
        try:
            df = pd.read_csv(path, encoding=self.config.default_encoding)
            self.history = [] if df.empty else [Calculation.from_dict(r) for r in df.to_dict("records")]
            self.logger.info(f"History loaded from {path}.")
        except (pd.errors.ParserError, pd.errors.EmptyDataError, KeyError) as exc:
            self.logger.error(f"Malformed history: {exc}")
            raise OperationError(f"Could not load history: {exc}") from exc
