from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.operations import OperationFactory


@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.result = OperationFactory.create(self.operation).execute(self.operand1, self.operand2)

    def to_dict(self):
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "result": str(self.result),
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data):
        calc = Calculation(data["operation"], Decimal(str(data["operand1"])), Decimal(str(data["operand2"])))
        calc.timestamp = datetime.fromisoformat(str(data["timestamp"]))
        calc.result = Decimal(str(data["result"]))
        return calc

    def __str__(self):
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"
