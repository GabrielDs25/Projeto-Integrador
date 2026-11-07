"""Funções para métricas e avaliação automática de respostas."""

import re
from typing import Any


def _normalize_text(value: Any) -> str:
    """Converte o texto para minúsculas e remove pontuação extras."""
    if value is None:
        return ""
    text = str(value).lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _keywords(text: str) -> set[str]:
    """Extrai palavras relevantes, ignorando termos curtos e vazios."""
    if not text:
        return set()
    tokens = set()
    for token in _normalize_text(text).split():
        if len(token) >= 3:
            tokens.add(token)
    return tokens


def response_similarity(reference: str, answer: str) -> float:
    """Calcula similaridade por sobreposição de palavras-chave entre referência e resposta."""
    reference_keywords = _keywords(reference)
    answer_keywords = _keywords(answer)

    if not reference_keywords and not answer_keywords:
        return 1.0
    if not reference_keywords or not answer_keywords:
        return 0.0

    intersection = reference_keywords & answer_keywords
    union = reference_keywords | answer_keywords
    return len(intersection) / len(union)


def evaluate_response(
    reference: str,
    answer: str,
    criteria: str | None = None,
    *,
    minimum_score: float = 0.35,
) -> dict[str, Any]:
    """Avalia se uma resposta atende ao critério da referência.

    A lógica usa similaridade por sobreposição de palavras-chave e, quando houver
    critério textual, adiciona as ideias essenciais do critério à referência.
    """
    reference_text = _normalize_text(reference)
    answer_text = _normalize_text(answer)
    criteria_text = _normalize_text(criteria or "")

    if not reference_text and not answer_text:
        return {"correct": True, "score": 1.0, "reason": "sem conteúdo para comparar"}

    base_score = response_similarity(reference_text, answer_text)
    if criteria_text:
        base_score = max(base_score, response_similarity(reference_text + " " + criteria_text, answer_text))

    score = min(max(base_score, 0.0), 1.0)
    correct = score >= minimum_score

    return {
        "correct": correct,
        "score": round(score, 4),
        "reason": (
            "resposta com termos essenciais da referência"
            if correct
            else "resposta insuficiente para os critérios esperados"
        ),
    }


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


def average_score(results: list[dict], key: str = "score") -> float:
    """Calcula a média de uma métrica numérica presente em cada item."""
    if not results:
        return 0.0
    values = [float(item[key]) for item in results if item.get(key) is not None]
    if not values:
        return 0.0
    return sum(values) / len(values)


def concordance_rate(results: list[dict], auto_key: str = "score", human_key: str = "human_score") -> float:
    """Calcula a proporção de casos em que a nota automática e humana ficaram próximas.

    A comparação é feita usando a escala 0-1 da nota automática e a escala 0-5 da
    nota humana, normalizadas para comparação direta.
    """
    if not results:
        return 0.0

    comparable = []
    for item in results:
        auto = item.get(auto_key)
        human = item.get(human_key)
        if auto is None or human is None:
            continue
        comparable.append((float(auto), float(human)))

    if not comparable:
        return 0.0

    close_matches = 0
    for auto, human in comparable:
        auto_normalized = auto
        human_normalized = human / 5.0
        if abs(auto_normalized - human_normalized) <= 0.25:
            close_matches += 1

    return close_matches / len(comparable)
