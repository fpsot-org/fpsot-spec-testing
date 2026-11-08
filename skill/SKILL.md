---
name: fpsot-testing
description: Testing rules for FPSOT projects. Use when writing or reviewing unit, integration, contract, functional or end-to-end tests, Gherkin feature files in English and French, conformance suites, test data or fixtures, or the test jobs of continuous integration.
---

# FPSOT testing

Summary of the FPSOT testing specification. It adds no rules of its own.
The spec text in `spec/` wins on any difference. Each line cites its requirement ID.
The example feature is in `examples/features/`, and its check is `examples/check-features.py`.

Each line keeps the strength of its rule: "must" and "must not" are MUST and MUST NOT, "should" and "should not" are SHOULD and SHOULD NOT, "may" is MAY.

## Test levels

- Each test must belong to one level (unit, integration, contract, functional, end-to-end), and the project must mark the level (TST-001).
- A test must not replace with a test double what its level runs for real; it may replace what the table of TST-002 allows. An end-to-end test that replaces an outside system must name it in its report (TST-002).
- Each behavior should be checked at the lowest level that can catch its faults; most tests should be unit tests, end-to-end tests the fewest (TST-003).
- A test must give the same result on each run, must not depend on order, other tests or the machine, and must not sleep for a fixed time; it must wait on a condition with a time limit (TST-004).
- A test of a business rule must use the rule's own interface, and must not depend on how the rule is built (plain code or a rules engine) (TST-005).
- A project may use any language, runner and framework; it should name its tools and versions per level in its repository (TST-006).

## Unit and integration tests

- A unit test must run in isolation: no network, shared database or file outside its temporary folder; each outside dependency must be a test double (TST-010).
- Code that reads the clock, random values or the default time zone must receive them from outside, and unit tests must supply fixed values; a zone must be a time zone database name, under DAT-030 (TST-011).
- A unit test should check one behavior; its name must state the behavior and its result (TST-012).
- Unit tests should be fast enough to run before each commit; a slow one should move to integration or replace its slow dependency (TST-013).
- An integration test must use the real product of each dependency it names, at its production version, and should start it for the run, such as in a container; an in-memory stand-in must not count (TST-014).
- Each integration test must create its own data and must not rely on another test's data; it should use unique identifiers (TST-015).
- An integration test must leave each dependency as it found it, unless the dependency exists for it alone (TST-016).
- An integration test must not reach a shared or production system; it must use only dependencies that the test run starts and controls (TST-017).

## Functional tests and BDD

- Each functional test must start from a Gherkin scenario, in feature files in the product repository beside the code (TST-020).
- Scenarios should be written with domain experts before the code; a domain expert, a developer and a tester should take part; a domain expert should review each change (TST-021).
- A scenario must check one behavior, and its name must state it (TST-022).
- Steps must state what happens in domain terms; they must not hold UI details (page, button, click) or implementation details (HTTP method, table, class name) (TST-023).
- Each scenario must have at least one When and one Then step; it should have one action only (TST-024).
- A Background must hold only Given steps that every scenario needs, and should stay short (TST-025).
- A Scenario Outline should check one behavior with several data sets, and must not check different behaviors with its rows; a Rule should group the scenarios of one business rule (TST-026).
- Each scenario must carry a unique identifying tag; tags must be English kebab-case (NAM-001, NAM-010); group tags should name a part of the domain (TST-027).
- Steps must use the terms of the domain glossary and the data models, one term per concept; codes must be the vocabulary codes, such as `person` (TST-028).
- A functional test must use only the public interfaces of the product, and must not call internal code or touch its database (TST-029).

## Feature files in English and French

- Each feature file must exist in English and French, with the same English kebab-case file name in `features/en/` and `features/fr/` (TST-030).
- The first line must be `# language: en` or `# language: fr`; files must use only these keywords: Feature/Fonctionnalité, Background/Contexte, Rule/Règle, Scenario/Scénario, Scenario Outline/Plan du scénario, Examples/Exemples, Given/Étant donné, When/Quand, Then/Alors, And/Et, But/Mais (TST-031).
- Both versions must have the same structure: rules, scenarios, examples, order, tags, number and kinds of steps, data table cells and Examples rows (TST-032).
- Test data must not be translated; a change to one version must change the other in the same pull request; French must follow OQLF usage (WRT-031) and must not be raw machine translation (WRT-033) (TST-033).
- CI must parse every feature file with an official Gherkin parser, fail on a parse error, and check TST-031 and TST-032; the check should be tested with broken files (TST-034).
- CI must run both versions; the step definitions of both languages must call the same code (TST-035).

## Contract tests and conformance suites

- An API provider must test its server against the published description (API-020, API-021); responses must match the schema; tests should call each operation and status code (TST-040).
- CI must compare the description with the last release and fail on a breaking change (API-051), except with a new major version (API-050) (TST-041).
- Consumer-driven contracts may be used; they must not require anything the published description does not allow, and the description wins (TST-042).
- An event producer should test each event against the published schema of its type (API-102, API-103) (TST-043).
- A spec may ship a conformance suite; it must use only public interfaces and must not require a language, framework or runner (TST-044).
- A replacement component must pass the same suite; a replacement business rule must pass that rule's scenarios except those it changes, and must list them with new scenarios (TST-045).
- A suite release must name the spec version it tests, with the same major and minor numbers; each test must cite its requirement IDs (TST-046).
- A suite result must not be presented as a certification, approval or endorsement by FPSOT; a vendor may state that a product passes a given suite release, with the date and full results (TST-047).
- A suite should write machine-readable results, per requirement ID: passed, failed or not applicable (TST-048).

## Test data

- Tests, fixtures, examples, demonstrations and test environments must use synthetic data only; never production personal information, not even an extract, copy, masked or de-identified version (TST-050).
- Synthetic data should be generated from the data models; a generator must take a fixed seed (TST-051).
- A test environment that needs production volume must reach it with generated data, and must not load production data (TST-052).
- Where reserved values exist, test data must use them: NANP line numbers 555-0100 to 555-0199, such as `+14185550123`; RFC 2606 domains such as `example.org` (TST-053).
- Test data must not take a value from a real record, and must not use the name of a known person; a postal address should pair a made-up street with a real municipality; a fixture should state that its data is synthetic (TST-054).
- Each suite that handles text must include English and French data, and names that test LOC-050 and LOC-051: French accents, both apostrophes, one-part names, letters beyond Western European languages (TST-055).
- Text values must keep their exact characters and be compared exactly; a test must not strip accents or change case (TST-056).

## Continuous integration and other checks

- Each level that runs in CI must be a required check (VCS-109); unit, integration and contract tests and the Gherkin check must run on every pull request; functional tests should; end-to-end tests may run on a schedule but must pass before each release (TST-060).
- A failing test must block the merge; it must not be turned off, skipped or deleted to pass a check, except under TST-062; a removal must be visible with its reason (TST-061).
- CI must not rerun a failed test on its own to turn it into a pass; a flaky test must be quarantined with a mark, out of the required check (TST-062).
- Each quarantined test must have an issue with a deadline, which should be within 30 days; by then it must be fixed or deleted with a reason; it should still run outside the required check (TST-063).
- CI should report coverage on each pull request; coverage must not be the only merge gate; a coverage drop may fail a check (TST-064).
- Functional tests must be able to run from outside against a built artifact, such as a native binary or a container image; the released artifact must pass them (TST-065).
- Accessibility tests must follow ACC-040 to ACC-047; performance tests must take their targets from the product's requirements; security tests belong to the future security spec (TST-066).
