from playwright.sync_api import Page

from automation_framework.ui.pages.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, 'https://practicesoftwaretesting.com/auth/login')
        self.email_input = self.page.get_by_placeholder('Your email')
        self.password_input = self.page.get_by_placeholder('Your password')
        self.sign_in_button = self.page.get_by_role('button', name='Login')
        self.register_link = self.page.get_by_label('Register your account')
        self.email_error = self.page.locator('[data-test="email-error"]')
        self.password_error = self.page.locator('[data-test="password-error"]')
        self.sign_in_error = self.page.locator('[data-test="login-error"]')

    def fill_email(self, email: str) -> None:
        self.email_input.fill(email)

    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def click_sign_in(self) -> None:
        self.sign_in_button.click()

    def sign_in(self, email: str, password: str) -> None:
        self.fill_email(email)
        self.fill_password(password)
        self.click_sign_in()

    def click_register(self) -> None:
        self.register_link.click()