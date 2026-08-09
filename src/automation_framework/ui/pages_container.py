from playwright.sync_api import Page

from automation_framework.ui.pages.sign_in_page import SignInPage
from automation_framework.ui.pages.home_page import HomePage


class Pages:
    def __init__(self, page: Page):
        self.sign_in = SignInPage(page)
        self.home = HomePage(page)