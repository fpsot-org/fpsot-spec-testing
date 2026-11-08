# Instructions for agents

This repository holds the FPSOT testing specification: test levels, BDD with Gherkin feature files in English and French, contract tests, conformance suites, synthetic test data and the test jobs of continuous integration.

- The normative text is in `spec/en/` and `spec/fr/`. Every rule has an ID such as `TST-001`.
- Follow `skill/SKILL.md` when you write or review tests, feature files or test data in any FPSOT project. The spec text wins on any difference.
- The example feature is in `examples/features/en/` and `examples/features/fr/`. After you change it, run `examples/test-features.sh` with the parser of `examples/requirements.txt`. Change both languages in the same commit.
- Keep all test data synthetic: 555-0100 to 555-0199 telephone numbers, `example.org` addresses, no real person.
- Every page exists in English and in French, with the same file name and the same IDs.
- Terms and abbreviations come from the term base of `fpsot-spec-writing`. Add a missing term there first.
- This is a layer 1 specification. It may refer to the layer 0 specifications, to data types, vocabularies and data models, and to api-restful for contract tests. It never refers to the registry, code or capability specifications, except by topic as future work.
- Do not name a language, runner or framework in a rule. Tools such as JUnit or Cucumber-JVM may appear only as examples.
- Do not copy text from outside standards, such as the ISTQB Glossary, ISO/IEC/IEEE 29119 or the Cucumber documentation. Summarize them in your own words and cite the exact version.
- Commits follow Conventional Commits and are signed. Pull requests are squash-merged.
