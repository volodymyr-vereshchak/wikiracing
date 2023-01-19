from services import DBService, ParseService
from settings import MAX_DEPTH


class WikiRacer:

    def __init__(self) -> None:
        self.db_service = DBService()
        self.parse_service = ParseService()
        self.depth = 0
        self.flag = False

    def find_path(self, start: str, finish: str) -> list[str]:
        path = []
        depth = 2
        while True:
            if len(path) > 1 or depth > MAX_DEPTH:
                break
            path = self.find_path_with_depth(start, finish, depth)
            depth += 1
        return path
    
    def find_path_with_depth(self, start: str, finish: str, max_depth: int) -> list[str]:
        path = [start]
        links_str = self.db_service.get_links(start)
        if not links_str or links_str is None:
            page = self.db_service.create_or_get_page(start)
            links_str = self.parse_service.parse_page(start)
            links = []
            for link in links_str:
                links.append(self.db_service.create_or_get_page(link))
            page.links = links
            self.db_service.add_page(page)
        
        self.depth += 1
        if finish in links_str:
            path += [finish]
            self.flag = True
            self.depth -= 1
            return path
        if finish not in links_str and self.depth == max_depth:
            self.depth -= 1
            return []
        if finish not in links_str:
            for link in links_str:
                path += self.find_path_with_depth(link, finish, max_depth)
                if self.flag is True:
                    break
            self.depth -= 1
            return path
        

wiki = WikiRacer()
# print(wiki.find_path("Дружба", "Рим"))
print(wiki.find_path("Мітохондріальна ДНК", "Вітамін K"))
