# language: en
# SPDX-License-Identifier: Community-Spec-1.0
# A broken fixture: an examples row has fewer cells than its header.
# expect: inconsistent cell count
Feature: Broken fixture for the Gherkin check

  Scenario Outline: A row with a missing cell
    Given a person who writes their name as "<full name>"
    Then the full name of the person is "<full name>"

    Examples:
      | full name | language |
      | Zoë Ní Bhriain |
