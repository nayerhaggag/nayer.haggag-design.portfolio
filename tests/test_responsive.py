"""Layout tests across a range of viewport sizes."""

import pytest
from playwright.sync_api import expect

from conftest import PAGES

VIEWPORTS = [
    (320, 700),   # small phone
    (375, 812),   # iPhone-ish
    (768, 1024),  # tablet
    (1024, 800),  # small laptop
    (1440, 900),  # desktop
    (1920, 1080), # large desktop
]


@pytest.mark.parametrize("width,height", VIEWPORTS)
@pytest.mark.parametrize("page_path", PAGES)
def test_no_horizontal_overflow(page, base_url, page_path, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{base_url}/{page_path}")
    page.wait_for_load_state("networkidle")
    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    client_width = page.evaluate("document.documentElement.clientWidth")
    assert scroll_width <= client_width + 1, (
        f"{page_path} overflows horizontally at {width}x{height}: "
        f"scrollWidth={scroll_width} clientWidth={client_width}"
    )


@pytest.mark.parametrize("width,height", VIEWPORTS)
def test_nav_visible_at_every_size(page, base_url, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{base_url}/index.html")
    nav = page.locator("nav")
    expect(nav).to_be_visible()
    expect(page.locator("nav .nav-brand")).to_be_visible()


@pytest.mark.parametrize("width,height", VIEWPORTS)
def test_hero_heading_fits_within_viewport(page, base_url, width, height):
    page.set_viewport_size({"width": width, "height": height})
    page.goto(f"{base_url}/index.html")
    heading = page.locator(".hero h1")
    box = heading.bounding_box()
    assert box is not None
    assert box["width"] <= width + 1
