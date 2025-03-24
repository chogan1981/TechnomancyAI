from core.logger import CentralizedLogger

logger = CentralizedLogger()

class CustomFileNotFound(Exception):
    pass

class CustomPermissionError(Exception):
    pass

class APIError(Exception):
    pass

def handle_exception(e):
    if isinstance(e, CustomFileNotFound):
        logger.log_error(f"File not found: {str(e)}. Please check the file path.")
    elif isinstance(e, CustomPermissionError):
        logger.log_error(f"Permission denied: {str(e)}. Please check your access rights.")
    elif isinstance(e, APIError):
        logger.log_error(f"API error occurred: {str(e)}. Please check the API endpoint.")
    else:
        logger.log_error(f"An unexpected error occurred: {str(e)}")

def log_with_context(e, context):
    logger.log_error(f"Error in {context}: {str(e)}", include_trace=True)