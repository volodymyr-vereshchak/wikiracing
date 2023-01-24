from __future__ import annotations
import requests
from time import sleep
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import Base, Page, page_to_link
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from settings import (
    DATABASE_URL,
    BASE_URL,
    REQUESTS_PER_MINUTE,
    LINKS_PER_PAGE,
    REPEAT_TIMES,
    TIMEOUT_REQUEST,
)


class DBService:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, echo=False)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add_page(self, page: Page) -> None:
        self.session.add(page)
        self.session.commit()

    def get_links(self, page_name: str) -> list[Page] | None:
        page = self.get_page_by_name(page_name)
        if page is not None:
            return [link.name for link in page.links]
        return None

    def get_page_by_name(self, page_name: str) -> Page | None:
        try:
            stmt = select(Page).where(Page.name == page_name)
            result = self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None

    def create_or_get_page(self, name: str) -> Page:
        page = self.get_page_by_name(name)
        if page is None:
            return Page(name=name)
        return page


class ParseService:
    def parse_page(self, name: str) -> set(str):
        links = []
        url = urljoin(BASE_URL, name)
        response = self.get_response(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links_tag = soup.select(
            "#content a[href^='/wiki/'][title]:not(a.mw-disambig):not(a[title^='Вікіпедія:'], a[title^='Шаблон:'], a[title^='Категорія:'], a[title^='Спеціальна:'], a[title^='Довідка:'], a[title^='Перегляд цього шаблону'], a[title^='Портал:']):not(a[class='image'], a[class='internal']):not(a[accesskey])"
        )
        for link in links_tag[:LINKS_PER_PAGE]:
            link_name = link.get("title")
            if link_name not in links:
                links.append(link_name)
        return links

    def get_response(self, url: str) -> requests.Response:
        response = requests.get(url=url)
        if response.status_code != 200:
            count_requests = 0
            while response.status_code != 200:
                sleep(TIMEOUT_REQUEST)
                if count_requests == REPEAT_TIMES:
                    raise TimeoutError(f"No response from wiki! URL: {url}")
                response = requests.get(url=url)
                count_requests += 1
        sleep(60 / REQUESTS_PER_MINUTE)
        return response
