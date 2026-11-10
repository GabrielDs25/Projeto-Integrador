import csv
import json
import sys
import os

# Adiciona a pasta src ao caminho para importar o model_client
sys.path.insert(0, os.path.join(os.path.dirname(_file_), "..", "src"))
from model_client import query_model, judge_with_llm

MODELS = ["gemma2:2b"]  # Coloque o nome dos modelos que você baixou no Ollama
JUDGE_MODEL = "gemma2:2b" 

def main():
    # Vamos ler o seu casos_exemplo.csv (que tem 3 perguntas)
    with open(os.path.join(os.path.dirname(_file_), "..", "eval", "casos_exemplo.csv"), newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))

    results = []
    for case in cases:
        q = case["pergunta"]
        ref = case["resposta_referencia"]
        
        for model in MODELS:
            print(f"Testando {model} na pergunta: {q[:30]}...")
            out = query_model(model, q)
            if not out["success"]:
                print(f"Erro: {out['error']}")
                continue
                
            # O juiz avalia a resposta
            judge = judge_with_llm(JUDGE_MODEL, q, ref, out["response"])
            
            results.append({
                "id": case["id"], "pergunta": q,
                "modelo": model, "resposta": out["response"],
                "segundos": out["seconds"],
                "juiz_correto": judge["correct"],
                "juiz_justificativa": judge["reason"],
            })

    # Salva os resultados reais!
    with open(os.path.join(os.path.dirname(_file_), "..", "eval", "resultados.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nSucesso! {len(results)} respostas salvas em eval/resultados.json")

if _name_ == "_main_":
    main()
