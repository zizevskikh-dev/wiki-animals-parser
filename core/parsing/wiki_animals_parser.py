from urllib.parse import urljoin, unquote
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from loguru import logger


class WikiAnimalsParser:
    """
    Parses animal names from a paginated Wikipedia category page.

    The parser navigates through all linked pages via "Next page" links,
    extracting animal names from <li><a title=...> elements.
    """

    def __init__(self, base_url: str) -> None:
        """
        Initializes the parser with the base URL of the Wikipedia website.

        Args:
            base_url (str): The root URL (e.g., "https://ru.wikipedia.org/").
        """
        self.base_url: str = base_url
        self.animal_names: List[str] = []
        self.parsed_pages_count: int = 0

        logger.debug("WikiAnimalParser initialized.")

    def parse(self, relative_url: Optional[str]) -> List[str]:
        """
        Launches the recursive parsing process from the given relative URL.

        Follows pagination, extracts animals, and adds them in self.animal_names list.

        Args:
            relative_url (Optional[str]): A current relative URL to a category page.

        Returns:
            List[str]: A list of extracted animal names.
        """
        if self.parsed_pages_count == 0:
            logger.info("Starting parsing process...")

        full_url = urljoin(base=self.base_url, url=unquote(relative_url))
        soup = self._get_soup_object(url=full_url)

        li_elements = self._get_li_elements(soup)
        self._add_animals_to_data(li_elements)

        next_relative_url = self._get_next_relative_url(soup)
        if next_relative_url:
            self.parse(relative_url=next_relative_url)
        else:
            logger.warning(f"Next page not found. Finishing parsing process.")
            logger.info("Parsing process completed.")

        return self.animal_names

    @staticmethod
    def _get_soup_object(url: str) -> BeautifulSoup:
        """
        Fetches and parses an HTML page from the given URL.

        Args:
            url (str): Full URL to the target page.

        Returns:
            BeautifulSoup: Parsed HTML content.
        """
        logger.debug(f"Fetching URL: {url}")
        response = requests.get(url=url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")

    @staticmethod
    def _get_li_elements(soup: BeautifulSoup) -> ResultSet:
        """
        Extracts <li> elements into the <div> witch has the "mw-category.mw-category-columns" CSS class.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            ResultSet: Collection of <li> tags with animal links.
        """
        return soup.select(selector="div.mw-category.mw-category-columns li")

    @staticmethod
    def _get_next_relative_url(soup: BeautifulSoup) -> Optional[str]:
        """
        Finds the "Next page" link on the current page.

        Args:
            soup (BeautifulSoup): Parsed HTML content.
        Returns:
            Optional[str]: The relative URL to the "Next page" or None if not found.
        """
        next_relative_url = soup.find("a", string="Следующая страница", href=True)
        return next_relative_url.get("href") if next_relative_url else None

    def _add_animals_to_data(self, li_elements: ResultSet) -> None:
        """
        Adds animal names from the <li> tags to a self.animal_names list.

        Args:
            li_elements (ResultSet): <li> tags from category page.
        """
        for li in li_elements:
            if li.find("a", title=True):
                animal_name = li.a["title"]
                logger.debug(f"Found animal name: {animal_name}")
                self.animal_names.append(animal_name)

        self.parsed_pages_count += 1
        logger.info(f"Animal names collected: {len(self.animal_names)}")
        logger.debug(f"Pages parsed: {self.parsed_pages_count}")
