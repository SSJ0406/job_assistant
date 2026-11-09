# Repository Guidelines

## Project Structure & Module Organization

This Python project is a Streamlit application. `main.py` is the application entry point, reusable code is in `job_assistant/`, and automated tests are in `tests/`. `.venv/` is the local virtual environment; do not commit or edit its generated contents.

## Build, Test, and Development Commands

Run commands from the project root. On Windows PowerShell, start the Streamlit app with `.\run_app.ps1`. To run the existing test suite, activate the local environment with `.\.venv\Scripts\Activate.ps1`, then run `python -m unittest discover -s tests`. No separate build system is configured.

## Coding Style & Naming Conventions

Use Python 3, four spaces for indentation, `snake_case` for modules, functions, and variables, and `PascalCase` for classes. Keep functions focused and add type hints when they clarify interfaces. No formatter or linter is configured; keep changes PEP 8-compatible and avoid adding tooling without recording how to run it.

## Testing Guidelines

Tests are located in `tests/` and use `unittest`; name new files `test_*.py` and cover new behavior and relevant edge cases. Run the suite with `python -m unittest discover -s tests`.

## Commit & Pull Request Guidelines

This directory has no Git history, so no established commit convention can be confirmed. Use concise imperative commit subjects (for example, `Add input validation`). Pull requests should explain the change and how it was checked, link related issues when available, and include screenshots only for user-facing visual changes.

## Security & Configuration

Keep secrets, local environment files, and virtual-environment contents out of source control. If dependencies are introduced, record them in a dependency manifest so contributors can reproduce the setup.

## Explicit Approval Protocol

Every specific implementation requires the user's explicit approval before work begins. First inspect the relevant files, project structure, conventions, tests, and working tree. Then describe the problem, proposed solution, files to change, expected project impact, risks, and test plan. Read-only inspection is allowed before approval; without approval, do not modify code, tests, or configuration. A general request, discussion, or lack of response is not approval.

Approval applies only to the proposal as described. Ask again if the implementation scope materially changes. Package installation, dependency changes, migrations, external data or service changes, commits, pushes, and deployments require separate approval. Preserve existing user changes; do not discard work or rewrite Git history.

## Implementation Scope & Change Management

Implement only the approved scope. Separate changes that are required to meet the request from those necessary to complete it safely, and keep optional improvements as suggestions unless approved. Do not add unrelated changes, features, or refactoring. If an unexpected issue requires a broader change, stop and request approval. Preserve existing behavior and public interfaces unless the approved scope explicitly changes them.

## Design & Code Quality

Prefer simple, explicit solutions that fit the current project. Keep functions and classes focused, use descriptive names, avoid hidden side effects, and comment on reasons or constraints rather than restating code. Apply SOLID, DRY, and other design principles pragmatically; avoid premature abstractions, unnecessary layers, dependencies, and hypothetical features. Keep domain logic separate from infrastructure when the project needs that boundary. Refactoring should preserve behavior and stay within the approved scope.

## Object-Oriented Design & SOLID

Use object-oriented design when it clarifies responsibilities or domain concepts. Apply SOLID pragmatically: give each class one clear responsibility (SRP); allow behavior to be extended without needless changes to stable code (OCP); keep subclasses compatible with their base types (LSP); prefer small, focused interfaces (ISP); and make high-level logic depend on suitable abstractions rather than concrete infrastructure (DIP). Prefer composition over inheritance unless a genuine "is-a" relationship exists. Encapsulate internal state and expose only the interface callers need. Use dependency injection when it makes dependencies explicit and improves testability. Avoid abstractions and design patterns without a concrete need.

## Test Quality & Validation

Include an appropriate test strategy in each implementation proposal. Cover expected behavior (happy paths), edge cases, invalid inputs, error handling, and regressions. Test observable behavior rather than implementation details. Keep tests deterministic, isolated, independent, and readable; avoid excessive mocking and do not change tests merely to hide implementation failures. Use the existing test framework, or propose one before introducing it. Run relevant checks within the approved scope and report exactly which tests ran and their results. Never claim success for checks that were not executed.

## Error Handling & Logging

Handle expected errors clearly, preserve useful context, and avoid swallowing exceptions. Use the project's logging approach and never log secrets or sensitive data.

## Security, Data & Integrations

Validate untrusted input at system boundaries. Protect credentials, use parameterized database queries, and apply least privilege. Keep external services behind clear interfaces, use timeouts, validate responses, and handle rate limits and failures. Explain data integrity, transaction, compatibility, and rollback considerations for proposed database changes. Changes that send messages, publish content, make payments, alter external records, or otherwise write to external systems need explicit approval.

## Documentation, Git & Completion

Update documentation only when it is needed for the approved change. Follow the existing Git workflow; do not create commits, push, deploy, modify Git configuration, or rewrite history without explicit approval. When reporting completed work, summarize what changed and why, list affected files, explain key decisions, state tests and checks actually run, and note anything that remains unverified. Never claim a check passed unless it did.

## Code Review & Quality Gates

Before reporting an implementation complete, review the full change set. Check that it meets the approved requirements, follows the existing architecture, and applies SOLID, DRY, KISS, and Clean Code appropriately. Look for unrelated edits, unnecessary dependencies or abstractions, security issues, and regressions. Report remaining problems and anything that could not be verified; do not declare success when required checks have not passed or were not run.

## Specialized Work

For database, external API, AI/ML, or other specialized work, keep those concerns isolated, make configuration explicit, and address the domain-specific risks before implementation. For AI features, treat retrieved or generated content as untrusted, validate outputs, and consider privacy, prompt injection, reproducibility, and evaluation. Do not add architecture, dependencies, or security-sensitive behavior without a clear need and approval.
