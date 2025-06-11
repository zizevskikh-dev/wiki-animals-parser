from pathlib import Path
from typing import Union

import pandas as pd
from loguru import logger


class CSVReportWriter:
    """
    Writes a pandas DataFrame to a CSV file in the specified directory.
    Automatically ensures uniqueness of the output filename to prevent overwriting.
    """

    def __init__(self, report_dir: Union[Path, str], report_filename: str) -> None:
        """
        Initializes the CSVReportWriter.

        Args:
            report_dir (Union[Path, str]): Directory where the CSV report will be saved.
            report_filename (str): Base name of the CSV file (without extension).
        """
        self.report_dir: Path = Path(report_dir)
        self.report_filename: str = report_filename
        self.output_file_path: Path = self.report_dir / f"{self.report_filename}.csv"

        logger.debug("CSVReportWriter initialized.")

    def _generate_unique_file_path(self, counter: int):
        """
        Generates a unique file path to avoid overwriting existing CSV reports.

        Args:
            counter (int): Starting counter for uniqueness suffix. Defaults to 1.
        """
        self.report_dir.mkdir(parents=True, exist_ok=True)

        while self.output_file_path.exists():
            self.output_file_path = (
                self.report_dir / f"{self.report_filename}({counter}).csv"
            )
            counter += 1

    def write(self, df: pd.DataFrame, include_index: bool = False) -> None:
        """
        Writes the provided DataFrame to a uniquely named CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to write to the CSV file.
            include_index (bool): Whether to include the DataFrame index in the CSV output.
        """
        if df.empty:
            logger.warning(
                "Provided DataFrame is empty. CSV report will not be written."
            )
            return

        self._generate_unique_file_path(counter=1)
        logger.info(f"Generating report...")
        df.to_csv(
            path_or_buf=self.output_file_path,
            encoding="utf-8",
            index=include_index,
            header=False,
        )
        logger.info(f"Report saved to: {self.output_file_path}")
