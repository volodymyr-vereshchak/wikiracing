from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from models import Base, Page, page_to_link
from settings import DATABASE_URL

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from settings import BASE_URL, REQUESTS_PER_MINUTE, LINKS_PER_PAGE

class DBService:

    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, echo=True)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
    
    def __enter__(self) -> DBService:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def add_page(self, page: Page) -> None:
        # self.session.bulk_save_objects(pages)
        self.session.add(page)
        self.session.commit()


    def get_links(self, page_name: str) -> list[Page]:
        stmt = select(page_to_link).join(Page, Page.id == page_to_link.c.link1_id).where(Page.name == page_name)
        result = self.session.execute(stmt)
        return result

    def get_page_by_name(self, page_name: str) -> Page:
        stmt = select(Page).where(Page.name == page_name)
        result = self.session.execute(stmt)
        return result.scalar_one()

    def create_or_get_page(self, name: str) -> Page:
        try:
            return self.get_page_by_name(name)
        except NoResultFound:
            return self.add_page(Page(name=name))


class ParseService:

    def parse_page(self, name: str) -> list(str):
        links = []
        url = urljoin(BASE_URL, name)
        response = requests.get(url=url).content
        soup = BeautifulSoup(response, "html.parser")
        links_tag = soup.select(
            "#content a[href^='/wiki/'][title]:not(.mw-disambig):not(a[title^='Вікіпедія:'], a[title^='Шаблон:'], a[title^='Категорія:'], a[title^='Спеціальна:']):not(a[class='image'], a[class='internal']):not(a[accesskey])"
        )
        for link in links_tag[:LINKS_PER_PAGE]:
            link_name = link.get("title")
            links.append(link_name)
        return links

parse = ParseService()
print(parse.parse_page("Дружба"))