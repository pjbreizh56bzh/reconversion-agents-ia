"""Data analysis utilities: load tabular data and produce a Markdown report."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


class AnalyzerError(RuntimeError):
    """Raised when input data cannot be loaded or is empty."""


def load_dataframe(path: str | Path) -> pd.DataFrame:
    """Load a CSV or JSON file (list of records) into a DataFrame."""
    file_path = Path(path)
    if not file_path.exists():
        raise AnalyzerError(f"File not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() == ".json":
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)
    else:
        raise AnalyzerError(f"Unsupported file type: {file_path.suffix}")

    if df.empty:
        raise AnalyzerError(f"No data found in {file_path}")

    return df


def build_report(df: pd.DataFrame, title: str = "Rapport d'analyse") -> str:
    """Build a Markdown report summarizing a DataFrame: shape, dtypes, stats, missing values."""
    lines = [f"# {title}", "", f"- Lignes : {len(df)}", f"- Colonnes : {len(df.columns)}", ""]

    lines.append("## Colonnes")
    lines.append("")
    lines.append("| Colonne | Type | Valeurs manquantes |")
    lines.append("|---|---|---|")
    for col in df.columns:
        lines.append(f"| {col} | {df[col].dtype} | {df[col].isna().sum()} |")
    lines.append("")

    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        lines.append("## Statistiques (colonnes numériques)")
        lines.append("")
        desc = numeric_df.describe().round(2)
        lines.append(desc.to_markdown())
        lines.append("")

    categorical_df = df.select_dtypes(include=["object", "string"])
    if not categorical_df.empty:
        lines.append("## Valeurs les plus fréquentes (colonnes textuelles)")
        lines.append("")
        for col in categorical_df.columns:
            top = df[col].value_counts().head(5)
            if top.empty:
                continue
            lines.append(f"**{col}**")
            lines.append("")
            for value, count in top.items():
                lines.append(f"- {value}: {count}")
            lines.append("")

    return "\n".join(lines)


def analyze_file(path: str | Path, title: str = "Rapport d'analyse") -> str:
    """Load a data file and return a Markdown analysis report."""
    df = load_dataframe(path)
    return build_report(df, title=title)
