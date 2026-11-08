# language: fr
# SPDX-License-Identifier: Community-Spec-1.0
# Une fixture brisée : « Etant donne », sans accents, n’est pas un mot clé.
# Le parseur lit alors cette étape comme une description du scénario.
# expect: misspelled-first-step.feature:8: 'Scénario' has a description
Fonctionnalité: Fixture brisée pour la vérification Gherkin

  Scénario: Un premier mot clé mal écrit
    Etant donne une personne qui écrit son nom "Tanvir"
    Alors le nom complet de la personne est "Tanvir"
