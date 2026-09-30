"""One spelling and one meaning per term, in everything a person reads.

The portal, the browser extension, the demo page and the Grafana dashboards
are read by the same people. A feature that is "貼り付けガード" on one screen
and "ペーストガード" on another reads as two features, and "ブラウザ" beside
"ブラウザー" reads as an unfinished translation. The rules are written down in
docs/ja-ui-copy-review.md; this test keeps them from drifting back.

It reads text, not behaviour, so it is cheap and has no fixtures.
"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

# Everything that puts Japanese in front of a person.
UI_FILES = [
    "portal/app/static/index.html",
    "extension/src/guard.js",
    "extension/src/manifest.json",
    "extension/src/managed-schema.json",
    "portal/extension-src/guard.js",
    "portal/extension-src/manifest.json",
    "portal/extension-src/managed-schema.json",
    "extension/demo/index.html",
    "dashboards/ai-guard.json",
    "demo/grafana/dash/ai-guard.json",
    "demo/docker-compose.yml",
]


def _text(path):
    return (ROOT / path).read_text(encoding="utf-8")


# (pattern, what to write instead). Patterns are for spellings, so each one is
# a whole family: -er/-or words keep the long vowel, -ry/-ty words do not.
BANNED = [
    (r"ペースト", "貼り付け（機能名は「貼り付けガード」）"),
    (r"ブラウザ(?!ー)", "ブラウザー"),
    (r"サーバ(?!ー)", "サーバー"),
    (r"ユーザ(?!ー)", "ユーザー"),
    (r"スキャナ(?!ー)", "スキャナー"),
    (r"プロバイダ(?!ー)", "プロバイダー"),
    (r"フォルダ(?!ー)", "フォルダー"),
    (r"エディタ(?!ー)", "エディター"),
    (r"パラメータ(?!ー)", "パラメーター"),
    (r"ドライバ(?!ー)", "ドライバー"),
    (r"レシーバ(?!ー)", "受信サービス（レシーバーとは書かない）"),
    (r"コレクタ(?!ー)", "収集エージェント"),
    (r"デバイス(?!コード)", "端末"),
    (r"検知", "検出"),
    (r"AI ツール", "AIツール（AI と ツール の間に空白を入れない）"),
    (r"AI 台帳", "AI台帳"),
]


@pytest.mark.parametrize("path", UI_FILES)
def test_no_variant_spellings(path):
    text = _text(path)
    found = []
    for pattern, use in BANNED:
        for m in re.finditer(pattern, text):
            line = text.count("\n", 0, m.start()) + 1
            found.append("%s:%d %r -> %s" % (path, line, m.group(0), use))
    assert not found, "\n".join(found[:20])


def test_the_two_extension_copies_say_the_same_thing():
    """The portal serves its own copy of the extension source; the two copies
    must stay word for word the same or the demo page and the installed
    extension would describe different products."""
    for name in ("guard.js", "manifest.json", "managed-schema.json"):
        assert _text("extension/src/" + name) == _text("portal/extension-src/" + name), name


def test_the_feature_name_and_the_button_it_describes_are_spelled_alike_everywhere():
    guard = _text("extension/src/guard.js")
    portal = _text("portal/app/static/index.html")
    manifest = json.loads(_text("extension/src/manifest.json"))
    # The extension's own button is what the portal and the demo page quote.
    m = re.search(r'go\.textContent = "([^"]+)"', guard)
    assert m, "the paste guard's continue button moved"
    button = m.group(1)
    assert button == "それでも貼り付ける"
    assert "「%s」" % button in portal
    assert "「%s」" % button in _text("extension/demo/index.html")
    assert "「そのまま貼り付ける」" not in portal
    # One name for the feature: the manifest, the portal navigation and the demo page.
    assert "貼り付けガード" in manifest["name"]
    assert "['paste','貼り付けガード']" in portal
    assert "貼り付けガードの動作デモ" in _text("extension/demo/index.html")


def test_the_glossary_records_the_decisions_this_test_enforces():
    doc = _text("docs/ja-ui-copy-review.md")
    for term in ("貼り付けガード", "ブラウザー", "端末", "収集エージェント", "AI台帳", "ツールレジストリ", "利用者", "検出ソース"):
        assert term in doc, term
