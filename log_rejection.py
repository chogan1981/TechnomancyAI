from core.logger import CentralizedLogger

logger = CentralizedLogger()

def log_rejection(message):
    logger.log_warning(f"Rejection: {message}")
