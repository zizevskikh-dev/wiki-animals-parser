from typing import List

import pandas as pd
from loguru import logger


class DataStructurer:
    """
    Groups a list of animal names by their first letter using pandas.

    This class takes a list of "animal names" and returns a grouped DataFrame
    showing how many unique animals start with each letter of the alphabet.

    Example:
        Input:
            ["Python europaeus", "Hydrochoerinae", "Python kyaiktiyo"]

        Output:
            first_letter  count
            H             1
            P             2
    """

    def __init__(self, data: List[str]) -> None:
        """
        Initializes the DataStructurer with a list of animal names.

        Args:
            data (List[str]): List of animal names.
        """
        self.animal_names = data

        logger.debug("DataStructurer initialized.")

    def group_animals_by_first_letter(self) -> pd.DataFrame:
        """
        Groups animal names by their capitalized first letter and counts unique entries.

        Steps:
            - Capitalizes names for consistency.
            - Removes duplicates.
            - Extracts the first character.
            - Counts how many names start with each letter.

        Returns:
            pd.DataFrame: DataFrame with two columns:
                - first_letter (str): Uppercase first letter of the animal name.
                - count (int): Number of unique names that start with this letter.
        """
        logger.info("Grouping animal names by initial letter...")

        if not self.animal_names:
            logger.warning("No animal names provided. Returning empty DataFrame.")
            return pd.DataFrame(columns=["first_letter", "count"])

        unique_names = pd.Series(self.animal_names).str.capitalize().drop_duplicates()
        first_letters = unique_names.str[0]

        grouped_df = (
            first_letters.value_counts()
            .rename_axis("first_letter")
            .reset_index(name="count")
            .sort_values(by="first_letter")
        )

        logger.info(f"Grouping finished. Found {len(grouped_df)} unique first letters.")

        return grouped_df
