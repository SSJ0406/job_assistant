# Code Review Guidelines

## 1. Purpose

Perform code reviews with a strong focus on correctness, maintainability, security, reliability, and architectural quality.

The primary goal is to identify actionable issues that could negatively affect the software.

Review code objectively. Do not treat personal preferences, stylistic differences, or theoretical concerns as defects.

Prioritize correctness and meaningful risks over cosmetic improvements.

## 2. General Review Principles

- Review the actual changes introduced by the current diff.
- If no diff is available, review the project present in the current workspace and state that the review covers the workspace snapshot. Do not imply that findings were introduced by a diff when that cannot be established.
- Consider the surrounding code and existing architecture when necessary.
- Do not assume that code is incorrect without sufficient evidence.
- Do not report issues that cannot be reasonably demonstrated.
- Avoid unnecessary refactoring suggestions unrelated to the reviewed changes.
- Do not recommend introducing abstractions, design patterns, or additional dependencies without a clear benefit.
- Prefer simple, readable, and maintainable solutions.
- Preserve existing conventions unless they introduce a meaningful problem.
- Do not modify code during a review unless explicitly requested.

## 3. Review Priorities

Classify findings according to their severity.

### P0 — Critical

Issues that can cause catastrophic failures, severe security vulnerabilities, or critical data loss.

Examples:
- Remote code execution vulnerabilities.
- Unrecoverable data corruption.
- Critical authentication or authorization bypasses.

### P1 — High

Issues that significantly affect functionality, security, reliability, or important business requirements.

Examples:
- Incorrect business logic affecting important workflows.
- Missing authorization checks.
- Major regressions.
- Incorrect handling of critical data.

### P2 — Medium

Issues that should be fixed but do not represent an immediate critical failure.

Examples:
- Incorrect behavior in specific edge cases.
- Missing validation that can lead to invalid application state.
- Significant maintainability problems that increase the risk of defects.
- Missing tests for important behavior.

### P3 — Low

Minor issues with limited impact.

Examples:
- Small readability problems.
- Minor inefficiencies.
- Non-critical inconsistencies.

Do not report purely stylistic preferences as findings.

## 4. Correctness and Functionality

Verify that the implementation:

- Correctly implements the intended behavior.
- Handles expected inputs and edge cases.
- Does not introduce regressions.
- Maintains data consistency.
- Handles errors appropriately.
- Does not silently ignore important failures.
- Uses appropriate defaults.
- Correctly handles `None`, empty collections, invalid inputs, and unexpected states.
- Does not introduce unintended side effects.

Pay particular attention to:

- Off-by-one errors.
- Incorrect conditional logic.
- Incorrect assumptions about input data.
- Unexpected mutation of shared state.
- Incorrect exception handling.
- Resource leaks.
- Race conditions and concurrency issues.

## 5. Clean Code and Maintainability

Evaluate the code according to the following principles.

### Readability

- Code should communicate its intent clearly.
- Names should describe the purpose of variables, functions, classes, and modules.
- Avoid unnecessarily complex expressions.
- Avoid deeply nested conditionals.
- Prefer explicit and understandable control flow.
- Avoid misleading names and unnecessary abbreviations.

### Functions and Methods

- Functions should have a clear and cohesive responsibility.
- Avoid unnecessarily large functions.
- Avoid excessive numbers of parameters.
- Avoid boolean parameters that significantly change a function's behavior when a clearer alternative exists.
- Avoid hidden side effects.
- Prefer explicit inputs and outputs.

Do not require every function to be extremely small. Evaluate its cohesion and readability in context.

### DRY — Don't Repeat Yourself

- Identify duplicated business logic.
- Recommend extracting shared logic when duplication creates a meaningful maintenance risk.
- Avoid introducing abstractions for coincidental similarities.
- Do not force unrelated code into a shared implementation.

### KISS — Keep It Simple

- Prefer straightforward implementations.
- Avoid unnecessary layers, abstractions, and indirection.
- Do not introduce complex solutions for simple problems.
- Prefer the simplest design that satisfies the requirements.

### YAGNI — You Aren't Gonna Need It

- Avoid speculative functionality.
- Avoid implementing hypothetical future requirements.
- Do not introduce unnecessary configuration options.
- Do not add unused abstractions or extension points.

## 6. Object-Oriented Programming and SOLID

Evaluate object-oriented design when it is relevant to the implementation.

### Single Responsibility Principle (SRP)

- Classes and modules should have cohesive responsibilities.
- Identify classes that combine unrelated business logic, infrastructure, persistence, or presentation concerns.
- Avoid splitting classes into unnecessarily small components.

### Open/Closed Principle (OCP)

- Prefer designs that can accommodate foreseeable changes without excessive modification of existing code.
- Do not introduce abstractions solely to satisfy OCP.
- Avoid speculative extensibility.

### Liskov Substitution Principle (LSP)

- Subclasses should preserve the behavioral contracts of their base classes.
- Identify implementations that violate expected behavior or introduce incompatible assumptions.

### Interface Segregation Principle (ISP)

- Prefer small, focused interfaces.
- Avoid forcing implementations to depend on methods they do not need.

### Dependency Inversion Principle (DIP)

- Separate high-level business logic from low-level implementation details when this improves architecture.
- Use dependency injection where it provides clear benefits for testability or flexibility.
- Avoid unnecessary dependency injection frameworks.

### Additional OOP Guidelines

- Prefer composition over inheritance when it results in a simpler design.
- Avoid deep inheritance hierarchies.
- Avoid classes that exist only to wrap a single function without a meaningful reason.
- Do not force OOP into code that is better expressed through simple functions or data structures.
- Use design patterns only when they solve an actual design problem.

## 7. Python-Specific Guidelines

Review Python code for idiomatic usage and compliance with established conventions.

### Style and Naming

- Follow PEP 8.
- Use `snake_case` for functions, methods, and variables.
- Use `PascalCase` for classes.
- Use `UPPER_CASE` for constants.
- Follow PEP 257 for docstrings when documentation is appropriate.

### Type Hints

- Use type hints for function signatures and important data structures.
- Prefer precise types over `Any` when practical.
- Avoid unnecessary complexity in type annotations.
- Use `Protocol`, `TypedDict`, `dataclasses`, and other typing features when they improve clarity or correctness.

### Python Best Practices

- Prefer context managers for resource management.
- Avoid mutable default arguments.
- Avoid unnecessary global state.
- Use comprehensions when they improve readability.
- Prefer explicit exception handling.
- Avoid bare `except:` clauses.
- Avoid catching exceptions only to suppress them.
- Use standard library functionality when it adequately solves the problem.

### Data Structures

- Choose data structures appropriate for the use case.
- Avoid unnecessary conversions and copies.
- Be aware of mutability and reference semantics.
- Avoid modifying objects unexpectedly.

### Python Style References

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/
- PEP 484: https://peps.python.org/pep-0484/

## 8. Architecture and Separation of Concerns

Evaluate whether the implementation respects the existing architecture.

- Keep business logic separate from infrastructure concerns.
- Avoid unnecessary coupling between modules.
- Avoid circular dependencies.
- Keep responsibilities clear across architectural layers.
- Ensure that dependencies flow in a consistent direction.
- Avoid leaking implementation details between layers.
- Avoid introducing unnecessary architectural complexity.

For applications involving APIs, databases, machine learning, or AI agents:

- Keep external service interactions isolated where appropriate.
- Avoid embedding business logic directly into API handlers.
- Avoid coupling domain logic to specific infrastructure implementations.
- Keep configuration separate from application logic.
- Ensure that external dependencies can be tested or replaced when necessary.

Do not require a specific architecture unless the project explicitly defines one.

## 9. Testing

Review whether the changes are adequately tested.

- New functionality should include appropriate tests.
- Bug fixes should include regression tests when practical.
- Tests should verify behavior rather than implementation details.
- Important edge cases should be covered.
- Error handling should be tested.
- Tests should be deterministic.
- Avoid unnecessary mocking.
- Avoid tests that depend on external services unless explicitly intended.
- Avoid weakening existing tests to accommodate incorrect behavior.

Consider:

- Unit tests.
- Integration tests.
- Regression tests.
- Boundary conditions.
- Invalid inputs.
- Failure scenarios.

Do not require tests for trivial changes when the testing benefit is negligible.

Do not claim that tests passed unless they were actually executed.

## 10. Security

Identify security vulnerabilities introduced or exposed by the changes.

Review:

- Input validation.
- Authentication and authorization.
- Sensitive information handling.
- Secrets and credentials.
- SQL injection.
- Command injection.
- Path traversal.
- Unsafe deserialization.
- Insecure file handling.
- Improper error messages.
- Dependency vulnerabilities when supported by available evidence.

Never recommend hardcoding credentials, API keys, or secrets.

Do not report speculative security concerns without a plausible attack scenario.

## 11. Performance and Resource Management

Identify meaningful performance or resource-management problems.

Review:

- Unnecessary database queries.
- N+1 query patterns.
- Inefficient algorithms.
- Unnecessary repeated computations.
- Excessive memory usage.
- Unnecessary data copying.
- Blocking operations in asynchronous code.
- Resource leaks.
- Inefficient loops over large datasets.

Do not recommend micro-optimizations without a meaningful expected benefit.

Prefer correctness and maintainability over premature optimization.

## 12. Documentation and Comments

- Ensure that documentation remains consistent with the implementation.
- Identify missing documentation for important public interfaces.
- Avoid unnecessary comments that merely restate the code.
- Prefer comments that explain reasoning, constraints, or non-obvious behavior.
- Identify misleading or outdated comments.
- Ensure that docstrings accurately describe behavior.

Do not require documentation for every private function or trivial implementation detail.

## 13. Code Review Findings

Every finding must be actionable and sufficiently specific.

A valid finding should:

1. Identify a concrete problem.
2. Explain why the problem matters.
3. Describe the circumstances under which it occurs.
4. Explain the potential impact.
5. Suggest a reasonable direction for fixing it when appropriate.

Avoid vague findings such as:

- "This code could be cleaner."
- "Consider improving the architecture."
- "This function is too long."
- "This might cause problems."

Instead, explain the actual issue and its consequences.

Do not report the same underlying issue multiple times.

Do not report issues that are already fixed in the current diff.

Do not report issues that are unrelated to the reviewed changes unless they are directly necessary to understand a regression.

## 14. Review Output Format

When performing a code review, use the following structure:

### Summary

Provide a brief overview of the reviewed changes and their general quality.

### Findings

For each finding, use the following format:

- **Priority:** P0 / P1 / P2 / P3
- **Location:** File and line number
- **Issue:** A concise description of the problem
- **Impact:** Why this matters
- **Recommendation:** A suggested direction for remediation

Findings should be ordered by severity, with the most important issues first.

If no actionable issues are identified, explicitly state:

"No actionable findings identified."

Do not invent findings to make the review appear more thorough.

### Testing

State which tests were executed, which were not executed, and any relevant limitations.

## 15. Final Review Checklist

Before completing the review, verify:

- [ ] The implementation satisfies the intended requirements.
- [ ] No significant functional defects were identified.
- [ ] Edge cases and error handling were considered.
- [ ] The code is readable and maintainable.
- [ ] DRY, KISS, and YAGNI were applied appropriately.
- [ ] SOLID principles were considered where relevant.
- [ ] The architecture remains consistent with the project.
- [ ] Tests adequately cover the changes.
- [ ] No significant security issues were identified.
- [ ] No meaningful performance regressions were identified.
- [ ] Documentation is consistent with the implementation.
- [ ] All findings are concrete, actionable, and supported by evidence.

## 16. Important Constraints

- Do not rewrite the entire implementation during a code review.
- Do not introduce new requirements.
- Do not enforce design principles mechanically.
- Do not treat personal preferences as defects.
- Do not recommend unnecessary abstractions or design patterns.
- Do not make unsupported assumptions.
- Do not claim that code, tests, or tools were executed when they were not.
- Focus on meaningful defects and improvements.
- Prefer a small number of high-quality findings over a large number of speculative comments.
