"""Funções pequenas para calcular métricas da avaliação."""


def accuracy_rate(results: list[dict]) -> float:
    """Retorna a proporção de respostas aprovadas, entre 0 e 1.

    Cada item deve conter a chave booleana 'correct'.
    Uma lista vazia retorna 0 para evitar divisão por zero.
    """
    if not results:
        return 0.0

    approved = sum(1 for item in results if item.get("correct") is True)
    return approved / len(results)


def average_response_time(results: list[dict]) -> float:
    """Calcula o tempo médio em segundos usando a chave 'seconds'."""
    if not results:
        return 0.0

    times = [float(item["seconds"]) for item in results]
    return sum(times) / len(times)
