# Arquitetura inicial

```text
Usuário
  |
  v
Tela Streamlit (src/app.py)
  |
  v
Funções de métricas (src/evaluation.py)
  |
  +--> CSV/SQLite (etapa futura)
  |
  +--> Modelos locais via Ollama (etapa futura)
  |
  v
Tabelas e gráficos
```

A primeira versão usa dados fictícios para testar a interface e as métricas. Antes de usar resultados reais, o grupo deve integrar os modelos, registrar as versões utilizadas e guardar os dados brutos dos experimentos.
