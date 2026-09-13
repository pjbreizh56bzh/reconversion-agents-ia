import json

import pytest

from agent.analyzer import AnalyzerError, analyze_file, build_report, load_dataframe


def test_load_dataframe_csv(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")

    df = load_dataframe(csv_path)

    assert list(df.columns) == ["name", "age"]
    assert len(df) == 2


def test_load_dataframe_json(tmp_path):
    json_path = tmp_path / "data.json"
    json_path.write_text(json.dumps([{"name": "Alice", "age": 30}]), encoding="utf-8")

    df = load_dataframe(json_path)

    assert len(df) == 1


def test_load_dataframe_missing_file(tmp_path):
    with pytest.raises(AnalyzerError):
        load_dataframe(tmp_path / "missing.csv")


def test_load_dataframe_unsupported_extension(tmp_path):
    bad_path = tmp_path / "data.txt"
    bad_path.write_text("hello", encoding="utf-8")

    with pytest.raises(AnalyzerError):
        load_dataframe(bad_path)


def test_build_report_contains_key_sections(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("name,age\nAlice,30\nBob,25\nAlice,40\n", encoding="utf-8")
    df = load_dataframe(csv_path)

    report = build_report(df, title="Mon rapport")

    assert "# Mon rapport" in report
    assert "## Colonnes" in report
    assert "## Statistiques" in report
    assert "## Valeurs les plus fréquentes" in report


def test_analyze_file_end_to_end(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("name,age\nAlice,30\n", encoding="utf-8")

    report = analyze_file(csv_path)

    assert "# Rapport d'analyse" in report
