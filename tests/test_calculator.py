import pytest
from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


@pytest.fixture
def calc(tmp_path):
    cfg = CalculatorConfig(log_dir=tmp_path / "l", history_dir=tmp_path / "h",
                           max_history_size=5, auto_save=False)
    return Calculator(cfg)


def test_perform(calc):
    assert calc.perform_operation("add", "2", "3") == Decimal("5")
    assert len(calc.history) == 1


def test_bad_number(calc):
    with pytest.raises(ValidationError):
        calc.perform_operation("add", "abc", "3")


def test_too_big(calc):
    with pytest.raises(ValidationError):
        calc.perform_operation("add", "1e20", "1")


def test_unknown_op(calc):
    with pytest.raises(ValidationError):
        calc.perform_operation("xyz", "1", "2")


def test_div_zero(calc):
    with pytest.raises(OperationError):
        calc.perform_operation("divide", "1", "0")


def test_undo_redo(calc):
    calc.perform_operation("add", "1", "1")
    calc.perform_operation("add", "2", "2")
    assert calc.undo() is True
    assert len(calc.history) == 1
    assert calc.redo() is True
    assert len(calc.history) == 2


def test_undo_empty(calc):
    assert calc.undo() is False


def test_redo_empty(calc):
    assert calc.redo() is False


def test_clear(calc):
    calc.perform_operation("add", "1", "1")
    calc.clear_history()
    assert calc.get_history() == []


def test_max_size(calc):
    for i in range(10):
        calc.perform_operation("add", str(i), "1")
    assert len(calc.history) == 5


def test_save_load(calc):
    calc.perform_operation("add", "2", "3")
    calc.save_history()
    other = Calculator(calc.config)
    other.load_history()
    assert other.history[0].result == Decimal("5")


def test_load_missing(calc):
    with pytest.raises(OperationError):
        calc.load_history()
