# reconversion-agents-ia

Agent d'automatisation Python polyvalent : scraping web, analyse de données et
traitement par lots. Conçu pour être vendable en prestation freelance
(Fiverr, Upwork, Malt) dès le premier client.

## Fonctionnalités

- **Scraping** (`agent/scraper.py`) : récupère une page web et en extrait le
  titre, la méta-description, les titres (`h1`/`h2`/`h3`), les liens et le
  texte brut.
- **Traitement par lots** : scrape une liste d'URLs (un fichier texte, une
  URL par ligne) et exporte les résultats en JSON.
- **Analyse de données** (`agent/analyzer.py`) : charge un fichier CSV ou
  JSON et génère un rapport Markdown (dimensions, types de colonnes, valeurs
  manquantes, statistiques descriptives, valeurs les plus fréquentes).
- **CLI unifiée** (`agent/cli.py`) via [Click](https://click.palletsprojects.com/).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Pour lancer les tests, installer aussi les dépendances de développement :

```bash
pip install -r requirements-dev.txt
```

## Utilisation

```bash
# Scraper une page unique
python -m agent.cli scrape https://example.com -o page.json

# Scraper une liste d'URLs (fichier texte, une URL par ligne)
python -m agent.cli batch-scrape urls.txt -o pages.json

# Analyser un CSV ou JSON et générer un rapport Markdown
python -m agent.cli analyze data.csv -o rapport.md
```

## Tests

```bash
pytest agent/tests -v
```

## Déploiement avec Docker

```bash
docker build -t agent-automatisation .
docker run --rm agent-automatisation scrape https://example.com
```

## Exemple concret (à montrer sur un profil freelance)

Le dossier [`examples/`](examples/) contient une sortie réelle de l'outil,
utilisable telle quelle dans un portfolio Fiverr/Upwork/Malt :

- [`example_scrape.json`](examples/example_scrape.json) — résultat de
  `agent.cli scrape` sur une page produit de démonstration (titre,
  méta-description, titres, liens, texte).
- [`example_leads.csv`](examples/example_leads.csv) — jeu de données brut
  (catalogue produits) tel qu'on l'obtiendrait après un scraping par lots.
- [`example_report.md`](examples/example_report.md) — rapport généré par
  `agent.cli analyze` à partir de ce CSV (statistiques de prix, répartition
  par catégorie, produits les plus fréquents).

Pour régénérer ces fichiers :

```bash
python -m agent.cli scrape <url> -o examples/example_scrape.json
python -m agent.cli analyze examples/example_leads.csv -o examples/example_report.md --title "Rapport - Catalogue BoutiqueDemo"
```

## Vendre cette solution en freelance

### Positionnement

Un agent d'automatisation générique se décline en plusieurs prestations
concrètes pour de petites entreprises ou indépendants qui n'ont pas le temps
ou les compétences techniques pour :

- surveiller des sites concurrents (prix, contenus, disponibilités) ;
- constituer une base de prospects à partir de pages web publiques ;
- transformer un export CSV/JSON brut en rapport lisible pour une décision.

### Offres suggérées (Fiverr / Upwork / Malt)

| Offre | Description | Fourchette de prix |
|---|---|---|
| Scraping ponctuel | Extraction structurée d'une ou plusieurs pages, livrée en CSV/JSON | 50–150 € |
| Veille récurrente | Scraping planifié (ex. quotidien) avec alerte sur changement | 100–400 €/mois |
| Rapport d'analyse | Nettoyage + rapport Markdown/PDF à partir d'un jeu de données fourni | 80–300 € |
| Automatisation sur mesure | Adaptation du script à un besoin spécifique du client | 150–500 €/mission |

### Prérequis légaux et éthiques

- Respecter les conditions d'utilisation et le `robots.txt` des sites ciblés.
- Ne scraper que des données publiques, sans contourner d'authentification
  ni de protections anti-bot.
- Informer le client des limites (données personnelles, RGPD) avant toute
  mission impliquant des données à caractère personnel.

### Prochaine étape concrète

1. Personnaliser ce dépôt avec 2-3 exemples de sortie (page scrapée +
   rapport) pour illustrer la prestation sur le profil freelance.
2. Publier une offre ciblée (ex. "Scraping web + rapport Markdown sur mesure")
   avec un délai de livraison court (24-48h) pour convertir rapidement.
3. Ajuster le prix après les 2-3 premières missions selon le temps réel passé.
