"""Tests for CLI module."""

from pathlib import Path

import pytest
from git_workflow_automator import cli


def test_main():
    """Test main function exists."""
    assert callable(cli.main)


def test_init_generates_templates(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["gwa", "init", "--prompts", "2"]) 

    rc = cli.main()
    assert rc == 0

    copilot = tmp_path / "COPILOT_LOG.md"
    submission = tmp_path / "DEV_SUBMISSION_TEMPLATE.md"
    assert copilot.exists()
    assert submission.exists()
    assert "Prompt 1" in copilot.read_text()
    assert "Prompt 2" in copilot.read_text()


def test_init_alias_slash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["gwa", "/init"]) 
    rc = cli.main()
    assert rc == 0
    assert (tmp_path / "COPILOT_LOG.md").exists()
