from services import DBService, ParseService
from models import Base, Page, page_to_link


class WikiRacer:

    def __init__(self) -> None:
        self.db_service = DBService()
        self.parse_service = ParseService()

    def find_path(self, start: str, finish: str) -> list[str]:
        page = self.db_service.create_or_get_page(start)
        links_str = self.parse_service.parse_page(start)
        links = []
        for link in links_str:
            links.append(self.db_service.create_or_get_page(link))
        page.links = links
        self.db_service.add_page(page)


wiki = WikiRacer()
print(wiki.find_path("Дружба", "Рим"))
# page_1 = wiki.db_service.create_or_get_page(name="test1", url="https://test1")
# page_2 = wiki.db_service.create_or_get_page(name="test2", url="https://test2")
# # page_3 = Page(name="test3", url="https://test3")
# # wiki.db_service.add_page(page_1, [page_2, page_3])
# # page_4 = Page(name="test4", url="https://test4")
# # page_5 = Page(name="test5", url="https://test5")
# # page_7 = Page(name="test7", url="https://test7")
# # # page_4.links = [page_5, page_6]
# # page_7.links = [page_4, page_5]
# # wiki.db_service.add_page([page_7])
# # for page in wiki.db_service.get_links("test2").scalars():
# #     print(page.name)

# page_10 = wiki.db_service.create_or_get_page(name="test10", url="https://test10")
# page_10.links = [page_1, page_2]
# # page_7 = Page(name="test7", url="https://test7")
# # page_7.links = [page_4]
# wiki.db_service.add_page([page_10])
