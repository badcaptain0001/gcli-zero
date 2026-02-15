"""Configuration management with pydantic validation."""

import sys
from pathlib import Path
from typing import Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel, Field, field_validator


class BranchPolicy(BaseModel):
    """Branch naming and management policies."""
    
    prefix_required: bool = Field(default=False, description="Require branch prefix")
    allowed_prefixes: list[str] = Field(default_factory=lambda: ["feature", "bugfix", "hotfix"])
    main_branch: str = Field(default="main", description="Main branch name")
    protected_branches: list[str] = Field(default_factory=lambda: ["main", "master"])


class CommitPolicy(BaseModel):
    """Commit message policies."""
    
    conventional_commits: bool = Field(default=True, description="Enforce conventional commits")
    allowed_types: list[str] = Field(default_factory=lambda: ["feat", "fix", "docs", "style", "refactor", "test", "chore"])
    require_scope: bool = Field(default=False, description="Require scope in commit message")
    max_subject_length: int = Field(default=72, ge=1)
    
    @field_validator("max_subject_length")
    @classmethod
    def validate_max_length(cls, v):
        if v < 10:
            raise ValueError("max_subject_length must be at least 10")
        return v


class PRPolicy(BaseModel):
    """Pull request policies."""
    
    require_description: bool = Field(default=True)
    auto_assign: bool = Field(default=False)
    draft_by_default: bool = Field(default=False)


class Config(BaseModel):
    """Root configuration model."""
    
    branch: BranchPolicy = Field(default_factory=BranchPolicy)
    commit: CommitPolicy = Field(default_factory=CommitPolicy)
    pr: PRPolicy = Field(default_factory=PRPolicy)


def load_config(path: Optional[Path] = None) -> Config:
    """Load and validate configuration from .gwa.toml."""
    if path is None:
        path = Path.cwd() / ".gwa.toml"
    
    if not path.exists():
        return Config()
    
    with open(path, "rb") as f:
        data = tomllib.load(f)
    
    return Config(**data)
