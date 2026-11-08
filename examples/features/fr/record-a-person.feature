# language: fr
# SPDX-License-Identifier: Community-Spec-1.0
# Exemple de fonctionnalité de la spécification FPSOT sur les tests (TST-030 à TST-035).
# Elle décrit des règles de la spécification FPSOT sur les modèles de données. Toutes les données sont synthétiques (TST-050 à TST-056).
@party
Fonctionnalité: Inscrire une personne comme partie
  Un organisme public inscrit comme partie chaque personne avec qui il traite, selon DMO-040.
  Seul le nom complet d’une personne est obligatoire, selon DMO-032.

  Règle: Le nom complet est la seule partie obligatoire d’un nom de personne

    @party-person-001
    Scénario: Une personne qui n’a qu’un seul nom
      Étant donné une personne qui écrit son nom "Tanvir"
      Quand l’organisme public inscrit la personne
      Alors l’enregistrement est une partie du type "person"
      Et le nom complet de la personne est "Tanvir"
      Et le nom de la personne n’a ni prénoms ni nom de famille

    @party-person-002
    Plan du scénario: Un nom garde ses accents et ses signes
      Étant donné une personne qui écrit son nom "<nom complet>"
      Quand l’organisme public inscrit la personne
      Alors le nom complet de la personne est "<nom complet>"

      Exemples:
        | nom complet             |
        | Marie-Ève Lévesque-Côté |
        | François L'Écuyer       |
        | Benoît D’Amours         |
        | Zoë Ní Bhriain          |
        | Đặng Thị Ngọc Ánh       |

  Règle: Les coordonnées gardent la forme du modèle Party

    @party-contact-001
    Scénario: Une adresse courriel garde la casse de sa partie locale
      Étant donné une personne nommée "Marie-Ève Lévesque-Côté"
      Quand l’organisme public inscrit l’adresse courriel "Marie-Eve.Levesque@example.org" de la personne
      Alors l’adresse courriel de la personne est échangée sous la forme "Marie-Eve.Levesque@example.org"

    @party-contact-002
    Scénario: Un numéro de poste reste séparé du numéro de téléphone
      Étant donné une personne nommée "Marie-Ève Lévesque-Côté"
      Quand l’organisme public inscrit le numéro de téléphone "+14185550123" avec le poste "204" de la personne
      Alors le numéro de téléphone de la personne est échangé sous la forme "+14185550123"
      Et le poste du numéro est échangé sous la forme "204"
