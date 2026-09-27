from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app import main


CSS_FILES = ("index.css", "dads.css", "brand.css", "semantic.css")
ROUTES = {
    "/digital-design-system/tokens/index.css": "index.css",
    "/digital-design-system/tokens/dads.css": "dads.css",
    "/digital-design-system/tokens/brand.css": "brand.css",
    "/digital-design-system/tokens/semantic.css": "semantic.css",
}


def _route(path):
    for route in main.app.routes:
        if getattr(route, "path", None) == path:
            return route
    raise AssertionError("route not registered: %s" % path)


def _css_routes():
    for route in main.app.routes:
        path = getattr(route, "path", "") or ""
        if path.endswith(".css"):
            yield route


@pytest.fixture
def css_dir(tmp_path, monkeypatch):
    for name in CSS_FILES:
        (tmp_path / name).write_text(":root{--dads:1}", encoding="utf-8")
    monkeypatch.setenv("DADS_CSS_DIR", str(tmp_path))
    return tmp_path


def test_fixed_css_routes_registered():
    for path in ROUTES:
        assert _route(path).path == path


def test_no_unknown_css_route_registered():
    registered = {route.path for route in _css_routes()}
    assert registered == set(ROUTES) | {"/enterprise.css"}


def test_each_route_depends_on_data_auth():
    for path in ROUTES:
        route = _route(path)
        calls = [dep.call for dep in route.dependant.dependencies]
        assert main.require_auth in calls
        assert main.require_page_auth not in calls


def test_file_response_for_each_fixed_file(css_dir):
    for path, name in ROUTES.items():
        response = _route(path).endpoint()
        assert isinstance(response, FileResponse)
        assert response.media_type == "text/css"
        assert response.headers["cache-control"] == "private, no-store"
        assert Path(response.path) == css_dir / name


def test_unset_env_returns_404(monkeypatch):
    monkeypatch.delenv("DADS_CSS_DIR", raising=False)
    for path in ROUTES:
        with pytest.raises(HTTPException) as excinfo:
            _route(path).endpoint()
        assert excinfo.value.status_code == 404


def test_empty_env_returns_404(monkeypatch):
    monkeypatch.setenv("DADS_CSS_DIR", "")
    for path in ROUTES:
        with pytest.raises(HTTPException) as excinfo:
            _route(path).endpoint()
        assert excinfo.value.status_code == 404


def test_missing_file_returns_404(tmp_path, monkeypatch):
    monkeypatch.setenv("DADS_CSS_DIR", str(tmp_path))
    for path in ROUTES:
        with pytest.raises(HTTPException) as excinfo:
            _route(path).endpoint()
        assert excinfo.value.status_code == 404
