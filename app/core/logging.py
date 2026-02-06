import logging
import sys
from loguru import logger
from app.core.config import settings

class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    """
    Configures the logging for the application.
    Intercepts standard logging and routes it through Loguru.
    """
    # Remove all existing handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
        logging.getLogger(name).setLevel(logging.INFO)

    # Configure Loguru
    logger.remove()  # Remove default handler
    
    # Add console handler
    logger.add(
        sys.stderr,
        level="DEBUG" if settings.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Add file handler (JSON for easier parsing in production)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 month",
        level="INFO",
        compression="zip",
        serialize=True,  # JSON format
    )

    logger.info("Logging configured successfully")
