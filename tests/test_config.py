import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


def test_default(tmp_path):
    cfg = CalculatorConfig(log_dir=tmp_path / "l", history_dir=tmp_path / "h")
    assert cfg.log_file.name == "calculator.log"


@pytest.mark.parametrize("kwargs", [
    {"max_history_size": 0},
    {"precision": -1},
    {"max_input_value": 0},
])
def test_invalid(tmp_path, kwargs):
    with pytest.raises(ConfigurationError):
        CalculatorConfig(log_dir=tmp_path / "l", history_dir=tmp_path / "h", **kwargs)
