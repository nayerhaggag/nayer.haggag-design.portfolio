import http.server
import socket
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "index.html",
    "ai-feedback-tool.html",
    "scan-save.html",
    "solar-charger.html",
    "solar-power-bank.html",
    "whiteboard.html",
    "lawn-mower-cover.html",
]

# Pages that have an image gallery + lightbox.
GALLERY_PAGES = [
    "ai-feedback-tool.html",
    "scan-save.html",
    "solar-charger.html",
    "solar-power-bank.html",
    "whiteboard.html",
    "lawn-mower-cover.html",
]

# Gallery pages with 2+ images, where prev/next navigation actually moves
# between distinct images.
MULTI_IMAGE_GALLERY_PAGES = [
    "ai-feedback-tool.html",
    "scan-save.html",
    "solar-charger.html",
    "whiteboard.html",
    "lawn-mower-cover.html",
]

# Gallery pages with exactly one image, where prev/next should just wrap to
# the same image rather than error.
SINGLE_IMAGE_GALLERY_PAGES = [
    "solar-power-bank.html",
]


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # silence request logging
        pass


@pytest.fixture(scope="session")
def base_url():
    port = _free_port()
    handler = lambda *args, **kwargs: _QuietHandler(
        *args, directory=str(REPO_ROOT), **kwargs
    )
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()
    server.server_close()


@pytest.fixture
def console_errors(page):
    """Collect JS console errors and page errors raised while the test runs."""
    errors = []
    page.on(
        "console",
        lambda msg: errors.append(msg.text) if msg.type == "error" else None,
    )
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    return errors
