from pathlib import Path

import pandas as pd
import ollama
import streamlit as st

from src.model_runner import (
    create_client,
    generate_answer,
    list_models,
)
from src.results_store import create_run, get_run_results, list_runs, save_result

st.set_page_config(page_title="Avaliação de modelos de IA", page_icon="🧪", layout="wide")
st.title("🧪 Plataforma de Avaliação de Modelos de IA")
st.write(
    "Execute os mesmos casos em modelos locais, salve as respostas e compare os resultados."
)
st.info(
    "As respostas e os tempos são coletados de execuções reais. A aprovação automática "
    "e a avaliação humana serão adicionadas em etapas futuras."
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

st.subheader("Executar avaliação com Ollama")
try:
    ollama_client = create_client()
    available_models = list_models(ollama_client)
except (ConnectionError, ollama.RequestError, ollama.ResponseError) as error:
    st.error(
        "Não foi possível acessar o Ollama. Inicie o Ollama e confirme a conexão "
        "em OLLAMA_HOST. Detalhes: " + str(error)
    )
    available_models = []

if not available_models:
    st.warning(
        "Nenhum modelo local foi encontrado. Instale modelos com `ollama pull "
        "nome-do-modelo` e atualize a página."
    )
else:
    selected_models = st.multiselect(
        "Modelos para comparar",
        options=available_models,
        default=available_models[: min(3, len(available_models))],
        help="Selecione um ou mais modelos instalados no Ollama.",
    )
    if filtered_cases.empty:
        st.warning("Selecione casos usando os filtros antes de iniciar uma avaliação.")
    else:
        if len(filtered_cases) == 1:
            case_limit = 1
            st.caption("A execução inclui o único caso selecionado.")
        else:
            case_limit = st.slider(
                "Casos nesta execução",
                min_value=1,
                max_value=len(filtered_cases),
                value=min(10, len(filtered_cases)),
                help="Comece com poucos casos para validar os modelos; aumente para executar "
                "o conjunto completo.",
            )
        if st.button("Iniciar avaliação", type="primary", disabled=not selected_models):
            selected_cases = filtered_cases.head(case_limit)
            run_id = create_run(selected_models, len(selected_cases))
            progress = st.progress(0, text="Preparando execução...")
            total = len(selected_cases) * len(selected_models)
            completed = 0
            failures = 0

            for _, case in selected_cases.iterrows():
                for model in selected_models:
                    try:
                        answer, seconds = generate_answer(
                            ollama_client, model, str(case["pergunta"])
                        )
                        save_result(
                            run_id,
                            str(case["id"]),
                            model,
                            answer,
                            seconds,
                        )
                    except (
                        ConnectionError,
                        ollama.RequestError,
                        ollama.ResponseError,
                    ) as error:
                        failures += 1
                        save_result(
                            run_id,
                            str(case["id"]),
                            model,
                            None,
                            None,
                            str(error),
                        )
                    completed += 1
                    progress.progress(
                        completed / total,
                        text=f"Executando {completed} de {total} respostas...",
                    )

            if failures:
                st.warning(
                    f"Execução {run_id} concluída com {failures} falha(s). "
                    "Os erros foram registrados junto aos resultados."
                )
            else:
                st.success(f"Execução {run_id} concluída e salva.")

st.subheader("Resultados salvos")
runs = list_runs()
if not runs:
    st.caption("Ainda não há execuções registradas.")
else:
    run_options = {
        f"Execução {run['id']} · {run['created_at']} · "
        f"{', '.join(run['models'])} · {run['cases_count']} casos": run["id"]
        for run in runs
    }
    selected_run_label = st.selectbox(
        "Consultar execução", options=list(run_options)
    )
    run_results = get_run_results(run_options[selected_run_label])
    results_frame = pd.DataFrame(run_results)
    if not results_frame.empty:
        successful_results = results_frame[results_frame["error"].isna()]
        if not successful_results.empty:
            summary = (
                successful_results.groupby("model")
                .agg(
                    respostas=("response", "count"),
                    tempo_medio_segundos=("seconds", "mean"),
                )
                .reset_index()
            )
            st.dataframe(summary, hide_index=True, use_container_width=True)
        st.dataframe(results_frame, hide_index=True, use_container_width=True)
        st.download_button(
            "Baixar resultados da execução em CSV",
            data=results_frame.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"resultados_execucao_{run_options[selected_run_label]}.csv",
            mime="text/csv",
        )

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
