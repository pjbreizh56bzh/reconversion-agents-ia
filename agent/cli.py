"""Command-line interface for the automation agent.

Usage examples:
    python -m agent.cli scrape https://example.com -o page.json
    python -m agent.cli batch-scrape urls.txt -o pages.json
    python -m agent.cli analyze data.csv -o report.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from agent.analyzer import AnalyzerError, analyze_file
from agent.scraper import ScraperError, fetch_many, fetch_page


@click.group()
def cli() -> None:
    """Agent d'automatisation : scraping web et analyse de données."""


@cli.command()
@click.argument("url")
@click.option("-o", "--output", type=click.Path(), help="Fichier de sortie JSON (sinon stdout).")
def scrape(url: str, output: str | None) -> None:
    """Récupère une page web et affiche titre, méta-description, liens et texte."""
    try:
        page = fetch_page(url)
    except ScraperError as exc:
        click.echo(f"Erreur : {exc}", err=True)
        sys.exit(1)

    payload = json.dumps(page.to_dict(), ensure_ascii=False, indent=2)
    if output:
        Path(output).write_text(payload, encoding="utf-8")
        click.echo(f"Résultat écrit dans {output}")
    else:
        click.echo(payload)


@cli.command("batch-scrape")
@click.argument("urls_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), required=True, help="Fichier de sortie JSON.")
def batch_scrape(urls_file: str, output: str) -> None:
    """Récupère une liste d'URLs (une par ligne) et écrit les résultats en JSON."""
    urls = [line.strip() for line in Path(urls_file).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not urls:
        click.echo("Aucune URL trouvée dans le fichier.", err=True)
        sys.exit(1)

    results = fetch_many(urls)
    Path(output).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for r in results if "error" not in r)
    click.echo(f"{ok}/{len(urls)} pages récupérées avec succès. Résultat écrit dans {output}")


@cli.command()
@click.argument("data_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Fichier de sortie Markdown (sinon stdout).")
@click.option("--title", default="Rapport d'analyse", help="Titre du rapport.")
def analyze(data_file: str, output: str | None, title: str) -> None:
    """Analyse un fichier CSV ou JSON et génère un rapport Markdown."""
    try:
        report = analyze_file(data_file, title=title)
    except AnalyzerError as exc:
        click.echo(f"Erreur : {exc}", err=True)
        sys.exit(1)

    if output:
        Path(output).write_text(report, encoding="utf-8")
        click.echo(f"Rapport écrit dans {output}")
    else:
        click.echo(report)


if __name__ == "__main__":
    cli()
