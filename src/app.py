from pathlib import Path

import ollama
import pandas as pd
import streamlit as st

from src.evaluation import concordance_rate, evaluate_response
from src.model_runner import create_client, generate_answer, list_models
from src.results_store import (
    create_run,
    get_human_comparison,
    get_human_evaluations,
    get_run_results,
    list_runs,
    save_human_evaluation,
    save_result,
)

st.set_page_config(page_title="Avaliação de modelos de IA", page_icon="🧪", layout="wide")
st.title("🧪 Avaliação de modelos de IA")
st.caption(
    "Escolha os modelos e as perguntas, execute a avaliação e consulte os resultados."
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

try:
    ollama_client = create_client()
    available_models = list_models(ollama_client)
    ollama_error = None
except (ConnectionError, ollama.RequestError, ollama.ResponseError) as error:
    ollama_client = None
    available_models = []
    ollama_error = error

with st.sidebar:
    st.header("1. Configure a avaliação")

    if ollama_error:
        st.warning("Ollama desconectado")
    elif available_models:
        st.success(f"Ollama conectado · {len(available_models)} modelo(s)")
    else:
        st.info("Ollama conectado, mas sem modelos instalados.")

    selected_models = st.multiselect(
        "Modelos",
        options=available_models,
        default=available_models[: min(3, len(available_models))],
        help="Escolha os modelos que responderão às mesmas perguntas.",
    )

    st.divider()
    st.markdown("**Escolha as perguntas**")
    search = st.text_input("Buscar pergunta", placeholder="Ex.: variável, função...")
    topics = sorted(cases["tema"].dropna().unique().tolist())
    selected_topic = st.selectbox(
        "Tema",
        options=["Todos os temas", *topics],
        help="Escolha um tema ou mantenha todos para incluir a base inteira.",
    )

    filtered_cases = cases
    if selected_topic != "Todos os temas":
        filtered_cases = filtered_cases[filtered_cases["tema"] == selected_topic]
    if search:
        filtered_cases = filtered_cases[
            filtered_cases["pergunta"].str.contains(
                search, case=False, na=False, regex=False
            )
        ]

    if len(filtered_cases) > 1:
        case_limit = st.slider(
            "Quantidade de perguntas",
            min_value=1,
            max_value=len(filtered_cases),
            value=min(5, len(filtered_cases)),
            help="Comece com poucas perguntas. Para usar todas, arraste até o máximo.",
        )
    elif len(filtered_cases) == 1:
        case_limit = 1
        st.caption("1 pergunta encontrada.")
    else:
        case_limit = 0
        st.caption("Nenhuma pergunta encontrada. Ajuste a busca ou os temas.")

    st.caption(
        f"{len(filtered_cases)} de {len(cases)} perguntas correspondem aos filtros."
    )

st.subheader("Resumo")
metric_cases, metric_topics, metric_filtered = st.columns(3)
metric_cases.metric("Perguntas cadastradas", len(cases))
metric_topics.metric("Temas", len(topics))
metric_filtered.metric("Perguntas selecionadas", len(filtered_cases))

if ollama_error:
    st.error(
        "Não foi possível acessar o Ollama. Abra o Ollama e tente atualizar esta página. "
        f"Detalhes: {ollama_error}"
    )
elif not available_models:
    st.info(
        "Para começar, instale um modelo no Ollama. Exemplo: "
        "`ollama pull llama3.2:3b`. Depois, atualize esta página."
    )

st.subheader("2. Execute a avaliação")
if selected_models and case_limit:
    st.write(
        f"Serão feitas **{case_limit} pergunta(s)** em "
        f"**{len(selected_models)} modelo(s)** "
        f"(**{case_limit * len(selected_models)} respostas** no total)."
    )
else:
    st.write("Selecione ao menos um modelo e uma ou mais perguntas na barra lateral.")

if st.button(
    "▶ Iniciar avaliação",
    type="primary",
    disabled=not selected_models or not case_limit or ollama_client is None,
):
    selected_cases = filtered_cases.head(case_limit)
    run_id = create_run(selected_models, len(selected_cases))
    progress = st.progress(0, text="Preparando avaliação...")
    total = len(selected_cases) * len(selected_models)
    completed = 0
    failures = 0

    for _, case in selected_cases.iterrows():
        for model in selected_models:
            try:
                answer, seconds = generate_answer(
                    ollama_client, model, str(case["pergunta"])
                )
                evaluation = evaluate_response(
                    str(case["resposta_referencia"]),
                    answer,
                    str(case["criterio_aprovacao"]),
                )
                save_result(
                    run_id,
                    str(case["id"]),
                    model,
                    answer,
                    seconds,
                    correct=evaluation["correct"],
                    score=evaluation["score"],
                )
            except (ConnectionError, ollama.RequestError, ollama.ResponseError) as error:
                failures += 1
                save_result(run_id, str(case["id"]), model, None, None, str(error))
            completed += 1
            progress.progress(
                completed / total,
                text=f"Executando resposta {completed} de {total}...",
            )

    if failures:
        st.warning(
            f"Avaliação {run_id} salva com {failures} falha(s). "
            "Os erros aparecem nos resultados."
        )
    else:
        st.success(f"Avaliação {run_id} concluída e salva.")

results_tab, human_tab, cases_tab = st.tabs([
    "📊 Resultados",
    "🧑‍⚕️ Avaliação humana",
    "📚 Casos de teste",
])

with results_tab:
    st.subheader("3. Consulte os resultados")
    runs = list_runs()
    if not runs:
        st.info(
            "Ainda não há resultados. Configure uma avaliação na barra lateral e "
            "clique em **Iniciar avaliação**."
        )
    else:
        run_options = {
            f"Avaliação {run['id']} · {run['created_at'][:16].replace('T', ' ')} · "
            f"{', '.join(run['models'])} · {run['cases_count']} pergunta(s)": run["id"]
            for run in runs
        }
        selected_run_label = st.selectbox(
            "Avaliação para consultar", options=list(run_options)
        )
        run_results = get_run_results(run_options[selected_run_label])
        results_frame = pd.DataFrame(run_results)

        if not results_frame.empty:
            successful_results = results_frame[results_frame["error"].isna()].copy()
            if not successful_results.empty:
                successful_results["correct"] = successful_results["correct"].fillna(False).astype(bool)
                summary = (
                    successful_results.groupby("model")
                    .agg(
                        respostas=("response", "count"),
                        acuracia=("correct", "mean"),
                        score_medio=("score", "mean"),
                        tempo_medio_segundos=("seconds", "mean"),
                    )
                    .reset_index()
                    .rename(
                        columns={
                            "model": "Modelo",
                            "respostas": "Respostas",
                            "acuracia": "Acurácia",
                            "score_medio": "Nota média",
                            "tempo_medio_segundos": "Tempo médio (s)",
                        }
                    )
                )
                summary["Acurácia"] = (summary["Acurácia"] * 100).round(1)
                summary["Nota média"] = summary["Nota média"].round(2)
                summary["Tempo médio (s)"] = summary["Tempo médio (s)"].round(2)
                st.dataframe(
                    summary,
                    hide_index=True,
                    use_container_width=True,
                )

                geral = successful_results["correct"].mean() if not successful_results.empty else 0.0
                st.metric("Acurácia geral", f"{geral * 100:.1f}%")

            comparison = pd.DataFrame(get_human_comparison(run_options[selected_run_label]))
            if not comparison.empty:
                comparison["auto_score"] = pd.to_numeric(comparison["auto_score"], errors="coerce")
                comparison["human_score"] = pd.to_numeric(comparison["human_score"], errors="coerce")
                comparison = comparison.dropna(subset=["auto_score", "human_score"])
                if not comparison.empty:
                    comparison_rows = []
                    for model_name, model_rows in comparison.groupby("model"):
                        model_pairs = [
                            {"score": float(auto), "human_score": float(human)}
                            for auto, human in zip(model_rows["auto_score"], model_rows["human_score"])
                        ]
                        comparison_rows.append(
                            {
                                "model": model_name,
                                "nota_automatica": model_rows["auto_score"].mean(),
                                "nota_humana": model_rows["human_score"].mean(),
                                "concordancia": concordance_rate(
                                    model_pairs,
                                    auto_key="score",
                                    human_key="human_score",
                                ),
                            }
                        )
                    comparison_summary = pd.DataFrame(comparison_rows)
                    comparison_summary["nota_automatica"] = comparison_summary["nota_automatica"].round(2)
                    comparison_summary["nota_humana"] = comparison_summary["nota_humana"].round(2)
                    comparison_summary["concordancia"] = (comparison_summary["concordancia"] * 100).round(1)
                    st.subheader("Concordância automática vs. humana")
                    comparison_display = comparison_summary.rename(
                        columns={
                            "model": "Modelo",
                            "nota_automatica": "Nota automática",
                            "nota_humana": "Nota humana",
                            "concordancia": "Concordância (%)",
                        }
                    )
                    st.dataframe(
                        comparison_display,
                        hide_index=True,
                        use_container_width=True,
                    )
                    concordancia_geral = comparison_display["Concordância (%)"].mean()
                    st.metric("Concordância geral", f"{concordancia_geral:.1f}%")
                    st.download_button(
                        "Baixar comparação em CSV",
                        data=comparison_display.to_csv(index=False).encode("utf-8-sig"),
                        file_name=f"comparacao_humana_{run_options[selected_run_label]}.csv",
                        mime="text/csv",
                    )

            display_results = results_frame.rename(
                columns={
                    "case_id": "Caso",
                    "model": "Modelo",
                    "response": "Resposta",
                    "seconds": "Tempo (s)",
                    "error": "Falha",
                    "correct": "Aprovado",
                    "score": "Nota",
                }
            )
            display_results["Aprovado"] = display_results["Aprovado"].map(
                {1: True, 0: False}
            )
            if display_results["Falha"].isna().all():
                display_results = display_results.drop(columns=["Falha"])
            with st.expander("Ver respostas detalhadas"):
                st.dataframe(
                    display_results, hide_index=True, use_container_width=True
                )
            st.download_button(
                "Baixar resultados em CSV",
                data=results_frame.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"resultados_avaliacao_{run_options[selected_run_label]}.csv",
                mime="text/csv",
            )

with human_tab:
    st.subheader("4. Registrar avaliação humana")
    runs = list_runs()
    if not runs:
        st.info("Ainda não há avaliações para receber notas humanas.")
    else:
        run_options = {
            f"Avaliação {run['id']} · {run['created_at'][:16].replace('T', ' ')}": run["id"]
            for run in runs
        }
        selected_run_label = st.selectbox(
            "Selecione a avaliação",
            options=list(run_options),
            key="human_run_select",
        )
        selected_run_id = run_options[selected_run_label]
        selected_run_results = pd.DataFrame(get_run_results(selected_run_id))
        if selected_run_results.empty:
            st.info("Esta avaliação ainda não possui respostas registradas.")
        else:
            human_candidates = selected_run_results[selected_run_results["error"].isna()]
            if human_candidates.empty:
                st.info("Não há respostas válidas para receber avaliação humana.")
            else:
                case_id = st.selectbox(
                    "Caso",
                    options=human_candidates["case_id"].tolist(),
                    key="human_case_select",
                )
                model = st.selectbox(
                    "Modelo",
                    options=sorted(human_candidates[human_candidates["case_id"] == case_id]["model"].tolist()),
                    key="human_model_select",
                )
                row = human_candidates[
                    (human_candidates["case_id"] == case_id)
                    & (human_candidates["model"] == model)
                ].iloc[0]
                st.write("**Resposta do modelo**")
                st.write(row.get("response", ""))

                with st.form("human_evaluation_form"):
                    score = st.slider("Nota humana (0 a 5)", 0, 5, 3)
                    notes = st.text_area("Observações da avaliação")
                    submitted = st.form_submit_button("Salvar avaliação humana")
                    if submitted:
                        save_human_evaluation(selected_run_id, str(case_id), model, int(score), notes)
                        st.success("Avaliação humana salva com sucesso.")

                existing_human = pd.DataFrame(get_human_evaluations(selected_run_id))
                if not existing_human.empty:
                    human_table = existing_human.rename(
                        columns={
                            "case_id": "Caso",
                            "model": "Modelo",
                            "score": "Nota humana",
                            "notes": "Observações",
                        }
                    )
                    st.dataframe(human_table, hide_index=True, use_container_width=True)

with cases_tab:
    st.subheader("Conheça os casos de teste")
    if filtered_cases.empty:
        st.info("Nenhum caso corresponde à busca e aos temas selecionados.")
    else:
        cases_by_topic = (
            filtered_cases.groupby("tema")
            .size()
            .rename("Perguntas")
            .sort_values(ascending=False)
        )
        st.bar_chart(cases_by_topic)
        st.dataframe(
            filtered_cases[["id", "tema", "pergunta"]].rename(
                columns={"id": "Caso", "tema": "Tema", "pergunta": "Pergunta"}
            ),
            hide_index=True,
            use_container_width=True,
        )

        selected_case_id = st.selectbox(
            "Ver resposta esperada e critério",
            options=filtered_cases["id"].tolist(),
            format_func=lambda case_id: (
                f"Caso {case_id} · "
                f"{filtered_cases.loc[filtered_cases['id'] == case_id, 'pergunta'].iloc[0][:70]}"
                "..."
            ),
        )
        selected_case = filtered_cases.loc[
            filtered_cases["id"] == selected_case_id
        ].iloc[0]
        with st.container(border=True):
            st.markdown("**Resposta de referência**")
            st.write(selected_case["resposta_referencia"])
            st.markdown("**O que a resposta deve conter**")
            st.write(selected_case["criterio_aprovacao"])

        st.download_button(
            "Baixar perguntas filtradas em CSV",
            data=filtered_cases.to_csv(index=False).encode("utf-8-sig"),
            file_name="casos_de_teste.csv",
            mime="text/csv",
        )
