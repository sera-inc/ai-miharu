"""The brand set the page links is served by name, from files that exist.

The page links a favicon, an SVG and an Apple touch icon besides the PNG
symbol. A link to a route that does not exist is a console 404 on every load
and a blank tab icon, and the hooded upstream logo must not come back through
/logo.png.
"""
import re
from pathlib import Path

import pytest
from fastapi.responses import FileResponse

from app import main

HTML = (main.STATIC / "index.html").read_text(encoding="utf-8")

ROUTES = {
    "/favicon.ico": ("favicon.ico", "image/x-icon"),
    "/apple-touch-icon.png": ("apple-touch-icon.png", "image/png"),
    "/sera-ai-governance-symbol.svg": ("sera-ai-governance-symbol.svg", "image/svg+xml"),
    "/sera-ai-governance-symbol-white.svg": ("sera-ai-governance-symbol-white.svg", "image/svg+xml"),
    "/sera-ai-governance-symbol.png": ("sera-ai-governance-symbol.png", "image/png"),
    "/logo.png": ("logo.png", "image/png"),
}


def _route(path):
    return next(r for r in main.app.routes if getattr(r, "path", "") == path)


@pytest.mark.parametrize("path", sorted(ROUTES))
def test_each_brand_file_is_served_by_a_fixed_route(path):
    name, media_type = ROUTES[path]
    route = _route(path)
    assert main.require_page_auth in [dep.call for dep in route.dependant.dependencies]
    response = route.endpoint()
    assert isinstance(response, FileResponse)
    assert response.media_type == media_type
    assert Path(response.path) == main.STATIC / name
    assert (main.STATIC / name).stat().st_size > 0


def test_the_page_links_only_routes_that_exist():
    served = {getattr(r, "path", "") for r in main.app.routes}
    links = re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]*href="([^"]+)"', HTML)
    assert links, "the page should declare its icons"
    assert set(links) <= served
    assert "/favicon.ico" in links and "/apple-touch-icon.png" in links
    assert "/sera-ai-governance-symbol.svg" in links


def test_the_public_logo_route_is_the_current_mark_not_the_upstream_logo():
    # The route survives for old bookmarks and READMEs; it serves the same
    # bytes as the symbol, never the hooded Shadow AI Guard logo.
    assert (main.STATIC / "logo.png").read_bytes() == (main.STATIC / "sera-ai-governance-symbol.png").read_bytes()


def test_the_sidebar_uses_the_white_mark_and_the_sign_in_card_has_both():
    assert re.search(r'id="brand-home"[^>]*>\s*<img src="/sera-ai-governance-symbol-white\.svg"', HTML)
    assert 'class="mark-on-light" src="/sera-ai-governance-symbol.svg"' in HTML
    assert 'class="mark-on-dark" src="/sera-ai-governance-symbol-white.svg"' in HTML
    assert "[data-theme=dark] .mark-on-light{display:none}" in HTML


def test_the_svg_sources_carry_an_accessible_title_and_no_script():
    for name in ("sera-ai-governance-symbol.svg", "sera-ai-governance-symbol-white.svg"):
        svg = (main.STATIC / name).read_text(encoding="utf-8")
        assert "<title" in svg and "世良AIガバナンス" in svg
        assert "<script" not in svg and "onload" not in svg.lower()
