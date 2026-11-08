# language: en
# SPDX-License-Identifier: Community-Spec-1.0
# Example feature of the FPSOT testing specification (TST-030 to TST-035).
# It describes rules of the FPSOT data models specification. All data is synthetic (TST-050 to TST-056).
@party
Feature: Record a person as a party
  A public body records each person it deals with as a party, under DMO-040.
  Only the full name of a person is required, under DMO-032.

  Rule: The full name is the only required part of a person name

    @party-person-001
    Scenario: A person with one name only
      Given a person who writes their name as "Tanvir"
      When the public body records the person
      Then the record is a party of type "person"
      And the full name of the person is "Tanvir"
      And the name of the person has no given names and no family name

    @party-person-002
    Scenario Outline: A name keeps its accents and signs
      Given a person who writes their name as "<full name>"
      When the public body records the person
      Then the full name of the person is "<full name>"

      Examples:
        | full name               |
        | Marie-Ève Lévesque-Côté |
        | François L'Écuyer       |
        | Benoît D’Amours         |
        | Zoë Ní Bhriain          |
        | Đặng Thị Ngọc Ánh       |

  Rule: Contact data keeps the form of the Party model

    @party-contact-001
    Scenario: An email address keeps the case of its local part
      Given a person named "Marie-Ève Lévesque-Côté"
      When the public body records the email address "Marie-Eve.Levesque@example.org" for the person
      Then the email address of the person is exchanged as "Marie-Eve.Levesque@example.org"

    @party-contact-002
    Scenario: A telephone extension stays apart from the number
      Given a person named "Marie-Ève Lévesque-Côté"
      When the public body records the telephone number "+14185550123" with the extension "204" for the person
      Then the telephone number of the person is exchanged as "+14185550123"
      And the extension of the number is exchanged as "204"
