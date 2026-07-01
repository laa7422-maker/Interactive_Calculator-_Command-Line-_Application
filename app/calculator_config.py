import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

load_dotenv()


def _get_bool(key, default):
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


@dataclass
class CalculatorConfig:
    log_dir: Path = field(default_factory=lambda: Path(os.getenv("CALCULATOR_LOG_DIR", "logs")))
    history_dir: Path = field(default_factory=lambda: Path(os.getenv("CALCULATOR_HISTORY_DIR", "history")))
    max_history_size: int = field(default_factory=lambda: int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000")))
    auto_save: bool = field(default_factory=lambda: _get_bool("CALCULATOR_AUTO_SAVE", True))
    precision: int = field(default_factory=lambda: int(os.getenv("CALCULATOR_PRECISION", "10")))
    max_input_value: float = field(default_factory=lambda: float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e12")))
    default_encoding: str = field(default_factory=lambda: os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8"))

    def __post_init__(self):
        self.validate()
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    @property
    def log_file(self):
        return self.log_dir / "calculator.log"

    @property
    def history_file(self):
        return self.history_dir / "calculator_history.csv"

    def validate(self):
        if self.max_history_size <= 0:
            raise ConfigurationError("CALCULATOR_MAX_HISTORY_SIZE must be positive.")
        if self.precision < 0:
            raise ConfigurationError("CALCULATOR_PRECISION must be non-negative.")
        if self.max_input_value <= 0:
            raise ConfigurationError("CALCULATOR_MAX_INPUT_VALUE must be positive.")
