import pytest
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from main import CalculatorREPL


@pytest.fixture
def repl(tmp_path):
    cfg = CalculatorConfig(log_dir=tmp_path / "l", history_dir=tmp_path / "h", auto_save=False)
    return CalculatorREPL(Calculator(cfg))


def test_add(repl): assert "5" in repl.evaluate("add 2 3")
def test_bad_args(repl): assert "requires exactly two" in repl.evaluate("add 2")
def test_unknown(repl): assert "Unknown command" in repl.evaluate("foo 1 2")
def test_empty(repl): assert repl.evaluate("") == ""
def test_hist_empty(repl): assert "empty" in repl.evaluate("history")


def test_hist_full(repl):
    repl.evaluate("add 1 1")
    assert "add(1, 1)" in repl.evaluate("history")


def test_clear(repl):
    repl.evaluate("add 1 1")
    repl.evaluate("clear")
    assert "empty" in repl.evaluate("history")


def test_undo_redo(repl):
    repl.evaluate("add 1 1")
    assert "Undo successful" in repl.evaluate("undo")
    assert "Redo successful" in repl.evaluate("redo")


def test_nothing(repl):
    assert "Nothing to undo" in repl.evaluate("undo")
    assert "Nothing to redo" in repl.evaluate("redo")


def test_save_load(repl):
    repl.evaluate("add 2 3")
    assert "saved" in repl.evaluate("save")
    assert "loaded" in repl.evaluate("load")


def test_load_fail(repl): assert "not found" in repl.evaluate("load")


def test_help(repl):
    o = repl.evaluate("help")
    assert "add" in o and "history" in o and "exit" in o


def test_exit(repl):
    repl.evaluate("exit")
    assert repl.running is False


def test_div_err(repl): assert "Error" in repl.evaluate("divide 1 0")
