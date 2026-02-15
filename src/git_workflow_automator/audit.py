"""Audit logging for git workflow operations."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class AuditLogger:
    """JSONL audit logger for tracking workflow operations."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize audit logger.
        
        Args:
            repo_path: Path to git repository root. Defaults to current directory.
        """
        if repo_path is None:
            repo_path = Path.cwd()
        
        self.log_dir = repo_path / ".git" / "gwa"
        self.log_file = self.log_dir / "audit.jsonl"
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Create log directory if it doesn't exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log(self, command: str, action: str, details: Optional[dict[str, Any]] = None, 
            status: str = "success", error: Optional[str] = None):
        """Write an audit log entry.
        
        Args:
            command: The CLI command executed (e.g., 'start', 'commit')
            action: Description of the action taken
            details: Additional context and metadata
            status: Operation status ('success', 'failure', 'dry_run')
            error: Error message if status is 'failure'
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "command": command,
            "action": action,
            "status": status,
            "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
            "details": details or {},
        }
        
        if error:
            entry["error"] = error
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def read_logs(self, limit: Optional[int] = None) -> list[dict[str, Any]]:
        """Read audit log entries.
        
        Args:
            limit: Maximum number of recent entries to return
            
        Returns:
            List of log entries as dictionaries
        """
        if not self.log_file.exists():
            return []
        
        entries = []
        with open(self.log_file, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        if limit:
            return entries[-limit:]
        return entries
