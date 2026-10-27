# Project Guidelines

## Project context
- This repository is a Python automation testing portfolio project.
- Main technologies: Python 3.13, pytest, Playwright, uv, Pydantic, and Ruff.
- The primary focus is learning Playwright and AI-assisted development.

## Architecture
- Follow the existing project structure and conventions.
- Keep UI interactions in existing Page Objects and components.
- Keep API clients focused on HTTP operations, not test assertions.
- Reuse existing pytest fixtures where appropriate.
- Avoid unnecessary abstractions and overengineering.

## Working rules
- Inspect relevant code before proposing changes.
- Prefer minimal, focused changes.
- Do not modify unrelated files.
- Do not add dependencies without approval.
- Clearly distinguish verified findings from assumptions.
- Explain proposed changes and show the diff.

## Validation
- Run relevant existing tests when the environment is ready.
- Report test results accurately; never claim unexecuted tests passed.
- Do not start or reset Docker containers or databases without approval.
- Do not commit or push changes unless explicitly requested.