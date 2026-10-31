Projeto Integrador

Tema 3. Plataforma de avaliação de LLMs e agentes

Curso: EAD_PROINT_100.DD-ADS-PI-10-74.2026.74

Disciplina: Projeto Integrador

Integrante 1: [Gabriel dos Santos] – RA: [2411597]

Integrante 2: [Leonardo Henrique Félix] – RA: [2410717]

Integrante 3: [Mateus Felipe Silva Pacheco] – RA: [2411247]

>>>>>>> 782461515b80a2be77eacf10b65b2820b9e860b5

# Tema 3 — Plataforma de Avaliação de Modelos de IA

Projeto acadêmico para testar e comparar respostas de modelos de inteligência artificial.

> **Estado atual:** versão inicial para o Marco 1. A tela usa dados de exemplo; ela ainda não consulta modelos reais de IA. Essa integração será feita numa próxima etapa.

## Objetivo

Enviar as mesmas perguntas a três modelos de IA, registrar suas respostas e comparar qualidade e tempo. O projeto também deverá comparar um avaliador automático com avaliações humanas.

## Como executar no computador

Recomendado: Python 3.11 ou 3.12.

1. Instale o Python e marque a opção **Add Python to PATH** durante a instalação.
2. Abra um terminal dentro desta pasta.
3. Crie um ambiente virtual:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **Linux/macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
5. Abra a tela:
   ```bash
   streamlit run src/app.py
   ```

## Como executar os testes

```bash
python -m pytest
```

## Estrutura

- `src/`: código do programa.
- `tests/`: testes automáticos.
- `eval/`: exemplos de perguntas e resultados.
- `docs/`: documentação.
- `evidencias/`: guardar capturas, logs, resultados e vídeo ao longo do projeto.
- `PROMPTS.md`: registrar o uso de ferramentas de IA.

## Próximas etapas

1. Confirmar com o professor a escolha do Tema 3. ok
2. Criar um repositório no GitHub e enviar estes arquivos. ok
3. Fazer a integração contínua (CI) executar os testes.
4. Integrar modelos reais de IA locais, por exemplo usando Ollama.
5. Preparar 100 casos de teste e avaliar pelo menos 30 casos com pessoas.
6. Comparar o avaliador automático com as avaliações humanas.
7. Registrar resultados, falhas e limitações honestamente.

## Privacidade e custo

Usar perguntas sintéticas ou conteúdo público. Não inserir senhas, chaves de API ou dados pessoais reais. O objetivo é executar o projeto sem serviços pagos; a escolha final dos modelos deve ser testada no computador do grupo.
=======

<img width="993" height="738" alt="Buscar pergunta" src="https://github.com/user-attachments/assets/5c55959c-276e-4113-a8f0-7b7caf78f85f" />
Buscar pergunta
Permite pesquisar palavras e localizar perguntas específicas dentro dos 100 casos cadastrados.

<img width="1440" height="776" alt="Filtrar por tema" src="https://github.com/user-attachments/assets/da3e0037-9f44-4672-98a7-34d054f5dbba" />
Filtrar por tema
Permite selecionar assuntos, como coleções, arquivos e testes, para visualizar somente determinadas perguntas.

<img width="1166" height="768" alt="Indicadores" src="https://github.com/user-attachments/assets/593410b0-a8f1-45d0-9573-d51189bfe14f" />
Indicadores
- 100 casos cadastrados.
- 10 temas.
- 100 casos encontrados.

<img width="1027" height="777" alt="Distribuicao de casos por tema" src="https://github.com/user-attachments/assets/7e37c501-09ee-4ad9-9e7b-81c07484e347" />
Distribuição de casos por tema
Mostra graficamente quantas perguntas existem em cada assunto.

