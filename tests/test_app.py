from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parents[1] / "src" / "app.py"


def test_app_displays_cases_and_download_button(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "EVALUATION_DB_PATH", str(tmp_path / "evaluations.sqlite3")
    )
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    assert not app.exception
    assert [metric.value for metric in app.metric] == ["100", "10", "100"]
    assert [button.label for button in app.get("download_button")] == [
        "Baixar casos filtrados em CSV"
    ]


def test_app_search_filters_cases(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "EVALUATION_DB_PATH", str(tmp_path / "evaluations.sqlite3")
    )
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    app.text_input[0].set_value("None").run(timeout=20)

    assert not app.exception
    assert app.metric[2].value == "1"


def test_app_handles_unavailable_ollama(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "EVALUATION_DB_PATH", str(tmp_path / "evaluations.sqlite3")
    )
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:1")

    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    assert not app.exception
    assert any("Não foi possível acessar o Ollama" in error.value for error in app.error)
