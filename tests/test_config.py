"""Tests for configuration module."""

import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from git_workflow_automator.config import Config, BranchPolicy, CommitPolicy, load_config


def test_default_config():
    """Test that default config loads successfully."""
    config = Config()
    assert config.branch.main_branch == "main"
    assert config.commit.conventional_commits is True
    assert config.pr.require_description is True


def test_branch_policy_validation():
    """Test branch policy validation."""
    policy = BranchPolicy(
        prefix_required=True,
        allowed_prefixes=["feat", "fix"],
        protected_branches=["main"]
    )
    assert policy.prefix_required is True
    assert "feat" in policy.allowed_prefixes


def test_commit_policy_validation():
    """Test commit policy validation."""
    policy = CommitPolicy(max_subject_length=50)
    assert policy.max_subject_length == 50


def test_commit_policy_min_length_validation():
    """Test that commit policy enforces minimum length."""
    with pytest.raises(ValidationError) as exc_info:
        CommitPolicy(max_subject_length=5)
    assert "max_subject_length must be at least 10" in str(exc_info.value)


def test_load_config_from_file():
    """Test loading config from .gwa.toml file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".gwa.toml"
        config_path.write_text("""
[branch]
prefix_required = true
allowed_prefixes = ["feature", "bugfix"]
main_branch = "develop"

[commit]
max_subject_length = 80
""")
        
        config = load_config(config_path)
        assert config.branch.prefix_required is True
        assert config.branch.main_branch == "develop"
        assert config.commit.max_subject_length == 80


def test_load_config_missing_file():
    """Test that missing config file returns defaults."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".gwa.toml"
        config = load_config(config_path)
        assert config.branch.main_branch == "main"
