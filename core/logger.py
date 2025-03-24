import logging
from core.logger_interface import ILogger  # Add this import

class CentralizedLogger(ILogger):  # Inherit from ILogger
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CentralizedLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger("CentralizedLogger")
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    # ILogger interface methods
    def log_info(self, message: str):
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.warning(message)

    def log_error(self, message: str, include_trace: bool = False):
        if include_trace:
            self.logger.error(message, exc_info=True)
        else:
            self.logger.error(message)

    # Optional: passthrough for raw logger access
    def __getattr__(self, attr):
        return getattr(self.logger, attr)
