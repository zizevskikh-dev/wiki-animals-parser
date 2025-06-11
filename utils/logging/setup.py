import sys
from pathlib import Path
from typing import Union

from loguru import logger


class LoggerConfigurator:
    """
    Sets up structured logging using the loguru library with file rotation and dual output.

    Logging strategy:
        - DEBUG and above messages go to a compressed, rotating log file.
        - INFO and SUCCESS messages appear in the console for real-time feedback.
    """

    def __init__(self, log_file: Union[str, Path]) -> None:
        """
        Initializes the logger configuration.

        Args:
            log_file (Union[str, Path]): Path to the file where logs will be written.
        """
        self.log_file = log_file

    def setup_logger(self) -> None:
        """
        Configures the logger with two sinks:

            1. File Sink:
                - Level: DEBUG and above
                - Rotation: After 10 MB
                - Retention: Last 10 log files
                - Compression: zip
                - Encoding: UTF-8
                - Format: Timestamp | Level | Line | Function | Elapsed | Message

            2. Console Sink:
                - Levels: INFO and SUCCESS only
                - Output: Colored and simplified message format
        """
        logger.remove()

        # File output
        logger.add(
            sink=self.log_file,
            level="DEBUG",
            rotation="10 MB",
            retention=10,
            compression="zip",
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {line}: {function} | {elapsed} | {message}",
        )

        # Console output
        logger.add(
            sink=sys.stdout,
            filter=lambda record: record["level"].name in ["INFO", "SUCCESS"],
            format="<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> | <green>{level}</green> | {message}",
        )

        logger.debug(f"Logger initialized with log file: {self.log_file}")
