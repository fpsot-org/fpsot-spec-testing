# language: en
# SPDX-License-Identifier: Community-Spec-1.0
# A broken fixture: "Example" and "*" come from the English dialect of Gherkin, but TST-031 does not allow them.
# expect: other-keywords.feature:8: keyword 'Example'; TST-031 allows 'Scenario'
# expect: other-keywords.feature:10: step keyword '\*'
Feature: Broken fixture for the Gherkin check

  Example: Keywords outside the table
    Given a person who writes their name as "Tanvir"
    * the public body records the person
    Then the full name of the person is "Tanvir"
