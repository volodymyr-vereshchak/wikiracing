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
        self.engine = create_engine(DATABASE_URL, echo=False)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
    
    def __enter__(self) -> DBService:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def add_page(self, page: Page) -> None:
        self.session.add(page)
        self.session.commit()


    def get_links(self, page_name: str) -> list[Page]|None:
        page = self.get_page_by_name(page_name)
        if page is not None:
            return [link.name for link in page.links]
        return None

    def get_page_by_name(self, page_name: str) -> Page|None:
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
        response = requests.get(url=url).content
        soup = BeautifulSoup(response, "html.parser")
        links_tag = soup.select(
            "#content a[href^='/wiki/'][title]:not(a.mw-disambig):not(a[title^='Вікіпедія:'], a[title^='Шаблон:'], a[title^='Категорія:'], a[title^='Спеціальна:']):not(a[class='image'], a[class='internal']):not(a[accesskey])"
        )
        for link in links_tag[:LINKS_PER_PAGE]:
            link_name = link.get("title")
            if link_name not in links:
                links.append(link_name)
        return links

db = DBService()
print(db.get_links("Бактерії"))

# from typing import List
# import requests
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup
# from time import sleep

# requests_per_minute = 100
# links_per_page = 200
# MAX_DEPTH = 2
# BASE_URL = "https://uk.wikipedia.org/wiki/"

# class WikiRacer:
#     def __init__(self) -> None:
#         self.depth = 0
#         self.flag = False
    
#     def get_links(self, page: str) -> list:
#         links = []
#         url = urljoin(BASE_URL, page)
#         response = requests.get(url=url).content
#         soup = BeautifulSoup(response, "html.parser")
#         links_tag = soup.select("#content a[href^='/wiki/'][title]:not(a.mw-disambig):not(a[title^='Вікіпедія:'], a[title^='Шаблон:'], a[title^='Категорія:'], a[title^='Спеціальна:']):not(a[class='image'], a[class='internal']):not(a[accesskey])")
#         for link in links_tag:
#             links.append(link.get("title"))
#         sleep(60 / requests_per_minute)
#         return links

#     def find_path(self, start: str, finish: str) -> List[str]:
#         path = [start]
#         links = self.get_links(start)
#         self.depth += 1
#         if finish in links:
#             path += [finish]
#             self.flag = True
#             self.depth -= 1
#             return path
#         if finish not in links and self.depth == MAX_DEPTH:
#             self.depth -= 1
#             return []
#         if finish not in links:
#             for link in links[:200]:
#                 path += self.find_path(link, finish)
#                 if self.flag is True:
#                     break
#             self.depth -= 1
#             return path

# wiki = WikiRacer()
# # print(wiki.find_path("Мітохондріальна ДНК", "Вітамін K"))
# print(wiki.find_path("Фестиваль", "Пілястра"))
# # print(wiki.get_links("Дружба"))