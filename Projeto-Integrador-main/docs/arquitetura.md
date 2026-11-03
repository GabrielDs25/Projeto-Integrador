# Arquitetura inicial

```text
Usuário
  |
  v
Interface Streamlit (src/app.py)
  | busca, filtro, consulta e exportação
  +--> Casos de teste (eval/casos_exemplo.csv)
  |
  +--> Gráfico de quantidade de casos por tema
  |
  +--> Próxima etapa:
         Modelos locais via Ollama
         Resultados e métricas de avaliação
```

A interface atual consulta os 100 casos cadastrados no CSV. Permite buscar perguntas, filtrar por tema, consultar respostas de referência e critérios de aprovação e baixar os casos filtrados. O gráfico apresenta a distribuição dos casos, não o desempenho de modelos.

A integração com modelos ainda será feita. Antes de divulgar métricas de desempenho, o grupo deve executar os experimentos, registrar os modelos e suas versões, guardar os dados brutos e documentar falhas e limitações.
