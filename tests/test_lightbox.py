"""Tests for the gallery lightbox: opening, closing, and prev/next navigation."""

import pytest
from playwright.sync_api import expect

from conftest import GALLERY_PAGES, MULTI_IMAGE_GALLERY_PAGES, SINGLE_IMAGE_GALLERY_PAGES


@pytest.fixture
def gallery_page(page, base_url):
    def _open(page_path):
        page.goto(f"{base_url}/{page_path}")
        page.wait_for_load_state("networkidle")
        return page

    return _open


def _gallery_srcs(page):
    return page.locator(".gallery img").evaluate_all("els => els.map(e => e.src)")


@pytest.mark.parametrize("page_path", GALLERY_PAGES)
def test_clicking_image_opens_lightbox_with_same_image(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)

    overlay = page.locator(".lightbox-overlay")
    expect(overlay).not_to_have_class(("lightbox-overlay active",))

    page.locator(".gallery img").first.click()
    expect(overlay).to_have_class("lightbox-overlay active")
    expect(overlay.locator("img")).to_have_attribute("src", srcs[0])


@pytest.mark.parametrize("page_path", SINGLE_IMAGE_GALLERY_PAGES)
def test_nav_arrows_wrap_to_same_image_when_only_one_image(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)
    assert len(srcs) == 1

    page.locator(".gallery img").first.click()
    overlay_img = page.locator(".lightbox-overlay img")
    expect(overlay_img).to_have_attribute("src", srcs[0])

    page.locator(".lightbox-next").click()
    expect(overlay_img).to_have_attribute("src", srcs[0])

    page.locator(".lightbox-prev").click()
    expect(overlay_img).to_have_attribute("src", srcs[0])


@pytest.mark.parametrize("page_path", MULTI_IMAGE_GALLERY_PAGES)
def test_next_arrow_advances_image(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)

    page.locator(".gallery img").first.click()
    overlay = page.locator(".lightbox-overlay")
    overlay_img = overlay.locator("img")
    expect(overlay_img).to_have_attribute("src", srcs[0])

    page.locator(".lightbox-next").click()
    expect(overlay_img).to_have_attribute("src", srcs[1])


@pytest.mark.parametrize("page_path", MULTI_IMAGE_GALLERY_PAGES)
def test_prev_arrow_wraps_to_last_image(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)

    page.locator(".gallery img").first.click()
    overlay_img = page.locator(".lightbox-overlay img")
    expect(overlay_img).to_have_attribute("src", srcs[0])

    page.locator(".lightbox-prev").click()
    expect(overlay_img).to_have_attribute("src", srcs[-1])


@pytest.mark.parametrize("page_path", MULTI_IMAGE_GALLERY_PAGES)
def test_next_arrow_wraps_to_first_image(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)

    # open on the last image, then advance past the end
    page.locator(".gallery img").last.click()
    overlay_img = page.locator(".lightbox-overlay img")
    expect(overlay_img).to_have_attribute("src", srcs[-1])

    page.locator(".lightbox-next").click()
    expect(overlay_img).to_have_attribute("src", srcs[0])


@pytest.mark.parametrize("page_path", MULTI_IMAGE_GALLERY_PAGES)
def test_arrow_keys_navigate_images(gallery_page, page_path):
    page = gallery_page(page_path)
    srcs = _gallery_srcs(page)

    page.locator(".gallery img").first.click()
    overlay_img = page.locator(".lightbox-overlay img")
    expect(overlay_img).to_have_attribute("src", srcs[0])

    page.keyboard.press("ArrowRight")
    expect(overlay_img).to_have_attribute("src", srcs[1])

    page.keyboard.press("ArrowLeft")
    expect(overlay_img).to_have_attribute("src", srcs[0])


@pytest.mark.parametrize("page_path", GALLERY_PAGES)
def test_escape_key_closes_lightbox(gallery_page, page_path):
    page = gallery_page(page_path)
    page.locator(".gallery img").first.click()
    overlay = page.locator(".lightbox-overlay")
    expect(overlay).to_have_class("lightbox-overlay active")

    page.keyboard.press("Escape")
    expect(overlay).not_to_have_class("lightbox-overlay active")


@pytest.mark.parametrize("page_path", GALLERY_PAGES)
def test_clicking_outside_image_closes_lightbox(gallery_page, page_path):
    page = gallery_page(page_path)
    page.locator(".gallery img").first.click()
    overlay = page.locator(".lightbox-overlay")
    expect(overlay).to_have_class("lightbox-overlay active")

    # click near the top-left corner of the overlay, away from the centered image
    overlay.click(position={"x": 5, "y": 5})
    expect(overlay).not_to_have_class("lightbox-overlay active")


@pytest.mark.parametrize("page_path", GALLERY_PAGES)
def test_nav_buttons_do_not_close_lightbox(gallery_page, page_path):
    page = gallery_page(page_path)
    page.locator(".gallery img").first.click()
    overlay = page.locator(".lightbox-overlay")

    page.locator(".lightbox-next").click()
    expect(overlay).to_have_class("lightbox-overlay active")

    page.locator(".lightbox-prev").click()
    expect(overlay).to_have_class("lightbox-overlay active")


@pytest.mark.parametrize("page_path", GALLERY_PAGES)
def test_body_scroll_locked_while_open(gallery_page, page_path):
    page = gallery_page(page_path)
    page.locator(".gallery img").first.click()
    overflow = page.evaluate("document.body.style.overflow")
    assert overflow == "hidden"

    page.keyboard.press("Escape")
    overflow = page.evaluate("document.body.style.overflow")
    assert overflow == ""
