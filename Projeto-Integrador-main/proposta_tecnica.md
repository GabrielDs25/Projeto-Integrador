# Proposta técnica — Plataforma de Avaliação de Modelos de IA

**Tema:** 3 — Plataforma de avaliação de LLMs e agentes  
**Grupo:** preencher com os quatro integrantes  
**Data:** 24/10/2026

## 1. Problema

Modelos de inteligência artificial podem produzir respostas diferentes para a mesma pergunta. Uma resposta pode ser correta, clara e rápida, enquanto outra pode conter erros ou demorar mais. Sem testes organizados, é difícil comparar modelos e descobrir quando uma mudança nas instruções piora os resultados.

## 2. Objetivo

Desenvolver uma aplicação simples que execute um conjunto de perguntas em três modelos de linguagem, registre respostas e tempos e apresente uma comparação dos resultados. A plataforma também investigará se um modelo usado como avaliador consegue atribuir notas semelhantes às avaliações humanas.

## 3. Usuários e funcionamento previsto

O usuário selecionará os modelos e iniciará uma avaliação. O sistema enviará as mesmas perguntas a cada modelo, armazenará os resultados e exibirá tabelas e gráficos. Cada caso de teste terá uma pergunta, uma resposta de referência ou critérios de correção e, quando possível, uma nota humana.

## 4. Arquitetura inicial

- **Interface:** Streamlit, para apresentar controles, tabelas e gráficos.
- **Lógica:** Python, para executar testes, calcular métricas e organizar resultados.
- **Modelos:** modelos locais compatíveis com Ollama, após teste de compatibilidade e desempenho.
- **Armazenamento:** SQLite ou arquivos CSV/JSON para guardar perguntas e resultados.
- **Qualidade:** pytest para testes automáticos e GitHub Actions para executar os testes a cada alteração.
- **Execução:** Docker/Compose será preparado e validado durante o desenvolvimento.

## 5. Plano de avaliação

O objetivo final é montar 100 casos de teste e executar os mesmos casos nos três modelos. As métricas previstas incluem:
- **Taxa de acerto:** quantidade de respostas aprovadas dividida pelo total avaliado.
- **Tempo médio de resposta:** média dos tempos medidos em segundos.
- **Concordância do avaliador:** comparação entre notas de um avaliador automático e notas humanas em pelo menos 30 casos. Será definida uma métrica adequada ao tipo de nota, como concordância percentual ou kappa ponderado para categorias ordenadas.
- **Regressão:** comparar resultados antes e depois de alterar intencionalmente um prompt, verificando se a qualidade piora.

Os critérios de correção serão definidos antes dos testes. Os resultados serão registrados em CSV/JSON, incluindo falhas e limitações. Não serão inventados resultados: as tabelas finais serão preenchidas depois da execução real dos experimentos.

## 6. Plano de trabalho

1. Criar repositório, ambiente Python, primeiro teste e CI.
2. Criar a tela inicial e um formato padronizado para os casos de teste.
3. Integrar três modelos locais e salvar respostas e tempos.
4. Completar os 100 casos e executar os experimentos.
5. Coletar avaliações humanas para pelo menos 30 casos e analisar a concordância.
6. Preparar documentação técnica, pesquisa em formato ABNT, vídeo e pasta de evidências.

## 7. Riscos e cuidados

Modelos locais podem responder lentamente ou não caber na memória disponível; por isso, serão testados modelos pequenos antes da escolha final. Respostas de IA podem parecer convincentes e ainda estar erradas, então a avaliação usará critérios explícitos e revisão humana. Serão usados dados públicos ou sintéticos, sem informações pessoais reais. O projeto será planejado para não depender de APIs ou hospedagem pagas.

## 8. Resultado esperado

Uma aplicação reproduzível que permita executar perguntas de teste, consultar resultados e comparar modelos de maneira transparente. O sucesso será medido pela execução reproduzível dos testes, pelo registro dos dados e pela análise crítica dos resultados, inclusive quando forem negativos.
