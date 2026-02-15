# GitHub Copilot CLI Challenge Submission

## Project Name

Git Workflow Automator (GWA)

## Repository

https://github.com/badcaptain0001/gcli-zero

## What I Built

I built **Git Workflow Automator (GWA)**, a terminal-first CLI that streamlines daily Git workflows.

Current commands:

- `gwa start`
- `gwa commit`
- `gwa sync`
- `gwa pr`
- `gwa doctor`

## Why I Built This

Git workflows are repetitive and easy to get wrong under time pressure.  
This tool gives one consistent CLI surface for common branch/commit/sync/PR/health actions.

## How to Run

```bash
git clone https://github.com/badcaptain0001/gcli-zero.git
cd gcli-zero
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -e '.[dev]'
pytest -q
gwa --help
```

## Copilot CLI Prompts I Used

```text
1) Scaffold a Python CLI project from scratch named git-workflow-automator with src package layout, tests folder, pyproject.toml, and a console script named gwa. Output shell commands only.

2) Generate minimal starter code for the package and CLI entrypoint using argparse.

3) Add commands start, commit, sync, pr, and doctor with dry-run support.

4) Create pydantic-based configuration loading from .gwa.toml with sensible defaults.

5) Add policy enforcement for branch naming and conventional commit message validation.

6) Add JSONL audit logging under .git/gwa/audit.jsonl with timestamp, command, status, and metadata.

7) Create pytest tests for config, policy, audit, and a basic CLI integration flow.

8) Improve README with installation, usage, and testing instructions.
```

## How Copilot CLI Helped

Copilot CLI accelerated:

- project scaffolding,
- initial command/module generation,
- policy/audit baseline implementation,
- test and documentation bootstrapping.

I manually reviewed and refined outputs for:

- command behavior,
- consistency across modules,
- test reliability,
- usability and clarity.

Detailed prompt-by-prompt notes are in `COPILOT_LOG.md`.

## Judging Criteria Mapping

### Use of GitHub Copilot CLI

- Copilot CLI was used throughout scaffolding, implementation, tests, and docs.
- Prompt evidence is documented above and in `COPILOT_LOG.md`.

### Usability and User Experience

- Simple command interface and clear output.
- Includes workflow commands and diagnostics in one tool.

### Originality and Creativity

- Practical Git workflow automation focused on real terminal pain points.
- Built iteratively with Copilot CLI + manual hardening.

## Testing / Validation

I validated the project with:

```bash
pytest -q
```

Current status: **all tests passing**.
