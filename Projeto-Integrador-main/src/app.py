
from pathlib import Path
import time

import ollama
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Avaliação de modelos de IA",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Plataforma de Avaliação de Modelos de IA")

st.write(
    "Consulte os casos de teste e compare o desempenho "
    "de diferentes modelos de inteligência artificial."
)

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parents[1]
CASES_PATH = BASE_DIR / "eval" / "casos_exemplo.csv"
RESULTS_PATH = BASE_DIR / "eval" / "resultados_avaliacao.csv"

# Modelos disponíveis
MODELOS = [
    "qwen2.5:3b",
    "llama3.2:3b",
    "gemma3:4b"
]

# Carregamento dos casos
required_columns = {
    "id",
    "pergunta",
    "resposta_referencia",
    "criterio_aprovacao",
    "tema",
}

cases = pd.read_csv(CASES_PATH)

missing_columns = required_columns.difference(cases.columns)

if missing_columns:
    st.error(
        "O arquivo de casos está sem as colunas obrigatórias: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

# Filtros
topics = sorted(cases["tema"].dropna().unique().tolist())

search_column, topic_column = st.columns([2, 1])

search = search_column.text_input(
    "Buscar pergunta",
    placeholder="Digite palavras da pergunta..."
)

selected_topics = topic_column.multiselect(
    "Filtrar por tema",
    options=topics,
    default=topics
)

filtered_cases = cases[cases["tema"].isin(selected_topics)]

if search:
    filtered_cases = filtered_cases[
        filtered_cases["pergunta"].str.contains(
            search,
            case=False,
            na=False,
            regex=False
        )
    ]

# Indicadores
metric_column, topics_column, visible_column = st.columns(3)

metric_column.metric("Casos cadastrados", len(cases))
topics_column.metric("Temas", len(topics))
visible_column.metric("Casos encontrados", len(filtered_cases))

# Gráfico e tabela
if filtered_cases.empty:
    st.warning("Nenhum caso corresponde aos filtros selecionados.")

else:
    st.subheader("Distribuição de casos por tema")

    cases_by_topic = (
        filtered_cases.groupby("tema")
        .size()
        .rename("Quantidade de casos")
        .sort_values(ascending=False)
    )

    st.bar_chart(cases_by_topic)

    st.subheader("Casos de teste")

    st.dataframe(
        filtered_cases[["id", "tema", "pergunta"]],
        hide_index=True,
        use_container_width=True
    )

    case_ids = filtered_cases["id"].tolist()

    selected_case_id = st.selectbox(
        "Consultar detalhes do caso",
        options=case_ids
    )

    selected_case = filtered_cases.loc[
        filtered_cases["id"] == selected_case_id
    ].iloc[0]

    with st.expander(f"Caso {selected_case_id}: resposta e critério"):
        st.markdown("**Resposta de referência**")
        st.write(selected_case["resposta_referencia"])

        st.markdown("**Critério de aprovação**")
        st.write(selected_case["criterio_aprovacao"])

    st.download_button(
        "Baixar casos filtrados em CSV",
        data=filtered_cases.to_csv(index=False).encode("utf-8-sig"),
        file_name="casos_de_teste.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# EXECUÇÃO DOS MODELOS DE IA
# --------------------------------------------------

st.divider()

st.header("🤖 Avaliação dos modelos de IA")

st.write(
    "Nesta primeira etapa, serão executados 5 casos "
    "para testar a integração com o Ollama."
)

selected_models = st.multiselect(
    "Selecione os modelos",
    options=MODELOS,
    default=MODELOS
)

if st.button("▶ Iniciar avaliação", type="primary"):

    if not selected_models:
        st.warning("Selecione pelo menos um modelo.")

    else:
        test_cases = cases.head(5)
        results = []

        total = len(test_cases) * len(selected_models)
        completed = 0

        progress = st.progress(0)
        status = st.empty()

        for modelo in selected_models:

            for _, case in test_cases.iterrows():

                status.write(
                    f"Executando {modelo} — Caso {case['id']}"
                )

                inicio = time.perf_counter()

                try:
                    response = ollama.chat(
                        model=modelo,
                        messages=[
                            {
                                "role": "user",
                                "content": str(case["pergunta"])
                            }
                        ]
                    )

                    tempo = time.perf_counter() - inicio

                    resposta = response["message"]["content"]

                    results.append({
                        "id": case["id"],
                        "tema": case["tema"],
                        "pergunta": case["pergunta"],
                        "modelo": modelo,
                        "resposta": resposta,
                        "tempo_segundos": round(tempo, 2),
                        "erro": ""
                    })

                except Exception as error:

                    tempo = time.perf_counter() - inicio

                    results.append({
                        "id": case["id"],
                        "tema": case["tema"],
                        "pergunta": case["pergunta"],
                        "modelo": modelo,
                        "resposta": "",
                        "tempo_segundos": round(tempo, 2),
                        "erro": str(error)
                    })

                completed += 1
                progress.progress(completed / total)

        status.success("Execução finalizada!")

        results_df = pd.DataFrame(results)

        st.session_state["evaluation_results"] = results_df

        results_df.to_csv(
            RESULTS_PATH,
            index=False,
            encoding="utf-8-sig"
        )

        st.success(
            f"{len(results_df)} avaliações registradas com sucesso!"
        )

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------

if "evaluation_results" in st.session_state:

    results_df = st.session_state["evaluation_results"]

    st.divider()
    st.header("📊 Resultados da avaliação")

    successful = results_df[results_df["erro"] == ""]

    if not successful.empty:

        summary = (
            successful.groupby("modelo")
            .agg(
                casos_executados=("id", "count"),
                tempo_medio=("tempo_segundos", "mean")
            )
            .reset_index()
        )

        summary["tempo_medio"] = summary["tempo_medio"].round(2)

        st.subheader("Comparação de desempenho")

        st.dataframe(
            summary,
            hide_index=True,
            use_container_width=True
        )

        st.subheader("Tempo médio por modelo")

        st.bar_chart(
            summary.set_index("modelo")["tempo_medio"]
        )

    st.subheader("Respostas geradas")

    st.dataframe(
        results_df,
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "📥 Baixar resultados em CSV",
        data=results_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="resultados_avaliacao.csv",
        mime="text/csv"
    )

    st.caption(
        "A qualidade das respostas ainda precisa de avaliação "
        "humana. O tempo médio é calculado somente sobre "
        "execuções bem-sucedidas."
    )
