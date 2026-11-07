"""Persistência local das execuções e respostas dos modelos."""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def database_path() -> Path:
    configured_path = os.getenv("EVALUATION_DB_PATH")
    if configured_path:
        return Path(configured_path)
    return Path(__file__).resolve().parents[1] / "data" / "evaluations.sqlite3"


def _connect() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS evaluation_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                models_json TEXT NOT NULL,
                cases_count INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS model_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL REFERENCES evaluation_runs(id),
                case_id TEXT NOT NULL,
                model TEXT NOT NULL,
                response TEXT,
                seconds REAL,
                error TEXT,
                correct INTEGER,
                score REAL,
                UNIQUE (run_id, case_id, model)
            );
            CREATE TABLE IF NOT EXISTS human_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL REFERENCES evaluation_runs(id),
                case_id TEXT NOT NULL,
                model TEXT NOT NULL,
                score INTEGER NOT NULL,
                notes TEXT,
                UNIQUE (run_id, case_id, model)
            );
            CREATE INDEX IF NOT EXISTS idx_model_results_run
                ON model_results(run_id);
            CREATE INDEX IF NOT EXISTS idx_human_evaluations_run
                ON human_evaluations(run_id);
            """
        )

        columns = {
            "correct": "INTEGER",
            "score": "REAL",
        }
        existing_columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(model_results)").fetchall()
        }
        for column_name, column_type in columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE model_results ADD COLUMN {column_name} {column_type};"
                )


def create_run(models: list[str], cases_count: int) -> int:
    initialize_database()
    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO evaluation_runs (created_at, models_json, cases_count)
            VALUES (?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                json.dumps(models, ensure_ascii=False),
                cases_count,
            ),
        )
        return int(cursor.lastrowid)


def save_result(
    run_id: int,
    case_id: str,
    model: str,
    response: str | None,
    seconds: float | None,
    error: str | None = None,
    *,
    correct: bool | None = None,
    score: float | None = None,
) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO model_results
                (run_id, case_id, model, response, seconds, error, correct, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                case_id,
                model,
                response,
                seconds,
                error,
                None if correct is None else int(correct),
                score,
            ),
        )


def list_runs() -> list[dict[str, Any]]:
    initialize_database()
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, created_at, models_json, cases_count
            FROM evaluation_runs
            ORDER BY id DESC
            """
        ).fetchall()
    return [
        {
            "id": row["id"],
            "created_at": row["created_at"],
            "models": json.loads(row["models_json"]),
            "cases_count": row["cases_count"],
        }
        for row in rows
    ]


def get_run_results(run_id: int) -> list[dict[str, Any]]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT case_id, model, response, seconds, error, correct, score
            FROM model_results
            WHERE run_id = ?
            ORDER BY CAST(case_id AS INTEGER), model
            """,
            (run_id,),
        ).fetchall()

    result = []
    for row in rows:
        item = dict(row)
        if item.get("correct") is None:
            item.pop("correct", None)
        if item.get("score") is None:
            item.pop("score", None)
        result.append(item)
    return result


def save_human_evaluation(
    run_id: int,
    case_id: str,
    model: str,
    score: int,
    notes: str | None = None,
) -> None:
    """Salva a avaliação subjetiva de um avaliador humano para um caso/modelo."""
    initialize_database()
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO human_evaluations (run_id, case_id, model, score, notes)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(run_id, case_id, model)
            DO UPDATE SET score = excluded.score, notes = excluded.notes
            """,
            (run_id, case_id, model, int(score), notes or ""),
        )


def get_human_evaluations(run_id: int) -> list[dict[str, Any]]:
    initialize_database()
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT case_id, model, score, notes
            FROM human_evaluations
            WHERE run_id = ?
            ORDER BY CAST(case_id AS INTEGER), model
            """,
            (run_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_human_comparison(run_id: int) -> list[dict[str, Any]]:
    """Combina avaliação automática e humana para comparar notas por modelo."""
    initialize_database()
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                m.case_id,
                m.model,
                m.score AS auto_score,
                h.score AS human_score,
                h.notes
            FROM model_results m
            LEFT JOIN human_evaluations h
                ON h.run_id = m.run_id
               AND h.case_id = m.case_id
               AND h.model = m.model
            WHERE m.run_id = ?
            ORDER BY CAST(m.case_id AS INTEGER), m.model
            """,
            (run_id,),
        ).fetchall()
    return [dict(row) for row in rows]
