from abc import ABC, abstractmethod

import pandas as pd

from app.calculation import Calculation
from app.logger import Logger


class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation):
        raise NotImplementedError


class LoggingObserver(HistoryObserver):
    def __init__(self, logger: Logger):
        self.logger = logger

    def update(self, calculation):
        self.logger.info(
            f"Calculation: {calculation.operation}"
            f"({calculation.operand1}, {calculation.operand2}) = {calculation.result}"
        )


class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator):
        self.calculator = calculator

    def update(self, calculation):
        if self.calculator.config.auto_save:
            self.calculator.save_history()


def history_to_dataframe(history):
    if not history:
        return pd.DataFrame(columns=["operation", "operand1", "operand2", "result", "timestamp"])
    return pd.DataFrame([c.to_dict() for c in history])
