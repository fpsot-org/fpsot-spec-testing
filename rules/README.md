# Rules

Machine-checkable rules for this specification.
Each rule cites the requirement ID it enforces.

The script `examples/check-features.py` checks feature files: it parses them with the official Gherkin parser (TST-034), checks the language header, the keywords of TST-031 and the parity of the English and French versions (TST-031, TST-032), and checks that each scenario has a When and a Then step and no description (TST-024, TST-036).
The `gherkin` job of the continuous integration runs its tests, `examples/test-features.sh`, on every change.
This folder has no other rules yet.
