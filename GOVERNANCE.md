# Governance

This prototype uses a lightweight maintainer model appropriate for a small portfolio repository.

## Decision Making

- The core maintainer approves architectural changes and release readiness.
- Feature proposals should be discussed in an issue before implementation when they change scope materially.
- Small fixes and documentation improvements may be merged directly when they preserve the existing design.

## Roles

- **Core maintainer**: owns repository direction, reviews structural changes, and decides when the prototype is complete enough for presentation.
- **Contributors**: submit focused improvements, bug fixes, and documentation updates.
- **Reviewers**: validate behavior, reproducibility, and clarity of presentation.

## Working Principles

- Keep the project synthetic, generic, and reproducible.
- Avoid hidden assumptions or dataset-specific special cases.
- Treat documentation and tests as part of the product, not optional extras.
- Prefer stable, comprehensible interfaces over premature optimization.