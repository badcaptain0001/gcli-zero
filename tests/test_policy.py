"""Tests for policy enforcement."""

import pytest

from git_workflow_automator.config import Config, BranchPolicy, CommitPolicy
from git_workflow_automator.policy import PolicyEnforcer, PolicyViolation


def test_branch_name_validation_with_prefix():
    """Test branch name validation with prefix requirement."""
    config = Config(
        branch=BranchPolicy(
            prefix_required=True,
            allowed_prefixes=["feature", "bugfix"],
            protected_branches=["main"]
        )
    )
    enforcer = PolicyEnforcer(config)
    
    # Valid branch names
    enforcer.validate_branch_name("feature/my-feature")
    enforcer.validate_branch_name("bugfix/fix-bug")
    
    # Invalid branch names
    with pytest.raises(PolicyViolation) as exc_info:
        enforcer.validate_branch_name("my-feature")
    assert "must start with one of" in str(exc_info.value)


def test_branch_name_validation_protected():
    """Test that protected branches cannot be used."""
    config = Config(
        branch=BranchPolicy(protected_branches=["main", "master"])
    )
    enforcer = PolicyEnforcer(config)
    
    with pytest.raises(PolicyViolation) as exc_info:
        enforcer.validate_branch_name("main")
    assert "protected name" in str(exc_info.value)


def test_commit_message_validation_conventional():
    """Test conventional commit message validation."""
    config = Config(
        commit=CommitPolicy(
            conventional_commits=True,
            allowed_types=["feat", "fix", "docs"],
            require_scope=False,
            max_subject_length=72
        )
    )
    enforcer = PolicyEnforcer(config)
    
    # Valid messages
    enforcer.validate_commit_message("feat: add new feature")
    enforcer.validate_commit_message("fix(auth): fix login bug")
    enforcer.validate_commit_message("docs: update README")
    
    # Invalid messages
    with pytest.raises(PolicyViolation) as exc_info:
        enforcer.validate_commit_message("Added new feature")
    assert "conventional commits format" in str(exc_info.value)
    
    with pytest.raises(PolicyViolation) as exc_info:
        enforcer.validate_commit_message("invalid: wrong type")
    assert "conventional commits format" in str(exc_info.value)


def test_commit_message_length_validation():
    """Test commit message length validation."""
    config = Config(
        commit=CommitPolicy(max_subject_length=50, conventional_commits=False)
    )
    enforcer = PolicyEnforcer(config)
    
    # Valid message
    enforcer.validate_commit_message("Short message")
    
    # Invalid message (too long)
    with pytest.raises(PolicyViolation) as exc_info:
        enforcer.validate_commit_message("x" * 51)
    assert "exceeds" in str(exc_info.value)


def test_commit_message_with_scope_required():
    """Test commit message validation when scope is required."""
    config = Config(
        commit=CommitPolicy(
            conventional_commits=True,
            require_scope=True,
            allowed_types=["feat", "fix"]
        )
    )
    enforcer = PolicyEnforcer(config)
    
    # Valid with scope
    enforcer.validate_commit_message("feat(api): add endpoint")
    
    # Invalid without scope
    with pytest.raises(PolicyViolation):
        enforcer.validate_commit_message("feat: add endpoint")
