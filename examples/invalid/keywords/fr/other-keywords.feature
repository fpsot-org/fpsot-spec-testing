# language: fr
# SPDX-License-Identifier: Community-Spec-1.0
# Une fixture brisée : « Soit », « Lorsque » et « Donc » viennent du dialecte français de Gherkin, mais TST-031 ne les permet pas.
# expect: other-keywords.feature:10: step keyword 'Soit'
# expect: other-keywords.feature:11: step keyword 'Lorsque'
# expect: other-keywords.feature:12: step keyword 'Donc'
Fonctionnalité: Fixture brisée pour la vérification Gherkin

  Scénario: Des mots clés hors du tableau
    Soit une personne dont le nom s’écrit "Tanvir"
    Lorsque l’organisme public inscrit la personne
    Donc le nom complet de la personne est "Tanvir"
