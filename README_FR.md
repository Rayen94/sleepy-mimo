# Sleepy Mimo — ton équipe YouTube automatique

Chaque nuit, ce système produit **1 vidéo longue (≈1 h, Full HD) + 3 Shorts** pour ta chaîne, les contrôle,
puis les envoie sur YouTube **en privé**. Le matin, tu les regardes et tu les passes en public (5 minutes).
Il tourne gratuitement dans le cloud sur GitHub Actions, même quand ton ordinateur est éteint.

## Ce que font les vidéos (version 5) — la série « Sleepy Mimo »
- **Une vraie série** : chaque vidéo longue est un épisode numéroté (Saison 1 : 12 épisodes écrits, diffusés dans l'ordre),
  avec le générique « Sleepy Mimo – Episode N » et une fin « See you in the next episode! ».
- **8 personnages** : Mimo, Luna la chouette, Pip le lapin, Twinkle l'étoile, Wooly l'agneau, Mia le chaton, Dot le caneton, Finn le renard.
- **Voix naturelles** (moteur Kokoro, gratuit) : chaque personnage a sa voix. Mimo chante les comptines avec cette voix.
- **Vrais instruments** (banque FluidR3 + FluidSynth) : boîte à musique, piano, harpe, cordes, basse, flûte, petites percussions.
- **Shorts = la suite de l'épisode** : l'histoire du jour découpée en Part 1, 2, 3, en vertical, avec « To be continued... »
  et « Watch the full episode! ».
- Le modèle de voix (≈120 Mo) est téléchargé automatiquement par GitHub la première fois, puis gardé en mémoire.

## Ce que font les vidéos (version 4)
- **Une histoire chaque jour** (en anglais) : Mimo et ses amis (Luna la chouette, Pip le lapin, Twinkle l'étoile,
  Wooly l'agneau) parlent avec leurs propres voix, dans des décors colorés. L'histoire mène à une comptine.
- **Comptines chantées** par la voix de Mimo, avec les **paroles en karaoké** à l'écran et une **scène dédiée** par comptine.
- **Intro « Sleepy Mimo »** au début de chaque vidéo longue. Image **Full HD, 30 images par seconde**.

## Ce que font les vidéos (version 2)
- **Vidéo longue d'1 h en 1080p** : Mimo passe par plusieurs décors (un toutes les 15 min) avec de doux fondus,
  et l'instrument change avec le décor.
- **Animation vivante** : Mimo respire, ses « Zzz » s'envolent, la lune brille, les nuages dérivent,
  des étoiles filantes passent, la caméra bouge doucement.
- **Musique plus riche** : mélodie + accords + basse douce + contre-mélodie en arpège, jeu « humain »,
  et sons d'ambiance selon le décor (bruit blanc doux, vagues, pluie, vent, nuit).
- **Shorts accrocheurs** : zoom d'ouverture, grosse phrase d'accroche qui apparaît dès la 1re seconde,
  légende, puis « More lullabies with Mimo » à la fin.

## L'équipe (12 agents)

| # | Agent | Ce qu'il fait | Fichier |
|---|-------|---------------|---------|
| 1 | Directeur général | Lit tes consignes, orchestre la journée, décide qui travaille et dans quel ordre | `main.py` + `consignes.yml` |
| 2 | Stratège contenu | Choisit les décors, morceaux et instruments, sans répéter les jours précédents | `agents/strategiste.py` |
| 3 | Compositeur | Compose des berceuses originales et arrange des comptines du domaine public | `agents/compositeur.py` |
| 4 | Illustrateur | Dessine Mimo et 6 décors animés (lune, nuages, océan, neige, lucioles, pluie) | `agents/illustrateur.py` |
| 5 | Monteur | Assemble animation + musique en vidéo HD (longue en 16:9, Shorts en 9:16) | `agents/monteur.py` |
| 6 | Rédacteur SEO | Titres, descriptions avec chapitres, tags — en anglais | `agents/redacteur.py` |
| 7 | Miniaturiste | Une miniature différente pour chaque vidéo longue | `agents/miniaturiste.py` |
| 8 | Contrôleur qualité | Vérifie durée, volume, saturation, format | `agents/controleur_qualite.py` |
| 9 | Gardien des règles | Bloque tout ce qui peut mettre la chaîne en danger (titres répétés, marques de tiers, promesses trompeuses, manque de variété) | `agents/gardien_regles.py` |
| 10 | Publieur | Envoie les vidéos en privé, réglées « conçues pour les enfants » | `agents/publieur.py` |
| 11 | Archiviste | Mémoire de la chaîne : tout ce qui a déjà été publié | `agents/archiviste.py` + `history.json` |
| 12 | Analyste | Abonnés, vues, statut des dernières vidéos, dans le rapport quotidien | `agents/analyste.py` |

Le rapport du jour (en français) est dans le dossier `reports/` et en résumé dans l'onglet **Actions**.

---

## Installation (une seule fois, environ 30 minutes)

### Étape 1 — Mettre le projet sur GitHub
1. Crée un compte sur **github.com**.
2. Clique sur **New repository** → nom : `sleepy-mimo` → coche **Private** → **Create repository**.
3. Clique sur **uploading an existing file**, glisse **tout le contenu** du dossier dézippé
   (y compris le dossier `.github`) → **Commit changes**.
   Astuce : si le dossier `.github` n'apparaît pas (il est caché), crée le fichier à la main :
   **Add file → Create new file**, nom `.github/workflows/production-quotidienne.yml`, et colle son contenu.

### Étape 2 — Ouvrir l'accès à YouTube (Google Cloud)
1. Va sur **console.cloud.google.com**, connecté avec le compte Google **de ta chaîne**.
2. Crée un projet : `sleepy-mimo`.
3. Menu **API et services → Bibliothèque** → cherche **YouTube Data API v3** → **Activer**.
4. **API et services → Écran de consentement OAuth** : type **Externe**, nom de l'appli `Sleepy Mimo`,
   ton e-mail. Ajoute ton adresse dans **Utilisateurs test**.
5. Toujours sur l'écran de consentement : clique **Publier l'application** (passer en « En production »).
   Important : sinon l'accès expire au bout de 7 jours. Google affichera un avertissement « appli non validée » :
   c'est normal pour une appli personnelle, clique sur « Paramètres avancés → Continuer ».
6. **API et services → Identifiants → Créer des identifiants → ID client OAuth** :
   type **Application Web**, URI de redirection autorisé :
   `https://developers.google.com/oauthplayground`
   Note le **Client ID** et le **Client secret**.

### Étape 3 — Obtenir la clé permanente (refresh token)
1. Va sur **developers.google.com/oauthplayground**.
2. Clique sur l'engrenage ⚙️ en haut à droite → coche **Use your own OAuth credentials** → colle Client ID et Client secret.
3. À gauche, dans le champ de saisie, colle :
   `https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly`
   → **Authorize APIs** → connecte-toi avec le compte de la chaîne → autorise.
4. Clique **Exchange authorization code for tokens** → copie le **Refresh token**.

### Étape 4 — Donner les clés à GitHub
Dans ton dépôt : **Settings → Secrets and variables → Actions → New repository secret**, crée :
- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`


### Étape 5 — Premier test
Onglet **Actions** → **Sleepy Mimo - production quotidienne** → **Run workflow**.
Compte 20 à 40 minutes. À la fin, les vidéos sont dans YouTube Studio en **Privé**,
et téléchargeables dans **Artifacts** en bas de la page de l'exécution.

Ensuite, le système tourne tout seul chaque nuit.

---

## Donner tes ordres à l'équipe : le panneau de commande
Ouvre le fichier **`consignes.yml`** dans ton dépôt GitHub → icône crayon ✏️ → modifie → **Commit changes**.
Tout est expliqué en français dans le fichier. Tu peux par exemple :
- mettre l'équipe en **pause** ;
- changer la **durée** de la vidéo longue ou des Shorts, et le **nombre de Shorts** ;
- **imposer un décor** (lune, nuages, océan, neige, lucioles, pluie) ou en interdire ;
- choisir les **instruments** et les **comptines** autorisés ;
- écrire **tes propres phrases** pour les Shorts ;
- ajouter des **tags** ;
- couper l'envoi sur YouTube (vidéos seulement téléchargeables).

Tes consignes sont appliquées dès la production suivante. Pour les voir tout de suite : **Actions → Run workflow**.
Si une consigne est mal écrite, l'équipe ne plante pas : elle garde la valeur par défaut et te le signale dans le rapport.

## Ta routine quotidienne (5 minutes)
1. Ouvre **YouTube Studio → Contenu**.
2. Regarde les 4 nouvelles vidéos privées. Supprime celles qui ne te plaisent pas.
3. Passe les autres en **Public**, ou programme-les (par exemple Shorts à 8h, 13h, 18h et vidéo longue à 19h).

## À savoir
- **Pourquoi en privé ?** YouTube bloque en privé les vidéos envoyées par une appli non auditée.
  Ce n'est pas un contournement : c'est simplement toi qui publies. C'est aussi ce qui protège ta monétisation.
- **Quota YouTube** : 10 000 unités/jour gratuites, un envoi en coûte environ 1 600 → 4 vidéos par jour passent.
- **Coût** : 0 €. Un dépôt privé GitHub a 2 000 minutes gratuites par mois ; une journée en utilise environ 20 à 40.
  Si tu dépasses, réduis `LONG_MINUTES` ou rends le dépôt public (minutes illimitées).
- **Miniatures** : YouTube n'accepte les miniatures personnalisées que si ton numéro de téléphone est vérifié sur la chaîne.
- **Musique** : uniquement des compositions générées par le système et des mélodies traditionnelles du domaine public,
  arrangées à neuf. Aucun enregistrement d'une autre chaîne n'est utilisé.
- **Police** : Fredoka (licence SIL Open Font License, libre d'utilisation).
