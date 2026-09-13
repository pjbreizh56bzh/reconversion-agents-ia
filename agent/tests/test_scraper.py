from unittest.mock import patch

import pytest

from agent.scraper import ScraperError, fetch_many, fetch_page

SAMPLE_HTML = """
<html>
<head>
  <title>Exemple de page</title>
  <meta name="description" content="Une page de test">
</head>
<body>
  <h1>Titre principal</h1>
  <h2>Sous-titre</h2>
  <p>Un paragraphe de contenu.</p>
  <a href="/relatif">Lien relatif</a>
  <a href="https://external.test/page">Lien externe</a>
  <a href="#ancre">Ancre ignorée</a>
</body>
</html>
"""


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code


def test_fetch_page_extracts_expected_fields():
    with patch("agent.scraper.requests.get", return_value=FakeResponse(SAMPLE_HTML)):
        page = fetch_page("https://example.test/")

    assert page.status_code == 200
    assert page.title == "Exemple de page"
    assert page.meta_description == "Une page de test"
    assert page.headings == ["Titre principal", "Sous-titre"]
    assert "https://example.test/relatif" in page.links
    assert "https://external.test/page" in page.links
    assert not any(link.startswith("#") for link in page.links)
    assert page.word_count > 0


def test_fetch_page_raises_on_network_error():
    import requests

    with patch("agent.scraper.requests.get", side_effect=requests.RequestException("boom")):
        with pytest.raises(ScraperError):
            fetch_page("https://example.test/")


def test_fetch_many_collects_errors_without_raising():
    import requests

    def fake_get(url, headers=None, timeout=None):
        if "bad" in url:
            raise requests.RequestException("nope")
        return FakeResponse(SAMPLE_HTML)

    with patch("agent.scraper.requests.get", side_effect=fake_get):
        results = fetch_many(["https://good.test/", "https://bad.test/"])

    assert results[0]["title"] == "Exemple de page"
    assert "error" in results[1]
