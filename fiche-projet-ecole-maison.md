# Fiche projet : L'école à la maison

*État au 1er octobre 2026, version 3.2.9.*
*À tenir à jour après chaque version.*

## 1. Le projet

C'est une appli web de révisions scolaires, de la grande section au CM2. Elle est utilisée par plusieurs familles.

- L'appli ne contient aucune donnée propre à une famille : chaque famille crée ses propres enfants au premier lancement.
- Elle doit convenir aussi bien à des enfants qui ne savent pas encore lire (GS, CP) qu'à des élèves de CM2.

Toutes les explications et tous les textes de l'appli sont en français.

### Confidentialité du dépôt

- Le dépôt GitHub est public. Il ne doit contenir **aucune information personnelle** : prénoms des enfants qui utilisent l'appli, résultats scolaires, adresses mail, clés familiales ou codes d'appairage.
- Les prénoms utilisés dans les exercices et les exemples sont fictifs et variés.

## 2. Architecture technique

### L'appli

- L'appli tient dans **un seul fichier `index.html`**, d'environ 4 000 lignes. Elle est écrite en JavaScript classique, sans framework, et tout le code tient dans une seule fonction englobante.
- Elle est hébergée sur **GitHub Pages**, en **PWA** :
  - `manifest.webmanifest` ;
  - `sw.js`, un service worker qui fonctionne en réseau d'abord. Il ne met en cache que la page de l'appli elle-même ;
  - les icônes.
- Les **données** sont rangées dans le stockage local du navigateur, sous la clé `ecole-maison-v1`. Elles fonctionnent hors ligne.
- Chaque version a deux numéros, à faire évoluer ensemble :
  - `APP_VERSION`, dans `index.html`, affiché en bas de l'écran des profils et des réglages de la famille ;
  - `VERSION`, dans `sw.js`.

### La synchronisation (facultative)

- Le serveur est un **Google Apps Script**, `serveur-synchro-Code.gs`. Il est déployé en application Web : « Exécuter en tant que : Moi », « Accès : Tout le monde ».
- Les données de chaque famille sont stockées dans un fichier JSON du Drive. Le nom du fichier est une empreinte SHA-256 de la clé familiale.
- La **fusion** utilise le même code dans l'appli et dans le serveur :
  - Les séances sont fusionnées par identifiant (`chemin|date`).
  - Les suppressions laissent une trace : `supprimes` pour les séances, `profilsSupprimes` pour les enfants.
  - Pour les réglages, la modification la plus récente l'emporte, grâce à des dates de modification (`maj`) comparées à un « état de référence » enregistré en local.
  - La mission du jour et le total des missions sont recalculés à partir des séances.
- `FUS_VERSION` vaut actuellement **3**. Il faut l'augmenter et **redéployer le serveur** dès qu'une nouvelle liste de séances apparaît, ou que la logique de fusion change.
- Le **code d'appairage** commence par `EM1.`. Il contient l'adresse et la clé familiale. Il ne doit jamais être partagé hors de la famille.
- **Piège déjà rencontré** : la fusion ne recopie pas les objets vides. `completer()` doit donc recréer toutes les sous-structures (par exemple `maternelle.vus` et `nivExo`) au démarrage et après chaque synchronisation.

### La version de test

- Elle est générée à partir de `index.html` :
  - les clés de stockage sont distinctes (`ecole-maison-TEST-…`) ;
  - un bandeau orange s'affiche en haut ;
  - il n'y a pas de service worker.
- Le bouton « Outils » propose :
  - de créer 4 enfants d'exemple (GS, CP, CE2, CM1), avec le code parents 0000 ;
  - de remettre les démos à zéro ;
  - de tout effacer.

## 3. Profils et accès

- Au premier lancement, un écran de bienvenue permet de créer les enfants : prénom, classe de la GS au CM2, et animal. On choisit ensuite le code parents. Le même écran permet de rejoindre une famille existante avec un code d'appairage.
- **Le code parents** comporte 4 chiffres et n'est pas stocké en clair. Après 3 erreurs, il faut attendre 30 secondes. En cas d'oubli, on le récupère grâce à l'adresse mail enregistrée.
- **Le code enfant** est facultatif. Il est stocké en clair et visible dans le suivi des parents.
- **Il n'y a qu'une seule entrée côté parents** : le bouton « Suivi des parents », sur l'écran des profils. On y trouve :
  - la vue d'ensemble des enfants ;
  - « Ajouter un enfant » ;
  - « ⚙️ Réglages de la famille » : adresse mail, synchronisation, sauvegarde complète en JSON, code parents ;
  - sur chaque fiche enfant :
    - « Modifier » : prénom, classe, animal, suppression ;
    - « Suivi détaillé » ;
    - « Réglages » : bilan mail, CSV, gestion des séances avec poubelle, mission, seuils, niveaux, effacement d'historique, suppression du profil.
- **Les avatars** :
  - ce sont des emojis, sauf trois dessins SVG maison : 🦛 l'hippopotame lavande avec ses dents, 🐘 l'éléphant gris, et 🪿 l'oie blanche à l'écharpe rouge ;
  - l'enfant choisit son animal dans une grille de 17 animaux.

## 4. Modules et activités disponibles selon la classe

| Classe | Modules |
|---|---|
| GS | Maternelle, Anglais |
| CP | Maternelle, Lecture flash, Anglais |
| CE1 à CM2 | Tables, Arbre à calculs, Fractions, Lecture à voix haute, Lecture flash, Anglais |

### Les modules pour les enfants qui lisent

- **Tables** : barème selon la vitesse ; une table ratée revient en entier en fin de série ; suivi des calculs « fragiles ».
- **Arbre à calculs** : 8 niveaux, qui s'adaptent tout seuls. Il sert de **récompense de la mission du jour**. Il diagnostique les erreurs : retenue oubliée, résultats de branches collés, etc.
- **Fractions** : 4 niveaux. Les pièges proposés : inverse, complément, colorié comparé au blanc, parts inégales.
- **Lecture à voix haute** :
  - **chronométrée** : mots correctement lus par minute (MCLM), objectif personnel, avis de l'adulte sur la fluidité ;
  - **guidée** : le texte s'éclaire au bon rythme, avec une vitesse ajustée selon l'avis de l'adulte ;
  - option « groupes de sens » ;
  - 10 textes plus 6 énigmes mathématiques.
- **Lecture flash** : 5 niveaux ; le temps d'affichage s'adapte.
- **Anglais** :
  - 5 niveaux, avec un **mode non-lecteur pour la GS et le CP** : consignes dites en français, démo animée, deuxième essai, séries de 6, niveau maximum 2 ;
  - un imagier par thèmes illustrés ;
  - la famille dessinée en pied.

### Le module Maternelle

- **Trois portes**, chacune ouvrant une page de jeux. **Chaque jeu a son propre niveau** (de 1 à 4) et ses séances comptent **6 questions du même jeu**.
  - 🍬 **Les nombres** : chiffre et bonbons, j'écoute et je trouve, les formes (avec des pièges couleur et forme dès le niveau 3, et des formes tournées au niveau 4), grand ou petit, combien de bonbons, le bocal, où y en a-t-il le plus, les suites de couleurs, remplir la boîte, du plus petit au plus grand.
  - 👂 **Les sons** : tambour des syllabes, lettres, mon prénom (« Cherche le prénom Paul » au niveau 3 et plus), rimes, premier son.
  - 🦁 **Les mots** : trouve l'image, où est le chat, les couleurs, l'intrus (la catégorie n'est plus nommée à partir du niveau 3), les devinettes.
- **Démo animée** avec la main 👆 : elle se lance toute seule aux niveaux 1 et 2 du jeu. Ensuite, le bouton 👀 permet de la revoir.
- Un jeu se **débloque** quand un jeu de la même porte atteint le niveau requis.
- **Le niveau d'un jeu** :
  - il monte après 4 réussites d'affilée ;
  - il descend après 2 échecs d'affilée, ou après une série terminée avec 2 étoiles ou moins.
- Chaque question laisse un deuxième essai. Après deux erreurs, la main montre la bonne réponse.
- Une même question ne revient pas deux fois dans une série.

### La mission du jour

- Elle est configurable par enfant. Par défaut, elle comprend tables, fractions, lecture et lecture flash, chacune avec un seuil de réussite.
- Une étape ne compte qu'avec une séance terminée et réussie.
- Pour les tables, il faut au moins 5 calculs des tables de 2 à 9.
- Pour la lecture chronométrée, il faut au moins 85 % de la moyenne des 5 dernières lectures.
- La mission n'est active que si le module Arbre est disponible pour la classe de l'enfant.

## 5. Conventions à respecter

- **Pas de `confirm()` ni d'`alert()`** : ces fenêtres sont bloquées dans certains lecteurs. Les actions importantes se confirment en **deux touches** avec `confirmer()`.
- **La voix française** :
  - `parlerFr(texte, id, texteAffiché)` ;
  - les mots isolés sont dits dans des énoncés séparés (`q.parts`, `parlerSuite`) ;
  - le dictionnaire `ORAL_FR` corrige les mots mal prononcés (bus → « busse ») ;
  - les noms de lettres sont dits avec des homophones (`LETTRE_NOM` : M = « aime », N = « haine »…) ;
  - jamais de « -t-il » à l'oral ;
  - une phrase n'en coupe jamais une autre, sauf sur une action de l'enfant.
- **Les enfants qui ne lisent pas (GS, CP)** : tout est dit à voix haute, sans aucun bouton à lire.
- **Les changements de niveau** sont fêtés avec des confettis (`feteNiveau()`), sauf si l'appareil est réglé pour réduire les animations.
- **Les formulations sont neutres** : par exemple « Nouveau niveau atteint », jamais « Tu es montée ».
- **On ne casse jamais les données existantes** :
  - toute nouvelle structure passe par `completer()` ou `missionDe()` ;
  - les anciennes données doivent toujours rester lisibles.
- **Avant de livrer** :
  - tester dans un vrai navigateur (Playwright, avec une voix simulée) ;
  - livrer la version de test en même temps que la mise à jour ;
  - repérer les nouveautés dans `APP_VERSION` et `sw.js`.

## 6. Procédure de déploiement

1. **Seulement si `FUS_VERSION` a changé**, mettre à jour le serveur Google :
   - coller le nouveau code ;
   - Déployer, puis Gérer les déploiements, crayon, **Nouvelle version**. L'adresse `/exec` ne change pas ;
   - prévenir les familles qui ont leur propre serveur, pour qu'elles fassent de même.
2. Mettre à jour `index.html` et `sw.js` sur GitHub.
3. Sur chaque appareil, fermer puis rouvrir l'appli, et vérifier le numéro de version. Sur ordinateur, faire Ctrl + F5.

## 7. Prochaines étapes

**Le module « Français »**, du CE1 au CM2, à faire dans cet ordre :

1. sujet et verbe ;
2. conjugaison (présent, futur, imparfait, passé composé) ;
3. accords ;
4. nature des mots ;
5. homophones (a/à, et/est, son/sont, on/ont, ces/ses) ;
6. dictée de mots.

Chaque thème sera un jeu à part, avec son niveau, sa démo et son suivi, et pourra entrer dans la mission du jour.

**À faire aussi :**

- recueillir les retours des familles sur le module Maternelle ;
- éventuellement, dessiner en portrait le dauphin, la tortue et le hibou.

**À garder en tête si l'appli est un jour diffusée largement :**

- intégrer la police d'écriture (aujourd'hui chargée depuis Google Fonts) ;
- ajouter une page confidentialité et mentions légales ;
- chaque famille utilise son propre serveur Google ;
- l'usage en classe serait un cadre à étudier à part.
