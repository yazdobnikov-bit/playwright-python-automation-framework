from playwright.sync_api import Locator


class Categories:
    def __init__(self, root: Locator):
        self.root = root

    def select(self, category: str) -> None:
        self.root.get_by_role("checkbox", name=category).check()
