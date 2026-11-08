# Terms needed

Entries to add to `termbase/terms.yaml` of `fpsot-spec-writing`, in its format.
The GDT search gave no record for behavior-driven development or for test double, and TERMIUM Plus could not be read.
Both entries take their French from the French version of the ISTQB Glossary 4.8.1, maintained by the CFTL.
That version keeps "behavior-driven development" in English, so the French full form stays in English, like the CSV and RDF entries.
For "test double", the ISTQB French term is "doublon de test"; the project lead should confirm it, since "doublure de test" is also in common use.

```yaml
  - id: bdd
    kind: abbreviation
    en: {short: "BDD", full: "behavior-driven development", definition: "A way of working in which domain experts, developers and testers agree on the expected behavior of a system through examples, which then become its tests."}
    fr: {short: "BDD", full: "behavior-driven development", definition: "Façon de travailler où les spécialistes du domaine, les équipes de développement et les équipes de test s'entendent sur le comportement attendu d'un système au moyen d'exemples, qui deviennent ensuite ses tests."}
    source: {name: "ISTQB Glossary 4.8.1, behavior-driven development, French version (no GDT record found; TERMIUM Plus could not be read)", url: "https://glossary.istqb.org/en_US/term/behavior-driven-development", checked: "2026-11-08"}
  - id: test-double
    kind: term
    en: {full: "test double", definition: "A component that stands in for a real dependency during a test, such as a component that returns fixed answers."}
    fr: {full: "doublon de test", definition: "Composant qui remplace une dépendance réelle pendant un test, par exemple un composant qui renvoie des réponses fixes."}
    source: {name: "ISTQB Glossary 4.8.1, test double, French version (no GDT record found; TERMIUM Plus could not be read)", url: "https://glossary.istqb.org/en_US/term/test-double", checked: "2026-11-08"}
```
