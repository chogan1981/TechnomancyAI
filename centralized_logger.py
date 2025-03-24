class CentralizedLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CentralizedLogger, cls).__new__(cls)
            cls._instance.initialize_logger()
        return cls._instance

    def initialize_logger(self):
        import logging
        self.logger = logging.getLogger("CentralizedLogger")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)