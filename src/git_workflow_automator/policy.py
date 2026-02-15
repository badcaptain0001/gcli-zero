"""Policy enforcement for git workflows."""

import re
from typing import Optional

from .config import Config


class PolicyViolation(Exception):
    """Exception raised when a policy is violated."""
    pass


class PolicyEnforcer:
    """Enforces workflow policies based on configuration."""
    
    def __init__(self, config: Config):
        self.config = config
    
    def validate_branch_name(self, branch_name: str) -> None:
        """Validate branch name against policy.
        
        Args:
            branch_name: The branch name to validate
            
        Raises:
            PolicyViolation: If branch name violates policy
        """
        # Check protected branches
        if branch_name in self.config.branch.protected_branches:
            raise PolicyViolation(f"Cannot create branch with protected name: {branch_name}")
        
        # Check prefix requirement
        if self.config.branch.prefix_required:
            has_valid_prefix = any(
                branch_name.startswith(f"{prefix}/")
                for prefix in self.config.branch.allowed_prefixes
            )
            if not has_valid_prefix:
                raise PolicyViolation(
                    f"Branch name must start with one of: {', '.join(self.config.branch.allowed_prefixes)}"
                )
    
    def validate_commit_message(self, message: str) -> None:
        """Validate commit message against policy.
        
        Args:
            message: The commit message to validate
            
        Raises:
            PolicyViolation: If commit message violates policy
        """
        lines = message.split("\n")
        subject = lines[0] if lines else ""
        
        # Check subject length
        if len(subject) > self.config.commit.max_subject_length:
            raise PolicyViolation(
                f"Commit subject exceeds {self.config.commit.max_subject_length} characters"
            )
        
        # Check conventional commits format
        if self.config.commit.conventional_commits:
            if self.config.commit.require_scope:
                pattern = r'^(' + '|'.join(self.config.commit.allowed_types) + r')\(.+\): .+'
            else:
                pattern = r'^(' + '|'.join(self.config.commit.allowed_types) + r')(\(.+\))?: .+'
            
            if not re.match(pattern, subject):
                raise PolicyViolation(
                    f"Commit message must follow conventional commits format. "
                    f"Allowed types: {', '.join(self.config.commit.allowed_types)}"
                )
