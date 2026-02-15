# Copilot Instructions for git-workflow-automator

## Build, Test, and Lint

### Installation
```bash
pip install -e .
# With dev dependencies
pip install -e '.[dev]'
```

### Running Tests
```bash
# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run a single test file
pytest tests/test_config.py

# Run a single test function
pytest tests/test_config.py::test_default_config

# Run tests with coverage
pytest --cov=git_workflow_automator --cov-report=term-missing
```

### CLI Usage
```bash
# Main command
gwa

# Show help
gwa --help

# Dry run mode (for testing commands without execution)
gwa --dry-run <command>

# Verbose output
gwa -v <command>
```

## Architecture

### Core Components

**Configuration System** (`config.py`)
- Uses Pydantic for validation with strict type checking
- Config is loaded from `.gwa.toml` (TOML format)
- Three policy sections: `branch`, `commit`, `pr`
- Python 3.11+ uses built-in `tomllib`, earlier versions use `tomli`
- Missing config files return default values (no errors)

**Policy Enforcement** (`policy.py`)
- `PolicyEnforcer` validates branch names and commit messages against loaded config
- Raises `PolicyViolation` exception on validation failures
- Branch validation checks: protected branch names, required prefixes
- Commit validation checks: subject length, conventional commits format, allowed types

**Audit Logging** (`audit.py`)
- Logs to `.git/gwa/audit.jsonl` (JSONL format, one entry per line)
- Each entry includes: timestamp (UTC ISO format), command, action, status, user, details
- Status values: `success`, `failure`, `dry_run`
- Log directory is created automatically if missing

**CLI** (`cli.py`)
- Command pattern: each command has a `cmd_<name>` function
- All commands support `--dry-run` and `--verbose` flags
- Available commands: `init`, `start`, `commit`, `sync`, `pr`, `doctor`
- Command aliases supported (e.g., `/init`)

### Module Relationships
```
cli.py → config.py → policy.py
              ↓
         audit.py
```

## Key Conventions

### Configuration Files
- Config file is always named `.gwa.toml` at repository root
- Config follows pydantic models: `BranchPolicy`, `CommitPolicy`, `PRPolicy`
- Nested structure with three top-level sections: `[branch]`, `[commit]`, `[pr]`

### Policy Validation
- Branch names must include prefix separator: `feature/my-branch` not `feature-my-branch`
- Conventional commit regex pattern is constructed dynamically from `allowed_types`
- Scope format: `type(scope): message` when `require_scope=true`

### Testing Patterns
- Use `pytest.raises(ValidationError)` for pydantic validation tests
- Use `tempfile.TemporaryDirectory()` for file system tests
- Test function naming: `test_<module>_<specific_case>`
- Assertions should check both positive cases and error messages

### Python Compatibility
- Minimum Python 3.8 (specified in `pyproject.toml`)
- Handle `tomllib` import: `if sys.version_info >= (3, 11)` fallback to `tomli`
- Type hints use modern syntax: `list[str]` not `List[str]`, `dict[str, Any]` not `Dict[str, Any]`

### CLI Command Structure
- All command functions accept `args` parameter from argparse
- Commands return integer exit code (0 for success)
- Use `hasattr(args, 'attr')` checks before accessing optional arguments
- Dry-run mode prints `[DRY RUN]` prefix, execution mode prints `[EXECUTING]`
