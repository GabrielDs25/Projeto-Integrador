# Tema 3 – Plataforma de Avaliação de LLMs e Agentes

**Curso:** EAD_PROINT_100.DD-ADS-PI-10-74.2026.74

**Disciplina:** Projeto Integrador

**Integrantes:**

- **Integrante 1:** Gabriel dos Santos – RA: 2411597
- **Integrante 2:** Leonardo Henrique Félix – RA: 2410717
- **Integrante 3:** Mateus Felipe Silva Pacheco – RA: 2411247

`782461515b80a2be77eacf10b65b2820b9e860b5`

---

## 1. Apresentação do Projeto

O projeto consiste no desenvolvimento de uma plataforma destinada à avaliação e comparação de modelos de Inteligência Artificial (LLMs) e agentes inteligentes.

A ferramenta tem como principal finalidade permitir a execução de testes padronizados, o registro das respostas geradas e a análise comparativa do desempenho de diferentes modelos, considerando critérios como qualidade das respostas, precisão, consistência e tempo de execução.

**Estado atual do projeto:** A plataforma encontra-se em sua versão inicial, correspondente ao Marco 1. Nesta etapa, a interface utiliza dados de exemplo para demonstrar suas funcionalidades. A integração com modelos reais de Inteligência Artificial será implementada nas próximas fases do desenvolvimento.

## 2. Objetivos do Projeto

Desenvolver uma plataforma capaz de enviar as mesmas perguntas para três modelos diferentes de Inteligência Artificial, registrar as respostas obtidas e apresentar uma comparação dos resultados.

Além disso, o sistema deverá permitir a avaliação automática das respostas e a comparação desses resultados com avaliações realizadas por pessoas. Dessa forma, será possível identificar diferenças entre as avaliações, analisar a qualidade das respostas e reconhecer os pontos fortes e as limitações de cada modelo.

O projeto também busca proporcionar uma maneira organizada e padronizada de avaliar modelos de IA, facilitando a interpretação dos resultados e a identificação de possíveis melhorias.

## 3. Tecnologias Utilizadas

O desenvolvimento utiliza tecnologias de código aberto e ferramentas gratuitas, priorizando a execução local e reduzindo a dependência de serviços pagos.

As principais tecnologias previstas são:

- **Python:** linguagem principal utilizada no desenvolvimento da aplicação.
- **Streamlit:** ferramenta utilizada para criação da interface gráfica e visualização dos resultados.
- **Ollama:** plataforma para execução local de modelos de Inteligência Artificial.
- **Pytest:** ferramenta responsável pela execução dos testes automatizados.
- **Git e GitHub:** utilizados para controle de versão, armazenamento do código e colaboração entre os integrantes.

## 4. Como Executar o Projeto

**Requisitos recomendados:** Python 3.11 ou 3.12.

Primeiramente, instale o Python e marque a opção *Add Python to PATH* durante a instalação.

Em seguida, abra o terminal dentro da pasta principal do projeto.

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

Com o ambiente virtual ativado, execute o comando:

```bash
python -m pip install -r requirements.txt
```

### 4.3. Iniciar a plataforma

Para iniciar a aplicação e acessar a interface pelo navegador, execute:

```bash
streamlit run src/app.py
```

Após a execução, o Streamlit disponibilizará um endereço local para acessar a plataforma.

## 5. Como Executar os Testes

O projeto utiliza testes automatizados para verificar o funcionamento dos componentes e identificar possíveis erros durante o desenvolvimento.

Para executar os testes, utilize:

```bash
python -m pytest
```

Os resultados permitirão acompanhar a qualidade do código e verificar se as alterações realizadas continuam funcionando corretamente.

## 6. Estrutura do Projeto

A organização dos arquivos foi planejada para facilitar o desenvolvimento, a manutenção e a colaboração entre os integrantes.

- **src/:** contém o código-fonte e os principais componentes da aplicação.
- **tests/:** armazena os testes automatizados responsáveis por verificar o funcionamento do sistema.
- **eval/:** reúne os casos de teste, perguntas e resultados utilizados na avaliação dos modelos.
- **docs/:** contém a documentação técnica e acadêmica do projeto.
- **evidencias/:** armazena capturas de tela, registros, resultados das avaliações e vídeos demonstrativos.
- **PROMPTS.md:** documenta as interações realizadas com ferramentas de Inteligência Artificial durante o desenvolvimento, incluindo os comandos utilizados, resumos das respostas e justificativas para aceitar, modificar ou descartar sugestões.

## 7. Próximas Etapas do Desenvolvimento

Para dar continuidade ao projeto e atender aos requisitos estabelecidos na disciplina, estão previstas as seguintes atividades:

1. Confirmar a escolha do Tema 3 com o professor. **(Concluído)**
2. Criar o repositório compartilhado no GitHub e disponibilizar os arquivos do projeto. **(Concluído)**
3. Implementar a integração contínua (CI), configurando a execução automática dos testes.
4. Integrar modelos reais de Inteligência Artificial, priorizando modelos locais executados por meio do Ollama.
5. Desenvolver e organizar uma base com 100 casos de teste para avaliar os modelos.
6. Realizar avaliações humanas de pelo menos 30 casos, permitindo comparar as avaliações das pessoas com os resultados do avaliador automático.
7. Analisar os resultados obtidos, considerando qualidade das respostas, precisão, consistência e tempo de execução.
8. Identificar e documentar possíveis erros, dificuldades, falhas e limitações encontradas durante os testes.
9. Organizar as evidências do desenvolvimento, incluindo resultados, gráficos, registros e demonstrações da plataforma.

## 8. Funcionalidades da Plataforma

A plataforma está sendo desenvolvida com recursos que facilitam a consulta, a organização e a análise dos casos de teste cadastrados.

### 8.1. Busca de perguntas

Permite pesquisar palavras ou termos específicos para localizar perguntas dentro da base de casos de teste. Essa funcionalidade facilita a identificação de questões e agiliza a navegação pela plataforma.

### 8.2. Filtro por tema

Possibilita selecionar assuntos específicos para visualizar somente as perguntas relacionadas ao tema escolhido, facilitando a organização e a realização de avaliações por categoria.

### 8.3. Indicadores gerais

Apresenta informações quantitativas sobre a base de avaliação, permitindo acompanhar os principais dados cadastrados na plataforma.

Atualmente, os indicadores demonstrados são:

- **100 casos cadastrados:** quantidade total de perguntas disponíveis na base.
- **10 temas:** número de categorias utilizadas para organizar os casos.
- **100 casos encontrados:** quantidade de registros encontrados na consulta apresentada.

### 8.4. Distribuição de casos por tema

Apresenta graficamente a quantidade de perguntas cadastradas em cada categoria. Esse recurso permite visualizar a distribuição dos casos e identificar quais temas possuem maior ou menor quantidade de perguntas.

## 9. Demonstração da Interface da Plataforma

A seguir, estão algumas imagens que demonstram as funcionalidades já desenvolvidas na versão inicial da plataforma.

### 9.1. Busca de perguntas

A funcionalidade de busca permite pesquisar palavras e localizar perguntas específicas dentro dos 100 casos cadastrados.

<img width="993" height="738" alt="Tela de busca de perguntas" src="https://github.com/user-attachments/assets/5c55959c-276e-4113-a8f0-7b7caf78f85f" />

### 9.2. Filtro por tema

Permite selecionar categorias específicas, como coleções, arquivos e testes, exibindo somente as perguntas relacionadas ao assunto escolhido.

<img width="1440" height="776" alt="Tela de filtro por tema" src="https://github.com/user-attachments/assets/da3e0037-9f44-4672-98a7-34d054f5dbba" />

### 9.3. Indicadores gerais

Apresenta um resumo quantitativo da base de avaliação, facilitando a visualização das informações principais.

- 100 casos cadastrados.
- 10 temas disponíveis.
- 100 casos encontrados.

<img width="1166" height="768" alt="Painel de indicadores" src="https://github.com/user-attachments/assets/593410b0-a8f1-45d0-9573-d51189bfe14f" />

### 9.4. Distribuição de casos por tema

Exibe um gráfico com a quantidade de perguntas cadastradas em cada assunto, permitindo visualizar como os casos estão distribuídos entre as diferentes categorias.

<img width="1027" height="777" alt="Gráfico de distribuição de casos por tema" src="https://github.com/user-attachments/assets/7e37c501-09ee-4ad9-9e7b-81c07484e347" />

## 10. Segurança, Privacidade e Custos

Durante o desenvolvimento, serão utilizados exclusivamente dados públicos ou sintéticos, evitando a utilização de informações pessoais reais.

Também serão adotadas medidas para proteger informações confidenciais, garantindo que senhas, chaves de API e outros dados sensíveis não sejam inseridos diretamente no código-fonte ou disponibilizados no repositório do GitHub.

O projeto terá como prioridade a utilização de ferramentas gratuitas e modelos executados localmente, buscando garantir que a plataforma funcione sem depender de serviços pagos.

A escolha definitiva dos modelos será realizada considerando a capacidade de processamento dos computadores disponíveis para os integrantes do grupo.

## 11. Considerações Finais

A proposta do projeto é desenvolver uma ferramenta que facilite a avaliação e a comparação de diferentes modelos de Inteligência Artificial, permitindo analisar seus resultados de maneira organizada, padronizada e objetiva.

Com o avanço do desenvolvimento, a plataforma deverá oferecer recursos para execução de testes automatizados, avaliações humanas, comparação de desempenho e geração de resultados que auxiliem na identificação das vantagens e limitações de cada modelo.

Além disso, a utilização de uma base padronizada de perguntas permitirá realizar comparações mais consistentes, contribuindo para uma avaliação mais confiável dos modelos analisados.

Dessa forma, o projeto busca proporcionar uma experiência prática de desenvolvimento e avaliação de sistemas inteligentes, aplicando conceitos de programação, testes de software, análise de dados e Inteligência Artificial.
