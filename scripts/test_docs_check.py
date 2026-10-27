"""Pytest for the cheat sheet docs check. No network and no agy."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import docs_check

ROOT = Path(__file__).resolve().parents[1]


class _Proc:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_parse_cards_from_cheat_sheet():
    html = (ROOT / "cheat-sheet.html").read_text(encoding="utf-8")
    cards = docs_check.parse_cards(html)
    assert [card["command"] for card in cards] == [
        "/doctor",
        "/context",
        "/model",
        "/permissions",
        "/clear",
        "/login",
        "/goal",
    ]
    assert all(len(card["rows"]) == 4 for card in cards)


def test_command_rows_matches_the_command_token():
    clear = "| `/clear [name]` | Start a fresh conversation |"
    clearall = "| `/clearall` | Not this command |"
    goal = "| `/goal [condition\\|clear]` | Set a finish line |"
    md = "\n".join([clear, clearall, goal])
    assert docs_check.command_rows(md, "/clear") == [clear]
    assert docs_check.command_rows(md, "/goal") == [goal]


def test_parse_reply_ok_outdated_blocked_and_prose():
    assert docs_check.parse_reply("OK") == []
    assert docs_check.parse_reply("OK\n<!-- GOAL_COMPLETE -->\n") == []  # seen from agy 2026-10-27
    reply = "\n".join(
        [
            'OUTDATED: "claim one" -> "doc one"',
            'OUTDATED: "claim two" -> "doc two"',
        ]
    )
    assert docs_check.parse_reply(reply) == [
        '"claim one" -> "doc one"',
        '"claim two" -> "doc two"',
    ]
    assert docs_check.parse_reply("BLOCKED ls") is None
    assert docs_check.parse_reply("The cheat sheet looks fine overall.") is None


def test_resolve_model_picks_highest_argon_medium():
    listing = "\n".join(
        [
            "gemini-4.11-argon-high\tskip",
            "gemini-4.10-argon-medium\tcurrent",
            "gemini-4.9-argon-medium\tolder",
        ]
    )

    def fake_run(cmd, **kwargs):
        return _Proc(0, listing)

    assert docs_check.resolve_model(run=fake_run) == "gemini-4.10-argon-medium"


def test_resolve_model_fails_when_none_match():
    def fake_run(cmd, **kwargs):
        return _Proc(0, "gemini-4.10-argon-high\nclaude\n")

    with pytest.raises(RuntimeError, match="no gemini argon-medium model in agy models"):
        docs_check.resolve_model(run=fake_run)


def test_ask_agy_retries_auto_denied_then_ok(monkeypatch):
    monkeypatch.setattr(docs_check, "RETRY_WAIT_S", 0)
    calls = []

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        if len(calls) < 3:
            return _Proc(1, stdout="", stderr="auto-denied")
        return _Proc(0, stdout="OK", stderr="")

    reply = docs_check.ask_agy(
        "brief",
        model="gemini-4.10-argon-medium",
        run=fake_run,
    )
    assert reply == "OK"
    assert len(calls) == 3
