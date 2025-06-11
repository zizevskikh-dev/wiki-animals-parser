from pathlib import Path
from typing import Dict, Optional

from dotenv import dotenv_values


class Config:
    """
    Loads and stores project configuration variables from a `.env` file.

    Attributes:
        LOG_FILE (Path): Path to the log file.
        REPORT_DIR (Path): Directory where the CSV report will be stored.
        REPORT_FILENAME (str): Name of the CSV report file (without extension).
        BASE_URL (str): Base URL of the target website (Wikipedia).
        RELATIVE_URL (str): Relative path to the specific page for scraping.
    """

    def __init__(self) -> None:
        """
        Initializes the Config object and loads variables from a .env file.

        Raises:
            ValueError: If any required environment variables are missing or empty.
        """
        self._project_path: Path = Path(__file__).parents[1]

        self._env_path: Path = Path(self._project_path) / ".env"
        self._env: Dict[str, Optional[str]] = dotenv_values(dotenv_path=self._env_path)

        self.LOG_FILE: Path = Path(self._project_path) / self._env.get("LOG_FILE")
        self.REPORT_DIR: Path = Path(self._project_path) / self._env.get("REPORT_DIR")
        self.REPORT_FILENAME: str = self._env.get("REPORT_FILENAME")
        self.BASE_URL: str = self._env.get("BASE_URL")
        self.RELATIVE_URL: str = self._env.get("RELATIVE_URL")

        self._validate()

    def _validate(self) -> None:
        """
        Validates the loaded environment variables.

        Raises:
            ValueError: If any environment variables are missing or empty.
        """
        missing = [key for key, value in self._env.items() if not value]
        if missing:
            raise ValueError(f"Missing environment variables: {missing}")
