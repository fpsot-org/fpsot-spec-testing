# language: fr
# SPDX-License-Identifier: Community-Spec-1.0
# Une fixture brisée : « Then » n’est pas un mot clé du dialecte français de Gherkin.
# expect: wrong-keyword.feature: parse error \(9:5\): expected: .*got 'Then
Fonctionnalité: Fixture brisée pour la vérification Gherkin

  Scénario: Un mot clé anglais dans un fichier français
    Étant donné une personne qui écrit son nom "Tanvir"
    Then le nom complet de la personne est "Tanvir"
