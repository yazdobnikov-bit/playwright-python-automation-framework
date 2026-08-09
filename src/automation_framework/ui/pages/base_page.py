from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, path: str):
        self.page = page
        self.path = path

    def open(self) -> None:
        self.page.goto(self.path)
