from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Avaliação de modelos de IA", page_icon="🧪", layout="wide")
st.title("🧪 Plataforma de Avaliação de Modelos de IA")
st.write(
    "Consulte e revise os casos de teste preparados para avaliar respostas de modelos."
)
st.info(
    "Esta etapa apresenta o conjunto de testes. A execução de modelos e as métricas "
    "de desempenho ainda não estão integradas; nenhum resultado de modelo é simulado."
)

cases_path = Path(__file__).resolve().parents[1] / "eval" / "casos_exemplo.csv"
required_columns = {
    "id",
    "pergunta",
    "resposta_referencia",
    "criterio_aprovacao",
    "tema",
}
cases = pd.read_csv(cases_path)
missing_columns = required_columns.difference(cases.columns)
if missing_columns:
    st.error(
        "O arquivo de casos está sem as colunas obrigatórias: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

topics = sorted(cases["tema"].dropna().unique().tolist())
search_column, topic_column = st.columns([2, 1])
search = search_column.text_input(
    "Buscar pergunta", placeholder="Digite palavras da pergunta..."
)
selected_topics = topic_column.multiselect(
    "Filtrar por tema",
    options=topics,
    default=topics,
)

filtered_cases = cases[cases["tema"].isin(selected_topics)]
if search:
    filtered_cases = filtered_cases[
        filtered_cases["pergunta"].str.contains(
            search, case=False, na=False, regex=False
        )
    ]

metric_column, topics_column, visible_column = st.columns(3)
metric_column.metric("Casos cadastrados", len(cases))
topics_column.metric("Temas", len(topics))
visible_column.metric("Casos encontrados", len(filtered_cases))

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
        use_container_width=True,
    )

    case_ids = filtered_cases["id"].tolist()
    selected_case_id = st.selectbox("Consultar detalhes do caso", options=case_ids)
    selected_case = filtered_cases.loc[filtered_cases["id"] == selected_case_id].iloc[0]

    with st.expander(f"Caso {selected_case_id}: resposta e critério"):
        st.markdown("**Resposta de referência**")
        st.write(selected_case["resposta_referencia"])
        st.markdown("**Critério de aprovação**")
        st.write(selected_case["criterio_aprovacao"])

    st.download_button(
        "Baixar casos filtrados em CSV",
        data=filtered_cases.to_csv(index=False).encode("utf-8-sig"),
        file_name="casos_de_teste.csv",
        mime="text/csv",
    )
