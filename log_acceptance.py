from core.logger import CentralizedLogger

logger = CentralizedLogger()

def log_acceptance(message):
    logger.log_info(f"Acceptance: {message}")
