# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-08

### Added

- Test level rules TST-001 to TST-006: five levels with one definition each, after the meanings of the ISTQB Glossary; what each level may replace with a test double; a balance toward the lowest level; repeatable tests; tests of business rules through their own interface, with no rules engine assumed; any language and tools.
- Unit and integration test rules TST-010 to TST-017: isolation, an injected clock and random source, one behavior per test, real dependency products, own data per test, cleanup and no shared environments.
- Functional test and BDD rules TST-020 to TST-029: Gherkin scenarios as the start of every functional test, written with domain experts; one behavior per scenario; declarative steps with no interface or implementation detail; When and Then steps, Background, Scenario Outline and Rule; identifying tags; domain terms; public interfaces only. A comparison with GovStack.
- Feature file rules TST-030 to TST-036: an English and a French version of each feature file, with one keyword per element from the official Gherkin dialects, the same structure and untranslated data; a parser check in the continuous integration; both versions run; no description on a scenario or a background.
- Contract and conformance rules TST-040 to TST-048: tests against the published API description, a breaking-change check, consumer-driven contracts, event schemas, conformance suites tied to the specification version, and results that are not a certification.
- Test data rules TST-050 to TST-057: synthetic data only in repositories, continuous integration and shared test environments, generated from the data models with a fixed seed; reserved telephone numbers and domains; no value from a real record; data in English and French with accents, apostrophes and names of one part, one character and 100 characters; exact comparison; identifiers with a check digit from never-assigned ranges.
- Continuous integration rules TST-060 to TST-066: each level as a required check, failing tests that block a merge, flaky tests quarantined with an issue and a deadline, coverage reported but not the only gate, functional tests against a built artifact, and pointers to the accessibility and future security specifications.
- An example feature in English and in French, `examples/features/`, for a Party rule of the data models specification, with synthetic data.
- The Gherkin check `examples/check-features.py`, with the parser pinned in `examples/requirements.txt`, and its tests `examples/test-features.sh` with broken files that it must reject.
- A `gherkin` job in the continuous integration that runs these tests.
- Comparison data for twelve topics, with Canada and Québec rows.
- How-to guide that writes a feature in English and in French and checks it.

[Unreleased]: https://github.com/fpsot-org/fpsot-spec-testing/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fpsot-org/fpsot-spec-testing/releases/tag/v0.1.0
