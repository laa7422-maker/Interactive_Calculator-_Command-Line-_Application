from abc import ABC, abstractmethod
from decimal import Decimal

from app.exceptions import OperationError, ValidationError


class Operation(ABC):
    name = "operation"

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        raise NotImplementedError

    def __str__(self):
        return self.name


class Addition(Operation):
    name = "add"
    def execute(self, a, b): return a + b


class Subtraction(Operation):
    name = "subtract"
    def execute(self, a, b): return a - b


class Multiplication(Operation):
    name = "multiply"
    def execute(self, a, b): return a * b


class Division(Operation):
    name = "divide"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Division by zero is not allowed.")
        return a / b


class Power(Operation):
    name = "power"
    def execute(self, a, b):
        try:
            return Decimal(str(float(a) ** float(b)))
        except (ValueError, OverflowError) as exc:
            raise OperationError(f"Cannot compute power: {exc}") from exc


class Root(Operation):
    name = "root"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Zeroth root is undefined.")
        if a < 0 and float(b) % 2 == 0:
            raise OperationError("Cannot take even root of a negative number.")
        try:
            return Decimal(str(float(a) ** (1.0 / float(b))))
        except (ValueError, OverflowError) as exc:
            raise OperationError(f"Cannot compute root: {exc}") from exc


class Modulus(Operation):
    name = "modulus"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Modulus by zero is not allowed.")
        return a % b


class IntegerDivision(Operation):
    name = "int_divide"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Integer division by zero is not allowed.")
        return a // b


class Percentage(Operation):
    name = "percent"
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot compute percentage with zero denominator.")
        return (a / b) * Decimal("100")


class AbsoluteDifference(Operation):
    name = "abs_diff"
    def execute(self, a, b): return abs(a - b)


class OperationFactory:
    _operations = {
        "add": Addition, "subtract": Subtraction, "multiply": Multiplication,
        "divide": Division, "power": Power, "root": Root, "modulus": Modulus,
        "int_divide": IntegerDivision, "percent": Percentage, "abs_diff": AbsoluteDifference,
    }

    @classmethod
    def create(cls, name):
        op = cls._operations.get(name.lower())
        if op is None:
            raise ValidationError(f"Unknown operation: {name!r}")
        return op()

    @classmethod
    def available_operations(cls):
        return list(cls._operations.keys())
