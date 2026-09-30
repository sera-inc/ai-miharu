import logging
import re
from pathlib import Path

import pytest
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app import main


MOUNT_FILES = ("index.css", "dads.css", "brand.css", "semantic.css")
ROUTES = {
    "/digital-design-system/tokens/index.css": "index.css",
    "/digital-design-system/tokens/dads.css": "dads.css",
    "/digital-design-system/tokens/brand.css": "brand.css",
    "/digital-design-system/tokens/semantic.css": "semantic.css",
}
BUNDLED = ("index.css", "dads.css")


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
    for name in MOUNT_FILES:
        (tmp_path / name).write_text(":root{--dads:1}", encoding="utf-8")
    monkeypatch.setenv("DADS_CSS_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture
def no_mount(monkeypatch):
    monkeypatch.delenv("DADS_CSS_DIR", raising=False)


def test_fixed_css_routes_registered():
    for path in ROUTES:
        assert _route(path).path == path


def test_no_unknown_css_route_registered():
    registered = {route.path for route in _css_routes()}
    assert registered == set(ROUTES) | {"/enterprise.css", "/dads-product.css"}


def test_each_route_uses_page_auth():
    for path in ROUTES:
        route = _route(path)
        calls = [dep.call for dep in route.dependant.dependencies]
        assert main.require_page_auth in calls
        assert main.require_auth not in calls


# ------------------------------------------------------- the bundled default --


def test_a_plain_run_serves_the_bundled_tokens(no_mount):
    """A clone with no mount and no private checkout still gets the DADS skin."""
    assert main.dads_token_source() == "bundled"
    for path, name in ROUTES.items():
        if name not in BUNDLED:
            continue
        response = _route(path).endpoint()
        assert isinstance(response, FileResponse)
        assert response.media_type == "text/css"
        assert response.headers["cache-control"] == "private, no-store"
        assert Path(response.path) == main.DADS_BUNDLE / name


def test_the_bundle_ships_no_private_layer_two_files(no_mount):
    """brand.css and semantic.css are the design system's own Layer 2. They are
    not bundled, so the routes stay dark unless an organisation mounts them."""
    for path, name in ROUTES.items():
        if name in BUNDLED:
            continue
        with pytest.raises(HTTPException) as excinfo:
            _route(path).endpoint()
        assert excinfo.value.status_code == 404
    assert sorted(p.name for p in main.DADS_BUNDLE.iterdir()) == sorted(BUNDLED)


def test_the_bundle_is_the_generated_public_layer_one():
    text = (main.DADS_BUNDLE / "dads.css").read_text(encoding="utf-8")
    assert "@digital-go-jp/tailwind-theme-plugin v1.0.1" in text
    assert "MIT License" in text
    assert "generated; do not edit by hand" in text
    assert "--dads-color-focus-blue:" in text
    # Layer 1 only: no product or design-system Layer 2 definitions in it.
    assert not re.search(r"^\s*--(app|brand)-[a-z0-9-]+\s*:", text, re.M)
    index = (main.DADS_BUNDLE / "index.css").read_text(encoding="utf-8")
    # The bundled entry point pulls in Layer 1 only.
    assert re.findall(r'@import\s+"([^"]+)"', index) == ["./dads.css"]


def test_every_dads_token_the_adapter_uses_is_in_the_bundle():
    """The adapter is written against Layer 1 names. A name the public bundle
    does not define would render as an unset property on a plain clone."""
    adapter = (main.STATIC / "dads-product.css").read_text(encoding="utf-8")
    bundle = (main.DADS_BUNDLE / "dads.css").read_text(encoding="utf-8")
    defined = set(re.findall(r"(--dads-[a-z0-9-]+)\s*:", bundle, re.I))
    used = set(re.findall(r"var\((--dads-[a-z0-9-]+)", adapter, re.I))
    assert used, "the adapter should reference DADS tokens"
    assert used - defined == set()


def test_the_adapter_defines_every_layer_two_name_it_falls_back_on():
    """--app-* names come from the design system's Layer 2 when it is mounted.
    On a plain clone the adapter's own layered fallback must cover each one,
    and must lose to a mounted Layer 2 (declarations inside @layer do)."""
    adapter = (main.STATIC / "dads-product.css").read_text(encoding="utf-8")
    fallback = re.search(r"@layer sera-standalone-fallback\s*\{(.*?)\n\}", adapter, re.S)
    assert fallback, "the standalone fallback layer is missing"
    defined = set(re.findall(r"(--app-[a-z0-9-]+)\s*:", fallback.group(1)))
    used = {name for name in re.findall(r"var\((--app-[a-z0-9-]+)", adapter)
            if not name.startswith("--app-sg-")}
    assert used, "the adapter should use some Layer 2 names"
    assert used - defined == set()


# -------------------------------------------------------- the optional mount --


def test_a_complete_mount_replaces_the_bundle(css_dir):
    assert main.dads_token_source() == "mounted"
    for path, name in ROUTES.items():
        response = _route(path).endpoint()
        assert isinstance(response, FileResponse)
        assert Path(response.path) == css_dir / name


def test_empty_env_means_no_mount(monkeypatch):
    monkeypatch.setenv("DADS_CSS_DIR", "")
    assert main.dads_token_source() == "bundled"
    assert Path(_route("/digital-design-system/tokens/dads.css").endpoint().path) \
        == main.DADS_BUNDLE / "dads.css"


def test_an_incomplete_mount_is_refused_loudly_not_half_used(tmp_path, monkeypatch, caplog):
    (tmp_path / "dads.css").write_text(":root{--dads:1}", encoding="utf-8")
    monkeypatch.setenv("DADS_CSS_DIR", str(tmp_path))
    assert main.dads_token_source() == "bundled"
    # The bundle is used, never the lone file in the incomplete directory.
    assert Path(_route("/digital-design-system/tokens/dads.css").endpoint().path) \
        == main.DADS_BUNDLE / "dads.css"
    with caplog.at_level(logging.INFO, logger="portal"):
        main._dads_preflight()
    text = caplog.text
    assert "is incomplete" in text and "index.css" in text and "semantic.css" in text
    assert "DADS tokens: bundled" in text


def test_preflight_says_which_tokens_are_in_use(css_dir, caplog):
    with caplog.at_level(logging.INFO, logger="portal"):
        main._dads_preflight()
    assert "DADS tokens: mounted" in caplog.text
    assert "incomplete" not in caplog.text


def test_the_config_names_the_token_source(css_dir, monkeypatch):
    assert main.config(None, _=None)["dads_tokens"] == "mounted"
    monkeypatch.delenv("DADS_CSS_DIR")
    assert main.config(None, _=None)["dads_tokens"] == "bundled"


# --------------------------------------------------------------- the adapter --


def test_product_adapter_is_served_with_page_auth(no_mount):
    route = _route("/dads-product.css")
    assert main.require_page_auth in [dep.call for dep in route.dependant.dependencies]
    response = route.endpoint()
    assert isinstance(response, FileResponse)
    assert Path(response.path) == main.STATIC / "dads-product.css"
    assert response.headers["cache-control"] == "private, no-store"


def test_product_adapter_is_served_with_a_mount_too(css_dir):
    response = _route("/dads-product.css").endpoint()
    assert Path(response.path) == main.STATIC / "dads-product.css"


def test_product_adapter_is_off_only_when_no_tokens_exist_at_all(no_mount, monkeypatch, tmp_path):
    monkeypatch.setattr(main, "DADS_BUNDLE", tmp_path)   # an image built without the bundle
    with pytest.raises(HTTPException) as excinfo:
        _route("/dads-product.css").endpoint()
    assert excinfo.value.status_code == 404
