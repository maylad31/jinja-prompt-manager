import sqlite3
from typing import Optional, List, Tuple
import os

DB_DIR = os.path.join(os.path.dirname(__file__), ".", "data")
DB_PATH = os.path.join(DB_DIR, "prompts.db")
os.makedirs(DB_DIR, exist_ok=True)


def initialize_db() -> None:
    """Create table for prompt versioning if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem TEXT NOT NULL,
            version INTEGER NOT NULL DEFAULT 1,
            prompt TEXT NOT NULL,
            model_name TEXT NOT NULL,
            score REAL,
            comment TEXT,
            production BOOLEAN DEFAULT FALSE
        )
        """
        )
        conn.commit()


def set_production_prompt(problem: str, model_name: str, version: int) -> None:
    """Set a specific version of a prompt as the production version, ensuring only one per (problem, model_name)."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Set all other versions to production = FALSE
        cursor.execute(
            """
            UPDATE prompt_versions
            SET production = FALSE
            WHERE problem = ? AND model_name = ?
        """,
            (problem, model_name),
        )

        # Now set the specified version to production = TRUE
        cursor.execute(
            """
            UPDATE prompt_versions
            SET production = TRUE
            WHERE problem = ? AND model_name = ? AND version = ?
        """,
            (problem, model_name, version),
        )

        conn.commit()


def save_prompt(
    problem: str,
    model_name: str,
    prompt: str,
    score: float = None,
    comment: str = None,
    production: bool = False,
) -> None:
    """Save a new version of the prompt in the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Get the latest version number
        cursor.execute(
            "SELECT MAX(version) FROM prompt_versions WHERE problem = ? AND model_name = ?",
            (problem, model_name),
        )
        latest_version = cursor.fetchone()[0]
        new_version = (latest_version or 0) + 1

        # Insert new prompt version
        cursor.execute(
            """
            INSERT INTO prompt_versions (problem, model_name, version, prompt,score,comment,production)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (problem, model_name, new_version, prompt, score, comment, production),
        )
        conn.commit()


def get_production_prompt(problem: str, model_name: str) -> Optional[str]:
    """Retrieve the production version of a prompt for a given problem and model."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT prompt FROM prompt_versions
            WHERE problem = ? AND model_name = ?
            AND production = TRUE
        """,
            (problem, model_name),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def get_all_prompts(problem: str, model_name: str) -> List[Tuple[str, int, bool]]:
    """Retrieve all versions of a given prompt."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT problem, version, prompt, model_name, score, comment, production FROM prompt_versions
            WHERE problem = ? AND model_name = ?
            ORDER BY version DESC
        """,
            (problem, model_name),
        )
        results = cursor.fetchall()

        keys = [
            "problem",
            "version",
            "prompt",
            "model_name",
            "score",
            "comment",
            "production",
        ]
        return [dict(zip(keys, row)) for row in results]


def update_score(
    problem: str, model_name: str, version: int, score: float, comment: str
) -> bool:
    """Update all details of a specific prompt version."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE prompt_versions
            SET score = ?, comment = ?
            WHERE problem = ? AND model_name = ? AND version = ?
        """,
            (score, comment, problem, model_name, version),
        )

        conn.commit()
        return cursor.rowcount > 0


def get_prompt(problem: str, model_name: str, version: int) -> Optional[str]:
    """Retrieve a specific version of a prompt."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT prompt FROM prompt_versions
            WHERE problem = ? AND model_name = ? AND version = ?
        """,
            (problem, model_name, version),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def delete_prompt(problem: str, model_name: str, version: int) -> None:
    """Delete a specific version of a prompt"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM prompt_versions
            WHERE problem = ? AND model_name = ? AND version = ?
        """,
            (problem, model_name, version),
        )


def delete_all_prompts(problem: str, model_name: str) -> None:
    """Delete a specific version of a prompt"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM prompt_versions
            WHERE problem = ? AND model_name = ?
        """,
            (problem, model_name),
        )


def remove_db() -> None:
    """Delete the database file."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
