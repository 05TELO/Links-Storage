from typing import Any
from typing import Dict

import requests
from bs4 import BeautifulSoup


class ParserOG:
    """
    Util class to parse Open Graph (OG) data from HTML content.
    """

    @classmethod
    def _fetch_html_data(cls, link: str) -> bytes:
        """
        Fetch HTML content from the provided link.

        :param link: The URL from which to fetch the HTML content.
        :type link: str

        :returns: HTML content in bytes format.
        :rtype: bytes
        """
        try:
            response = requests.get(link)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise e

    @classmethod
    def _parse_og(cls, html_content: bytes, link: str) -> Dict[str, Any]:
        """
        Parse Open Graph data from HTML content.

        :param html_content: HTML content in bytes format.
        :type html_content: bytes

        :param link: The URL for which the Open Graph data is parsed.
        :type link: str

        :returns: A dictionary containing parsed Open Graph data.
        :rtype: Dict[str, Any]
        """
        soup = BeautifulSoup(html_content, "html.parser")
        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_url = soup.find("meta", property="og:url")
        og_image = soup.find("meta", property="og:image")
        og_type = soup.find("meta", property="og:type")
        data = {
            "title": og_title.get("content"),
            "description": og_description.get("content"),
            "url": og_url.get("content"),
            "image": og_image.get("content"),
            "link_type": og_type.get("content").split(".")[0] if og_type else "website",
        }
        if not data["title"]:
            title_tag = soup.find("title")
            data["title"] = title_tag.text.strip()

        if not data["description"]:
            description_tag = soup.find("meta", attrs={"name": "description"})
            data["description"] = description_tag.text.strip()

        if not data["url"]:
            data["url"] = link

        return data

    @classmethod
    def extract_data_from_html(cls, link: str) -> Dict[str, Any]:
        """
        Extract Open Graph data from the provided URL link.

        :param link: The URL from which to extract Open Graph data.
        :type link: str

        :returns: A dictionary containing extracted Open Graph data.
        :rtype: Dict[str, Any]
        """
        html_content = cls._fetch_html_data(link)
        data = cls._parse_og(html_content, link)
        return data
