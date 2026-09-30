# Copyright 2026 Aman Karir
# SPDX-License-Identifier: Apache-2.0
# Part of Shadow AI Guard, https://github.com/AmanSK5/shadow-ai-guard

"""The weekly digest: the schedule computation and the text it sends.

The background loop itself is not under test - it is a sleep around these
two functions. What can be quietly wrong is the arithmetic (a digest that
fires on the wrong day, or twice) and the text (numbers that disagree with
the pages the reader opens next), so those are what get pinned down.
"""

import os
from datetime import datetime, timezone

os.environ.setdefault("PORTAL_AUTH", "none")

from app import main


def dt(y, m, d, h=0):
    return datetime(y, m, d, h, tzinfo=timezone.utc)


# 2026-08-24 is a Monday.


def test_next_digest_is_the_coming_slot():
    # Sunday evening -> Monday 08:00.
    assert main.next_digest(dt(2026, 8, 23, 20), "mon", 8) == dt(2026, 8, 24, 8)
    # Monday 07:59 -> the same morning.
    assert main.next_digest(dt(2026, 8, 24, 7), "mon", 8) == dt(2026, 8, 24, 8)


def test_next_digest_never_returns_now_or_the_past():
    # Exactly on the slot -> a week later, so a send at 08:00 cannot
    # reschedule itself for the moment it just fired.
    assert main.next_digest(dt(2026, 8, 24, 8), "mon", 8) == dt(2026, 8, 31, 8)
    # Monday afternoon -> next Monday.
    assert main.next_digest(dt(2026, 8, 24, 15), "mon", 8) == dt(2026, 8, 31, 8)


def test_next_digest_unknown_day_falls_back_to_monday():
    assert main.next_digest(dt(2026, 8, 22, 0), "someday", 8).weekday() == 0


def test_digest_text_carries_the_numbers_the_pages_show():
    g = {
        "personal_accounts": [
            {"user": "kaya", "device": "MAC-1", "tool": "chatgpt"},
            {"user": "", "device": "WIN-2", "tool": "gemini"},
        ],
        "counts": {"tools": 9, "devices": 61},
        "tools": {"chatgpt": {"devices": ["a", "b"]},
                  "claude": {"devices": ["a"]}},
    }
    s = {"groups": [
        {"group": "endpoint", "sources": [{"source": "x", "reporting": True}]},
        {"group": "cloud", "sources": [{"source": "y", "reporting": False},
                                       {"source": "z", "reporting": False}]},
    ]}
    text = main.digest_text(g, s, 168)
    assert "直近 7 日間" in text
    assert "個人アカウント 2 件（2 人）" in text
    assert "使用中のツール 9 件、端末 61 台" in text
    assert "chatgpt（2 台）" in text
    assert "報告のない検出ソース 2 件" in text


def test_digest_text_singular_forms_and_empty_estate():
    g = {"personal_accounts": [{"user": "kaya", "device": "", "tool": "t"}],
         "counts": {"tools": 0, "devices": 0}, "tools": {}}
    text = main.digest_text(g, {"groups": []}, 24)
    assert "個人アカウント 1 件（1 人）" in text
    assert "利用端末数の多いツール" not in text
    assert "報告のない検出ソース" not in text
