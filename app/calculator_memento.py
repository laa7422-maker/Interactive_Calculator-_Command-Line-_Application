from dataclasses import dataclass, field
from typing import List

from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    history: List[Calculation] = field(default_factory=list)

    @classmethod
    def save(cls, history):
        return cls(history=list(history))

    def restore(self):
        return list(self.history)
