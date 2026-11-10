import ollama
import time
import json

def query_model(model: str, prompt: str) -> dict:
    """Chama o Ollama, retorna resposta e tempo gasto."""
    start = time.time()
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2},
        )
        return {
            "model": model,
            "response": response.message.content,
            "seconds": round(time.time() - start, 2),
            "success": True,
        }
    except Exception as e:
        return {
            "model": model, "response": "", 
            "seconds": round(time.time() - start, 2), 
            "success": False, "error": str(e),
        }

def judge_with_llm(judge_model: str, question: str, reference: str, answer: str) -> dict:
    """Usa um LLM como juiz, retornando se a resposta está correta."""
    judge_prompt = f"""Você é um avaliador rigoroso. Compare a resposta do modelo com a resposta de referência.
Pergunta: {question}
Resposta de referência: {reference}
Resposta do modelo: {answer}
A resposta do modelo está correta? Responda APENAS com um JSON válido:
{{"correct": true ou false, "reason": "uma frase curta"}}
"""
    try:
        response = ollama.chat(
            model=judge_model,
            messages=[{"role": "user", "content": judge_prompt}],
            options={"temperature": 0.0},
        )
        text = response.message.content.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(text[start:end])
            return {"correct": bool(data.get("correct", False)), "reason": data.get("reason", "")}
        return {"correct": False, "reason": "Falha ao formatar JSON"}
    except Exception as e:
        return {"correct": False, "reason": f"Erro: {e}"}
