from typing import List
from requests import get
from bs4 import BeautifulSoup

from utils.url import get_domain
from config.config import config
from src.core.web_com import WebCom

class ExtractionData:
    def __init__(self,
                 url: List[str] = None,
                 file_name: str = ''
                ) -> None:
        self.url = url
        self.file_name = file_name
        self.data: List[List[str]] = []

    def validate_domain(self, url: str) -> bool:
        if config.VALID_DOMAINS.split(',').count(get_domain(url)) > 0:
            return True
        return False

    def _get_html_content(self, url: str) -> str:
        content = get(url, timeout=500).content
        return BeautifulSoup(content, features="html.parser")

    def execute(self) -> str:
        domain_allow = self.validate_domain(self.url)

        if domain_allow is False:
            print(f'{self.url} does not support to get data')
        else:
            html_content = self._get_html_content(self.url)
            webCom = WebCom(html_content)
            self.data = webCom.execute()

        return self.data
