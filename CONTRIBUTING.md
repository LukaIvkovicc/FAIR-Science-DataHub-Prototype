# Contributing

This repository is meant to stay small, readable, and easy to verify.

## Development Goals

- Keep the code generic and synthetic-data-only.
- Prefer clear, local changes over large abstractions.
- Preserve the current working vertical slice: ingest, validate, persist, serve, export.
- Update tests when behavior changes.

## Recommended Workflow

1. Create a focused branch for the change.
2. Make the smallest possible edit that solves the problem.
3. Run the relevant tests locally.
4. Update documentation when a user-facing behavior changes.
5. Keep commit messages and pull requests concise and descriptive.

## Review Expectations

- Code should be easy to read without prior context.
- Data and examples should remain synthetic.
- Any new endpoint or service behavior should include a test.
- If a change affects installation or runtime behavior, update the README and architecture docs.

## Style

- Use standard Python formatting and type hints where they clarify intent.
- Prefer explicit names over clever shortcuts.
- Keep public API responses stable unless there is a strong reason to change them.