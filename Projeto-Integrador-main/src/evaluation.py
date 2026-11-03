
"""Funções para calcular métricas da avaliação dos modelos de IA."""


def accuracy_rate(results: list[dict]) -> float:
    """Retorna a proporção de respostas aprovadas, entre 0 e 1."""
    if not results:
        return 0.0

    approved = sum(
        1 for item in results
        if item.get("correct") is True
    )
    return approved / len(results)


def average_response_time(results: list[dict]) -> float:
    """Calcula o tempo médio de resposta em segundos."""
    if not results:
        return 0.0

    times = [float(item["seconds"]) for item in results]
    return sum(times) / len(times)


def approved_count(results: list[dict]) -> int:
    """Conta quantas respostas foram aprovadas."""
    return sum(
        1 for item in results
        if item.get("correct") is True
    )


def rejected_count(results: list[dict]) -> int:
    """Conta quantas respostas não foram aprovadas."""
    return sum(
        1 for item in results
        if item.get("correct") is False
    )


def total_count(results: list[dict]) -> int:
    """Retorna a quantidade de avaliações realizadas."""
    return len(results)
