from src.results_store import create_run, get_run_results, list_runs, save_result


def test_run_and_results_are_persisted(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "EVALUATION_DB_PATH", str(tmp_path / "nested" / "results.sqlite3")
    )

    run_id = create_run(["modelo-a", "modelo-b"], cases_count=1)
    save_result(run_id, "1", "modelo-a", "Resposta", 1.25)
    save_result(run_id, "1", "modelo-b", None, None, "modelo indisponivel")

    runs = list_runs()
    assert len(runs) == 1
    assert runs[0]["id"] == run_id
    assert runs[0]["created_at"]
    assert runs[0]["models"] == ["modelo-a", "modelo-b"]
    assert runs[0]["cases_count"] == 1
    assert get_run_results(run_id) == [
        {
            "case_id": "1",
            "model": "modelo-a",
            "response": "Resposta",
            "seconds": 1.25,
            "error": None,
        },
        {
            "case_id": "1",
            "model": "modelo-b",
            "response": None,
            "seconds": None,
            "error": "modelo indisponivel",
        },
    ]
