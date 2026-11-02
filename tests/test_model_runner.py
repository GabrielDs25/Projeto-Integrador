from unittest.mock import Mock

from src.model_runner import generate_answer, list_models


def test_list_models_returns_sorted_model_names():
    client = Mock()
    client.list.return_value.models = [
        Mock(model="zeta:latest"),
        Mock(model="alpha:latest"),
    ]

    assert list_models(client) == ["alpha:latest", "zeta:latest"]


def test_generate_answer_returns_response_and_elapsed_time(monkeypatch):
    client = Mock()
    client.chat.return_value.message.content = "Resposta real"
    timestamps = iter([10.0, 12.5])
    monkeypatch.setattr("src.model_runner.perf_counter", lambda: next(timestamps))

    answer, seconds = generate_answer(client, "modelo:latest", "Pergunta")

    assert answer == "Resposta real"
    assert seconds == 2.5
    client.chat.assert_called_once_with(
        model="modelo:latest",
        messages=[{"role": "user", "content": "Pergunta"}],
        stream=False,
    )
