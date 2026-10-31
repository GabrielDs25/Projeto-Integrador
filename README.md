
# Tema 3 – Plataforma de Avaliação de LLMs e Agentes

**Curso:** EAD_PROINT_100.DD-ADS-PI-10-74.2026.74

**Disciplina:** Projeto Integrador

**Integrantes:**

- **Integrante 1:** Gabriel dos Santos – RA: 2411597
- **Integrante 2:** Leonardo Henrique Félix – RA: 2410717
- **Integrante 3:** Mateus Felipe Silva Pacheco – RA: 2411247

---

## 1. Apresentação do Projeto

O projeto consiste no desenvolvimento de uma plataforma para avaliação e comparação de modelos de Inteligência Artificial (LLMs) e agentes inteligentes. A ferramenta tem como finalidade permitir a execução de testes, a análise das respostas geradas e a comparação do desempenho de diferentes modelos, considerando critérios como qualidade das respostas, precisão e tempo de execução.

**Estado atual:** O projeto encontra-se em sua versão inicial, correspondente ao Marco 1. Nesta etapa, a interface utiliza dados fictícios para demonstrar o funcionamento da plataforma. A integração com modelos reais de Inteligência Artificial será desenvolvida nas próximas etapas.

## 2. Objetivo

Desenvolver uma plataforma capaz de enviar as mesmas perguntas para três modelos diferentes de Inteligência Artificial, registrar as respostas obtidas e comparar seus resultados.

Além disso, o sistema deverá permitir a avaliação automática das respostas e a comparação desses resultados com avaliações realizadas por pessoas, possibilitando identificar diferenças de desempenho, pontos positivos e limitações de cada modelo.

## 3. Tecnologias Utilizadas

O desenvolvimento do projeto utiliza tecnologias de código aberto e ferramentas gratuitas, priorizando a execução local e evitando a dependência de serviços pagos.

As principais tecnologias previstas são:

- **Python:** linguagem principal de desenvolvimento.
- **Streamlit:** criação da interface gráfica da plataforma.
- **Ollama:** execução local de modelos de Inteligência Artificial.
- **Pytest:** execução de testes automatizados.
- **Git e GitHub:** controle de versão e colaboração entre os integrantes.

## 4. Como Executar o Projeto

**Requisitos recomendados:** Python 3.11 ou 3.12.

Primeiramente, instale o Python e marque a opção *Add Python to PATH* durante a instalação.

Em seguida, abra o terminal dentro da pasta do projeto.

### 4.1. Criar o ambiente virtual

**Windows:**

```bash
py -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

### 4.3. Iniciar a plataforma

Para abrir a interface do sistema, execute:

```bash
streamlit run src/app.py
```

Após a execução, o Streamlit disponibilizará o endereço local para acessar a plataforma pelo navegador.

## 5. Como Executar os Testes

Para verificar o funcionamento dos componentes do projeto e executar os testes automatizados, utilize o comando:

```bash
python -m pytest
```

## 6. Estrutura do Projeto

A organização dos arquivos está dividida da seguinte maneira:

- **src/:** contém o código-fonte e os principais componentes da aplicação.
- **tests/:** armazena os testes automatizados utilizados para verificar o funcionamento do sistema.
- **eval/:** contém os casos de teste, perguntas e resultados utilizados na avaliação dos modelos.
- **docs/:** reúne a documentação técnica e acadêmica do projeto.
- **evidencias/:** armazena capturas de tela, registros, resultados de avaliações e vídeos demonstrativos.
- **PROMPTS.md:** documenta as interações realizadas com ferramentas de Inteligência Artificial durante o desenvolvimento, incluindo as respostas recebidas e as decisões tomadas pela equipe.

## 7. Próximas Etapas do Desenvolvimento

Para dar continuidade ao projeto e atender aos requisitos estabelecidos na disciplina, estão previstas as seguintes atividades:

1. Confirmar a escolha do Tema 3 com o professor. **(Concluído)**
2. Criar o repositório compartilhado no GitHub e disponibilizar os arquivos do projeto. **(Concluído)**
3. Implementar a integração contínua (CI), configurando a execução automática dos testes.
4. Integrar modelos reais de Inteligência Artificial, priorizando modelos locais executados por meio do Ollama.
5. Desenvolver uma base com 100 casos de teste para avaliar os modelos.
6. Realizar avaliações humanas de pelo menos 30 casos, permitindo comparar as opiniões das pessoas com os resultados do avaliador automático.
7. Analisar e comparar os resultados obtidos, considerando a qualidade das respostas, a precisão e o tempo de execução.
8. Registrar os resultados, erros encontrados, dificuldades e limitações identificadas durante o desenvolvimento.

## 8. Funcionalidades da Plataforma

A plataforma contará com recursos para facilitar a consulta, organização e análise dos casos de teste cadastrados.

**Busca de perguntas:** permite pesquisar palavras ou termos específicos e localizar perguntas dentro da base de 100 casos cadastrados.

**Filtro por tema:** possibilita selecionar assuntos específicos para visualizar somente as perguntas relacionadas ao tema escolhido, facilitando a organização dos testes.

**Indicadores gerais:** apresenta informações quantitativas sobre a base de avaliação, incluindo:

- 100 casos de teste cadastrados.
- 10 temas diferentes.
- Total de casos encontrados conforme os filtros aplicados.

**Distribuição de casos por tema:** apresenta um gráfico que demonstra a quantidade de perguntas cadastradas em cada assunto, permitindo visualizar como os casos estão distribuídos na base de testes.

## 9. Segurança, Privacidade e Custos

Durante o desenvolvimento, serão utilizados apenas dados públicos ou sintéticos, evitando a utilização de informações pessoais reais.

Também será necessário garantir que senhas, chaves de API e outras informações confidenciais não sejam inseridas no código-fonte ou disponibilizadas no repositório do GitHub.

O projeto terá como prioridade a utilização de ferramentas gratuitas e modelos executados localmente, garantindo que a plataforma possa funcionar sem depender de serviços pagos. A escolha definitiva dos modelos será realizada considerando a capacidade de processamento dos computadores disponíveis para os integrantes do grupo.

## 10. Considerações Finais

A proposta do projeto é desenvolver uma ferramenta que facilite a avaliação e a comparação de diferentes modelos de Inteligência Artificial, permitindo analisar seus resultados de maneira organizada e objetiva.

Com o avanço do desenvolvimento, a plataforma deverá oferecer recursos para testes automatizados, avaliações humanas, comparação de desempenho e geração de resultados que auxiliem na identificação das vantagens e limitações de cada modelo.

Dessa forma, o projeto busca contribuir para uma compreensão mais prática sobre o funcionamento, a qualidade e a eficiência dos modelos de Inteligência Artificial.

Um Pouco das funcionalidades:

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

