import pandas as pd
import streamlit as st

from evaluation import accuracy_rate, average_response_time

st.set_page_config(page_title="Comparador de IAs", page_icon="🧪", layout="wide")
st.title("🧪 Plataforma de Avaliação de Modelos de IA")
st.write(
    "Projeto acadêmico — Tema 3. Esta primeira tela usa **dados fictícios de exemplo**. "
    "Ela ainda não consulta modelos reais."
)

sample_results = [
    {"Modelo": "Modelo A", "Pergunta": "O que é uma variável?", "Aprovada": True, "Tempo (s)": 1.2},
    {"Modelo": "Modelo A", "Pergunta": "O que é uma função?", "Aprovada": True, "Tempo (s)": 1.4},
    {"Modelo": "Modelo A", "Pergunta": "O que é uma lista?", "Aprovada": False, "Tempo (s)": 1.1},
    {"Modelo": "Modelo B", "Pergunta": "O que é uma variável?", "Aprovada": True, "Tempo (s)": 2.1},
    {"Modelo": "Modelo B", "Pergunta": "O que é uma função?", "Aprovada": False, "Tempo (s)": 2.4},
    {"Modelo": "Modelo B", "Pergunta": "O que é uma lista?", "Aprovada": True, "Tempo (s)": 2.0},
    {"Modelo": "Modelo C", "Pergunta": "O que é uma variável?", "Aprovada": True, "Tempo (s)": 0.9},
    {"Modelo": "Modelo C", "Pergunta": "O que é uma função?", "Aprovada": True, "Tempo (s)": 1.0},
    {"Modelo": "Modelo C", "Pergunta": "O que é uma lista?", "Aprovada": True, "Tempo (s)": 1.1},
]

df = pd.DataFrame(sample_results)
st.info("Atenção: os nomes, acertos e tempos abaixo são inventados apenas para demonstrar a interface.")

selected_models = st.multiselect(
    "Escolha quais modelos de exemplo visualizar",
    options=sorted(df["Modelo"].unique()),
    default=sorted(df["Modelo"].unique()),
)

view = df[df["Modelo"].isin(selected_models)]

if view.empty:
    st.warning("Selecione pelo menos um modelo para ver os resultados.")
else:
    summaries = []
    for model, group in view.groupby("Modelo"):
        metric_rows = [
            {"correct": bool(row["Aprovada"]), "seconds": float(row["Tempo (s)"])}
            for _, row in group.iterrows()
        ]
        summaries.append(
            {
                "Modelo": model,
                "Taxa de aprovação": accuracy_rate(metric_rows),
                "Tempo médio (s)": average_response_time(metric_rows),
            }
        )

    summary_df = pd.DataFrame(summaries)
    col1, col2 = st.columns(2)
    col1.metric("Modelos exibidos", len(summary_df))
    col2.metric("Casos exibidos", len(view))

    st.subheader("Resumo por modelo")
    st.dataframe(
        summary_df.style.format(
            {"Taxa de aprovação": "{:.0%}", "Tempo médio (s)": "{:.2f}"}
        ),
        use_container_width=True,
    )

    st.subheader("Taxa de aprovação")
    st.bar_chart(summary_df.set_index("Modelo")["Taxa de aprovação"])

    st.subheader("Dados de exemplo")
    st.dataframe(view, use_container_width=True)

st.caption(
    "Próxima etapa: substituir os dados fictícios por resultados reais de três modelos "
    "e registrar cada execução."
)
