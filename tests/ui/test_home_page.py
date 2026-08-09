import re
from playwright.sync_api import Page, expect
from automation_framework.ui.pages.home_page import HomePage


def test_home_page(page: Page):
    page.goto('https://practicesoftwaretesting.com')
    expect(page).to_have_title(re.compile("Practice Software Testing"))
    expect(page).to_have_url("https://practicesoftwaretesting.com/")

def test_home_page_has_products(page: Page):
    home_page = HomePage(page)
    home_page.open()

    first_product = home_page.products.get_first_product()

    expect(first_product.root).to_be_visible()
    expect(first_product.name).not_to_be_empty()
    expect(first_product.price).to_have_text(
        re.compile(r"\$\d+\.\d{2}")
    )
    bolt_product = home_page.products.get_product_by_name("Bolt Cutters")
    expect(bolt_product.name).to_have_text("Bolt Cutters")
    expect(bolt_product.price).to_have_text(
        re.compile(r"\$\d+\.\d{2}")
    )
    expect(bolt_product.compare_btn).to_be_visible()