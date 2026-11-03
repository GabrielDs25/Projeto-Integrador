from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parents[1] / "src" / "app.py"


def test_app_displays_cases_and_download_button():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    assert not app.exception
    assert [metric.value for metric in app.metric] == ["100", "10", "100"]
    assert len(app.get("download_button")) == 1


def test_app_search_filters_cases():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=20)

    app.text_input[0].set_value("None").run(timeout=20)

    assert not app.exception
    assert app.metric[2].value == "1"
