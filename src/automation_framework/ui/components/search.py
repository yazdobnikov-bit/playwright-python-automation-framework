from playwright.sync_api import Locator


class Search:
    def __init__(self, root: Locator):
        self.root = root
        self.search_input = self.root.locator('[data-test="search-query"]')
        self.search_button = self.root.get_by_role("button", name="Search")
        self.reset_button = self.root.locator('[data-test="search-reset"]')

    def fill(self, text: str) -> None:
        self.search_input.fill(text)

    def submit(self) -> None:
        self.search_button.click()

    def reset(self) -> None:
        self.reset_button.click()

    def search(self, query: str) -> None:
        self.fill(query)
        self.submit()
