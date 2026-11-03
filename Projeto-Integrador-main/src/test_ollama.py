
import time
import ollama

modelos = [
    "qwen2.5:3b",
    "llama3.2:3b",
    "gemma3:4b"
]

pergunta = "Explique inteligência artificial em poucas palavras."

for modelo in modelos:
    print("\n" + "=" * 50)
    print(f"MODELO: {modelo}")
    print("=" * 50)

    inicio = time.perf_counter()

    try:
        resposta = ollama.chat(
            model=modelo,
            messages=[
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        fim = time.perf_counter()
        tempo = fim - inicio

        print("RESPOSTA:")
        print(resposta["message"]["content"])
        print(f"\nTempo de resposta: {tempo:.2f} segundos")

    except Exception as erro:
        print(f"Erro ao executar {modelo}: {erro}")
