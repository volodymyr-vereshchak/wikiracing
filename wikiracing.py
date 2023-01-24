from services import DBService, ParseService
from settings import MAX_DEPTH


class WikiRacer:

    def __init__(self) -> None:
        self.parse_service = ParseService()
        self.db_service = DBService()
        self.depth = 0
        self.flag = False

    def find_path(self, start: str, finish: str) -> list[str]:
        path = []
        depth = 2
        self.flag = False
        while True:
            if path or depth > MAX_DEPTH:
                break
            path = self.find_path_with_depth(start, finish, depth)
            depth += 1
        return path
    
    def find_path_with_depth(self, start: str, finish: str, max_depth: int) -> list[str]:
        path = []
        links_str = self.db_service.get_links(start)
        if not links_str or links_str is None:
            page = self.db_service.create_or_get_page(start)
            links_str = self.parse_service.parse_page(start)
            page.links = [self.db_service.create_or_get_page(link) for link in links_str]
            self.db_service.add_page(page)
        
        self.depth += 1
        
        if finish in links_str:
            path += [start, finish]
            self.flag = True
            self.depth -= 1
            return path
        
        if finish not in links_str:
            for link in links_str:
                if self.depth == max_depth or self.flag is True:
                    break
                path = self.find_path_with_depth(link, finish, max_depth)
            self.depth -= 1
            return [start] + path if path else path

