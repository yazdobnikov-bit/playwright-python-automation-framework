import re

from playwright.sync_api import expect

from automation_framework.ui.pages_container import Pages


def test_home_page(pages: Pages, base_url: str):
    pages.home.open()
    expected_url = base_url.rstrip('/') + '/'
    expect(pages.home.page).to_have_title(re.compile("Practice Software Testing"))
    expect(pages.home.page).to_have_url(expected_url)


def test_home_page_has_products(pages: Pages):
    pages.home.open()

    first_product = pages.home.products.get_first_product()

    expect(first_product.root).to_be_visible()
    expect(first_product.name).not_to_be_empty()
    expect(first_product.price).to_have_text(re.compile(r"\$\d+\.\d{2}"))
    bolt_product = pages.home.products.get_product_by_name("Bolt Cutters")
    expect(bolt_product.name).to_have_text("Bolt Cutters")
    expect(bolt_product.price).to_have_text(re.compile(r"\$\d+\.\d{2}"))
    expect(bolt_product.compare_btn).to_be_visible()
