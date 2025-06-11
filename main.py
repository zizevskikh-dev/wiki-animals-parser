from loguru import logger

from core.config import Config
from core.data.data_structurer import DataStructurer
from core.parsing.wiki_animals_parser import WikiAnimalsParser
from core.reporting.report_writer import CSVReportWriter
from utils.logging.setup import LoggerConfigurator


def main() -> None:
    """
    Entry point for running the Wikipedia animal parser pipeline.

    Workflow:
        1. Load configuration from environment variables.
        2. Initialize and configure the logging system.
        3. Scrape animal names from a Wikipedia website.
        4. Group the names by their first letter.
        5. Write the grouped result into a uniquely named CSV report.

    Components:
        - LoggerConfigurator: Initializes file and console logging.
        - WikiAnimalParser: Scrapes data from Wikipedia.
        - DataStructurer: Groups animal names by their first letter.
        - CSVReportWriter: Writes results into a CSV file using automatic filename versioning
          to avoid overwriting existing reports (e.g., `report.csv`, `report(1).csv`, ...).
    """
    # Load environment configuration
    config = Config()

    # Setup logging
    LoggerConfigurator(log_file=config.LOG_FILE).setup_logger()

    # Scrape animal names from Wikipedia
    parser = WikiAnimalsParser(base_url=config.BASE_URL)
    animal_names = parser.parse(relative_url=config.RELATIVE_URL)

    # Group animals by their first letter
    structurer = DataStructurer(data=animal_names)
    grouped_animals = structurer.group_animals_by_first_letter()

    # Write a report to a CSV file
    report_writer = CSVReportWriter(
        report_dir=config.REPORT_DIR,
        report_filename=config.REPORT_FILENAME,
    )
    report_writer.write(df=grouped_animals)

    logger.success(f"Wiki Animal Parser completed successfully!")


if __name__ == "__main__":
    main()
