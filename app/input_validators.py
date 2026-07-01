from decimal import Decimal, InvalidOperation

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


class InputValidator:
    @staticmethod
    def validate_number(value, config: CalculatorConfig) -> Decimal:
        try:
            number = Decimal(str(value).strip())
        except (InvalidOperation, ValueError, AttributeError) as exc:
            raise ValidationError(f"Invalid number: {value!r}") from exc
        if abs(number) > Decimal(str(config.max_input_value)):
            raise ValidationError(f"Value {number} exceeds maximum ({config.max_input_value}).")
        return number
