import logging
import os

def setup_logger() -> None:
    """Configure the application-wide logger to write to logs/app.log."""
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename=os.path.join("logs", "app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def info(msg: str) -> None:
    """Log an informational message."""
    logging.info(msg)

def warning(msg: str) -> None:
    """Log a warning message."""
    logging.warning(msg)

def error(msg: str) -> None:
    """Log an error message."""
    logging.error(msg)

def debug(msg: str) -> None:
    """Log a debug message."""
    logging.debug(msg)