import logging
from config.app import Settings

# Define ANSI color codes
COLOR_CODES = {
    'DEBUG': '\033[94m',  # Blue
    'INFO': '\033[92m',  # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',  # Red
    'CRITICAL': '\033[41m',  # Red background
    'RESET': '\033[0m'  # Reset to default
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # Map the log level to a color
        level_color = COLOR_CODES.get(record.levelname, COLOR_CODES['RESET'])
        # Format the message with the color and reset code
        message = super().format(record)
        return f"{level_color}{message}{COLOR_CODES['RESET']}"


def setup_logger():
    logger = logging.getLogger()

    # Determine the logging level based on settings
    debug_enabled = Settings().get_setting('debug')
    logger.setLevel(logging.DEBUG if debug_enabled else logging.INFO)

    # Create a console handler
    handler = logging.StreamHandler()

    # Define the log format with dynamic timestamp
    formatter = ColoredFormatter('%(asctime)s - %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # Add the handler to the logger if not already added
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
