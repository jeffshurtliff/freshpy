# AGENTS.md

Instructions for coding agents (Codex, etc.) working in this repository.

## Project overview

This repository contains `freshpy`, a Python package/toolset for interacting with Freshservice APIs.

Primary goals when making changes:
- Keep the public API stable unless the change explicitly requires a breaking change.
- Prefer small, testable changes.
- Keep docs and docstrings consistent and Sphinx-friendly.

## Dev environment

Use Poetry for dependency management and packaging.

Common commands (prefer these unless the user asks otherwise):
- Install: `poetry install`
- Run tests: `poetry run pytest`
- Lint/format (if configured in this repo): `poetry run ruff check .` and `poetry run ruff format .`
- Build: `poetry build`

If you add a dependency, add it via Poetry (`poetry add ...` / `poetry add --group dev ...`) rather than editing `pyproject.toml` by hand.

## Coding style

- Prefer clarity over cleverness.
- Keep functions small and focused.
- Avoid unnecessary abstraction.
- Keep changes localized; don’t reformat unrelated code.
- Use type hints where they improve readability and tooling, especially for public APIs.

## Docstrings (PEP 257 + Sphinx/reST)

### PEP 257 essentials (what “good” looks like)
Follow PEP 257 conventions:
- Use triple double-quotes: """..."""
- One-line docstrings:
  - The summary is on one line and ends with a period.
  - Example: """Return the API version string."""
- Multi-line docstrings:
  - First line is a short summary (imperative mood is fine), ending with a period.
  - Blank line after the summary.
  - Then a more detailed description if needed.
- Docstrings describe “what/why”; code should show “how”.
- Keep docstrings updated when behavior changes.

### Sphinx/reST field list style (required)
Use Sphinx/reST field lists for parameters and returns:

- :param <name>: ...
- :type <name>: ... (only if the type is non-obvious or you’re not using type hints consistently)
- :returns: ...
- :rtype: ... (only if needed; type hints usually suffice)
- :raises <ExceptionType>: ...

If type hints are present and clear, you may omit :type: and :rtype:.

### Function/method docstring template
```python
def example(name: str, enabled: bool = True) -> int:
    """Compute the example value.

    Longer explanation if needed.

    :param name: The user-facing name to process.
    :param enabled: Whether to enable additional processing.
    :returns: The computed example value.
    :raises ValueError: If `name` is empty.
    """
```

### Package / module docstrings (including __init__.py)

#### Module docstrings (some_module.py)
Every public module should start with a module docstring describing purpose and key concepts:

```
"""Freshservice REST helpers.

This module contains low-level request/response helpers used by the core client.
"""
```

#### Package docstrings (__init__.py)
If src/freshpy/__init__.py exposes the public API (re-exports classes/functions),
include a package docstring that explains the package purpose and lists key exports.

```
"""Top-level package for freshpy.

This package provides the :class:`freshpy.FreshPy` client and related helpers.
"""
```

If __init__.py only marks a package and exports nothing meaningful, keep the docstring short
(or omit it).

### Class docstrings vs __init__ docstrings (important rule)

#### Preferred approach for user-facing classes
For user-facing classes, document constructor parameters in the class docstring (not duplicated in __init__), using :param: fields.

```python
class FreshPy:
    """Freshservice API client.

    :param domain: Base instance domain (e.g. https://servicedesk.example.com)
    :param api_key: API key
    """
    def __init__(
        self,
        domain: str,
        api_key: str,
    ) -> None:
        """Initialize the client.

        Parameter documentation is defined on the class docstring.
        """
```

#### When __init__ should have full :param: docs
Only put full :param: documentation on __init__ if:
- the class docstring is intentionally minimal, or
- the class is internal/private and only __init__ needs documentation, or
- you need to document multiple alternative init signatures/behaviors that are clearer at __init__.

### Properties
Use property docstrings as short descriptions. Avoid :param: fields (properties take no params).

```python
@property
def api_version(self) -> str:
    """The Freshservice API version in use."""
```

## Tests

- Add or update tests for behavior changes.
- Prefer pytest-style tests.
- Keep tests deterministic (no real network calls unless explicitly requested).

## Documentation expectations

- If you change a public behavior, update the docstrings and any relevant docs under docs/ (always the changelog.rst file).
- When creating a new module, a header block similar to the example below should be included.

```python
# -*- coding: utf-8 -*-
"""
:Module:            freshpy.new_module_name
:Synopsis:          Defines the functionality related to ????
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     31 Dec 2025
"""
```

- If you change any file with a header block containing `Last Modified` or `Modified Date` fields:
  - Update the `Last Modified` field with the name (or username/pseudonym) of the person making the change.
    - The person making the change indicates the human user who is orchestrating the AI-generated changes.
    - If the person does not wish to display their name/username/pseudonym, use "Anonymous" as a default value.
  - Update the `Modified Date` field where applicable with the current date (local time) in the same format as the existing value.
- Keep examples accurate and runnable.

## PR / commit hygiene (if applicable)

- Keep commits focused and descriptive and prefer past-tense over present-tense. ("Updated the ..." over "Update the ...")
- Explicitly mention the file name if it fits organically and does not distract from the commit message itself.
- Avoid large refactors unless requested.
- Don’t change formatting in unrelated files.
