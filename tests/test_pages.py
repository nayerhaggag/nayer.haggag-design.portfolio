"""Smoke tests: every page loads cleanly, with no console/page errors,
no broken images, and no broken internal links."""

import re

import pytest
from playwright.sync_api import expect

from conftest import PAGES


@pytest.mark.parametrize("page_path", PAGES)
def test_page_loads_without_console_errors(page, base_url, console_errors, page_path):
    response = page.goto(f"{base_url}/{page_path}")
    assert response.ok, f"{page_path} returned status {response.status}"
    assert console_errors == [], f"{page_path} produced console errors: {console_errors}"


@pytest.mark.parametrize("page_path", PAGES)
def test_page_has_title_and_footer(page, base_url, page_path):
    page.goto(f"{base_url}/{page_path}")
    assert page.title().strip() != ""
    footer = page.locator("footer")
    expect(footer).to_be_visible()
    expect(footer).to_contain_text("Nayer Haggag")


@pytest.mark.parametrize("page_path", PAGES)
def test_page_has_working_nav(page, base_url, page_path):
    page.goto(f"{base_url}/{page_path}")
    nav = page.locator("nav")
    expect(nav).to_be_visible()
    expect(nav.locator("a.nav-brand")).to_be_visible()
    expect(nav.locator(".nav-links a")).to_have_count(4)


@pytest.mark.parametrize("page_path", PAGES)
def test_no_broken_images(page, base_url, page_path):
    page.goto(f"{base_url}/{page_path}")
    page.wait_for_load_state("networkidle")
    # Scope to real content images; the lightbox overlay injects its own
    # <img> with no src until an image has been clicked open.
    images = page.locator("img:not(.lightbox-overlay img)")
    count = images.count()
    assert count > 0, f"{page_path} has no images"
    for i in range(count):
        img = images.nth(i)
        natural_width = img.evaluate("el => el.naturalWidth")
        src = img.get_attribute("src")
        assert natural_width and natural_width > 0, f"Broken image on {page_path}: {src}"


@pytest.mark.parametrize("page_path", PAGES)
def test_internal_links_resolve(page, base_url, page_path):
    page.goto(f"{base_url}/{page_path}")
    hrefs = page.locator("a[href]").evaluate_all(
        "els => els.map(e => e.getAttribute('href'))"
    )
    internal_htmls = {
        h.split("#")[0]
        for h in hrefs
        if h and not h.startswith(("http://", "https://", "mailto:", "tel:", "#"))
        and h.split("#")[0] != ""
    }
    for href in internal_htmls:
        resp = page.context.request.get(f"{base_url}/{href}")
        assert resp.ok, f"Broken internal link on {page_path}: {href} -> {resp.status}"


def test_index_project_cards_link_to_real_pages(page, base_url):
    page.goto(f"{base_url}/index.html")
    cards = page.locator(".projects > a")
    count = cards.count()
    assert count >= 6
    for i in range(count):
        href = cards.nth(i).get_attribute("href")
        assert href and re.match(r"^[\w-]+\.html$", href)
