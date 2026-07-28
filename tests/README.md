# Test suite

Browser-driven tests (Playwright) for the static site: page health (no console
errors, no broken images/links), the gallery lightbox (open/close, prev/next
navigation, wraparound, keyboard, click-to-close), and responsive layout
(no horizontal overflow across viewport sizes 320px-1920px).

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r tests/requirements.txt
playwright install chromium
```

## Run

```
source .venv/bin/activate
pytest
```

No dev server needs to be running beforehand — `conftest.py` spins up a local
`http.server` on a free port for the duration of the test session.
