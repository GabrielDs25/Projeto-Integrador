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
                UNIQUE (run_id, case_id, model)
            );
            CREATE INDEX IF NOT EXISTS idx_model_results_run
                ON model_results(run_id);
            """
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
) -> None:
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO model_results
                (run_id, case_id, model, response, seconds, error)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (run_id, case_id, model, response, seconds, error),
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
            SELECT case_id, model, response, seconds, error
            FROM model_results
            WHERE run_id = ?
            ORDER BY CAST(case_id AS INTEGER), model
            """,
            (run_id,),
        ).fetchall()
    return [dict(row) for row in rows]
