from playwright.sync_api import expect

from automation_framework.ui.pages_container import Pages


def test_sign_in_with_empty_credentials(pages: Pages):
    pages.sign_in.open()
    pages.sign_in.click_sign_in()
    expect(pages.sign_in.email_error).to_be_visible()
    expect(pages.sign_in.password_error).to_be_visible()
    expect(pages.sign_in.email_error).to_have_text("Email is required")
    expect(pages.sign_in.password_error).to_have_text("Password is required")


def test_sign_in_with_invalid_credentials(pages: Pages):
    pages.sign_in.open()
    pages.sign_in.sign_in("nonexistent@example.com", "WrongPassword123!")
    expect(pages.sign_in.sign_in_error).to_be_visible()
    expect(pages.sign_in.sign_in_error).to_have_text("Invalid email or password")
