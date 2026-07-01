import logging

from app.calculator_config import CalculatorConfig


class Logger:
    def __init__(self, config: CalculatorConfig):
        self.config = config
        self._logger = logging.getLogger("calculator")
        self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            handler = logging.FileHandler(config.log_file, encoding=config.default_encoding)
            handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
            self._logger.addHandler(handler)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)
