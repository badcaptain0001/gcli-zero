"""Integration tests for basic workflow."""

import subprocess
import tempfile
from pathlib import Path


def test_basic_cli_workflow():
    """Test basic CLI workflow commands."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
        
        # Create .git directory structure for audit logs
        (repo_path / ".git" / "gwa").mkdir(parents=True, exist_ok=True)
        
        # Test dry-run commands
        result = subprocess.run(
            ["gwa", "--dry-run", "start", "feature/test"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "DRY RUN" in result.stdout
        
        result = subprocess.run(
            ["gwa", "--dry-run", "commit"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "DRY RUN" in result.stdout
        
        result = subprocess.run(
            ["gwa", "doctor"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "Git repository detected" in result.stdout


def test_policy_validation_integration():
    """Test that policy validation works with config."""
    from git_workflow_automator.config import Config, BranchPolicy
    from git_workflow_automator.policy import PolicyEnforcer, PolicyViolation
    
    config = Config(
        branch=BranchPolicy(
            prefix_required=True,
            allowed_prefixes=["feature", "bugfix"]
        )
    )
    enforcer = PolicyEnforcer(config)
    
    # Valid workflow
    enforcer.validate_branch_name("feature/add-logging")
    enforcer.validate_commit_message("feat: add audit logging")
    
    # Invalid workflow
    try:
        enforcer.validate_branch_name("add-logging")
        assert False, "Should have raised PolicyViolation"
    except PolicyViolation:
        pass


def test_audit_logging_integration():
    """Test that audit logging works in a real scenario."""
    import tempfile
    from git_workflow_automator.audit import AuditLogger
    
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        git_dir = repo_path / ".git"
        git_dir.mkdir()
        
        logger = AuditLogger(repo_path)
        
        # Simulate a workflow
        logger.log("start", "Created branch", {"branch": "feature/test"}, status="dry_run")
        logger.log("commit", "Committed changes", {"files": 3}, status="success")
        logger.log("sync", "Synced with remote", status="success")
        logger.log("pr", "Created PR", {"pr_number": 123}, status="success")
        
        # Verify logs
        entries = logger.read_logs()
        assert len(entries) == 4
        assert entries[0]["command"] == "start"
        assert entries[3]["command"] == "pr"
        assert entries[3]["details"]["pr_number"] == 123
        
        # Test limit parameter
        recent = logger.read_logs(limit=2)
        assert len(recent) == 2
        assert recent[0]["command"] == "sync"
