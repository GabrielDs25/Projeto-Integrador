"""Integração com modelos locais disponibilizados pelo Ollama."""

import os
from time import perf_counter

import ollama


def create_client() -> ollama.Client:
    """Cria um cliente Ollama usando OLLAMA_HOST quando configurado."""
    return ollama.Client(host=os.getenv("OLLAMA_HOST"))


def list_models(client: ollama.Client) -> list[str]:
    """Lista os nomes dos modelos instalados no servidor Ollama."""
    response = client.list()
    return sorted(model.model for model in response.models)


def generate_answer(
    client: ollama.Client, model: str, prompt: str
) -> tuple[str, float]:
    """Gera uma resposta e retorna o texto e o tempo medido em segundos."""
    started_at = perf_counter()
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    elapsed_seconds = perf_counter() - started_at
    return response.message.content, elapsed_seconds
