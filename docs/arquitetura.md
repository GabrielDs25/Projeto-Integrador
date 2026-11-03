# Arquitetura da plataforma

```text
Usuario
  |
  v
Interface Streamlit (src/app.py)
  | busca, filtros, execucao e exportacao
  +--> Casos de teste (eval/casos_exemplo.csv)
  |
  +--> Cliente Ollama (src/model_runner.py)
  |     modelos locais instalados
  |
  +--> SQLite (data/evaluations.sqlite3)
  |     execucoes, respostas, tempos e falhas
  |
  +--> Comparacao de tempos medios e exportacao CSV
```

A interface consulta os 100 casos cadastrados no CSV, permite buscar perguntas,
filtrar por tema, consultar respostas de referencia e criterios de aprovacao e
baixar os casos filtrados. O usuario seleciona modelos instalados no Ollama e a
quantidade de casos por execucao. As mesmas perguntas sao enviadas a cada modelo
selecionado.

Respostas, tempos medidos e falhas sao persistidos no SQLite e podem ser
consultados e exportados em CSV. O banco fica em `data/evaluations.sqlite3`;
`EVALUATION_DB_PATH` permite configurar outro caminho. A aprovacao automatica,
as notas humanas e a analise de concordancia ainda serao implementadas. Nenhum
resultado e criado sem uma execucao real.
