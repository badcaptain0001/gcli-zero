"""Tests for audit logging."""

import json
from pathlib import Path
import tempfile

from git_workflow_automator.audit import AuditLogger


def test_audit_logger_creates_directory():
    """Test that audit logger creates .git/gwa directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        git_dir = repo_path / ".git"
        git_dir.mkdir()
        
        logger = AuditLogger(repo_path)
        assert logger.log_dir.exists()
        assert logger.log_file.parent.exists()


def test_audit_logger_writes_jsonl():
    """Test that audit logger writes valid JSONL."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        git_dir = repo_path / ".git"
        git_dir.mkdir()
        
        logger = AuditLogger(repo_path)
        logger.log("start", "Created branch feature/test", {"branch": "feature/test"})
        logger.log("commit", "Committed changes", {"files": 3}, status="success")
        
        assert logger.log_file.exists()
        
        entries = logger.read_logs()
        assert len(entries) == 2
        assert entries[0]["command"] == "start"
        assert entries[1]["command"] == "commit"
        assert entries[0]["status"] == "success"


def test_audit_logger_handles_errors():
    """Test that audit logger handles error logging."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        git_dir = repo_path / ".git"
        git_dir.mkdir()
        
        logger = AuditLogger(repo_path)
        logger.log("sync", "Failed to sync", status="failure", error="Remote not found")
        
        entries = logger.read_logs()
        assert entries[0]["status"] == "failure"
        assert "error" in entries[0]
