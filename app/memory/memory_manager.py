"""
Memory Manager
============================================================

Persistent memory for the AI Marketing Strategy Manager.

Purpose:
- Store campaign information
- Retrieve previous campaigns
- Store user preferences/context
- Search campaign history
- Keep memory independent from Groq API calls

Storage:
    SQLite

Database:
    data/marketing_memory.db
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "marketing_memory.db"


# ============================================================
# MEMORY MANAGER
# ============================================================

class MemoryManager:
    """
    Persistent SQLite-based memory manager.

    Stores:
    - campaign information
    - campaign outputs
    - user context
    - arbitrary metadata
    """

    def __init__(self, database_path: Optional[str] = None):
        self.database_path = (
            Path(database_path)
            if database_path
            else DATABASE_PATH
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    # ========================================================
    # DATABASE CONNECTION
    # ========================================================

    def _connect(self):
        connection = sqlite3.connect(
            str(self.database_path)
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ========================================================
    # INITIALIZE DATABASE
    # ========================================================

    def _initialize_database(self):
        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_name TEXT,
                    product TEXT,
                    target_audience TEXT,
                    marketing_goal TEXT,
                    budget TEXT,
                    timeline TEXT,
                    strategy TEXT,
                    final_output TEXT,
                    metadata TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_context (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    # ========================================================
    # SAVE CAMPAIGN
    # ========================================================

    def save_campaign(
        self,
        campaign_name: str = "",
        product: str = "",
        target_audience: str = "",
        marketing_goal: str = "",
        budget: str = "",
        timeline: str = "",
        strategy: str = "",
        final_output: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:

        created_at = datetime.now().isoformat()

        metadata_json = json.dumps(
            metadata or {},
            ensure_ascii=False,
        )

        with self._connect() as connection:

            cursor = connection.execute(
                """
                INSERT INTO campaigns (
                    campaign_name,
                    product,
                    target_audience,
                    marketing_goal,
                    budget,
                    timeline,
                    strategy,
                    final_output,
                    metadata,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    campaign_name,
                    product,
                    target_audience,
                    marketing_goal,
                    budget,
                    timeline,
                    strategy,
                    final_output,
                    metadata_json,
                    created_at,
                ),
            )

            connection.commit()

            return cursor.lastrowid

    # ========================================================
    # GET CAMPAIGN
    # ========================================================

    def get_campaign(
        self,
        campaign_id: int,
    ) -> Optional[Dict[str, Any]]:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT *
                FROM campaigns
                WHERE id = ?
                """,
                (campaign_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_dict(row)

    # ========================================================
    # GET ALL CAMPAIGNS
    # ========================================================

    def get_all_campaigns(
        self,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM campaigns
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    # ========================================================
    # SEARCH CAMPAIGNS
    # ========================================================

    def search_campaigns(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:

        pattern = f"%{query}%"

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM campaigns
                WHERE
                    campaign_name LIKE ?
                    OR product LIKE ?
                    OR target_audience LIKE ?
                    OR marketing_goal LIKE ?
                    OR strategy LIKE ?
                ORDER BY id DESC
                """,
                (
                    pattern,
                    pattern,
                    pattern,
                    pattern,
                    pattern,
                ),
            ).fetchall()

        return [
            self._row_to_dict(row)
            for row in rows
        ]

    # ========================================================
    # SAVE USER CONTEXT
    # ========================================================

    def save_context(
        self,
        key: str,
        value: Any,
    ):

        updated_at = datetime.now().isoformat()

        if not isinstance(value, str):
            value = json.dumps(
                value,
                ensure_ascii=False,
            )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO user_context (
                    key,
                    value,
                    updated_at
                )
                VALUES (?, ?, ?)
                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (
                    key,
                    value,
                    updated_at,
                ),
            )

            connection.commit()

    # ========================================================
    # GET USER CONTEXT
    # ========================================================

    def get_context(
        self,
        key: str,
    ) -> Optional[Any]:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT value
                FROM user_context
                WHERE key = ?
                """,
                (key,),
            ).fetchone()

        if row is None:
            return None

        value = row["value"]

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    # ========================================================
    # GET ALL CONTEXT
    # ========================================================

    def get_all_context(self) -> Dict[str, Any]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT key, value
                FROM user_context
                ORDER BY key
                """
            ).fetchall()

        context = {}

        for row in rows:

            value = row["value"]

            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass

            context[row["key"]] = value

        return context

    # ========================================================
    # DELETE CONTEXT
    # ========================================================

    def delete_context(
        self,
        key: str,
    ) -> bool:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                DELETE FROM user_context
                WHERE key = ?
                """,
                (key,),
            )

            connection.commit()

            return cursor.rowcount > 0

    # ========================================================
    # CLEAR MEMORY
    # ========================================================

    def clear_all_memory(self):

        with self._connect() as connection:

            connection.execute(
                "DELETE FROM campaigns"
            )

            connection.execute(
                "DELETE FROM user_context"
            )

            connection.commit()

    # ========================================================
    # MEMORY SUMMARY
    # ========================================================

    def get_memory_summary(self) -> Dict[str, Any]:

        with self._connect() as connection:

            campaign_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM campaigns
                """
            ).fetchone()[0]

            context_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM user_context
                """
            ).fetchone()[0]

        return {
            "database": str(self.database_path),
            "campaign_count": campaign_count,
            "context_count": context_count,
        }

    # ========================================================
    # INTERNAL ROW CONVERSION
    # ========================================================

    @staticmethod
    def _row_to_dict(
        row: sqlite3.Row,
    ) -> Dict[str, Any]:

        result = dict(row)

        metadata = result.get("metadata")

        if metadata:

            try:
                result["metadata"] = json.loads(
                    metadata
                )
            except (
                json.JSONDecodeError,
                TypeError,
            ):
                pass

        return result


# ============================================================
# DEFAULT MEMORY INSTANCE
# ============================================================

memory_manager = MemoryManager()


# ============================================================
# QUICK HELPER FUNCTIONS
# ============================================================

def save_campaign(**kwargs) -> int:
    return memory_manager.save_campaign(**kwargs)


def get_campaign(
    campaign_id: int,
):
    return memory_manager.get_campaign(
        campaign_id
    )


def get_all_campaigns(
    limit: int = 20,
):
    return memory_manager.get_all_campaigns(
        limit
    )


def search_campaigns(
    query: str,
):
    return memory_manager.search_campaigns(
        query
    )


def save_context(
    key: str,
    value: Any,
):
    return memory_manager.save_context(
        key,
        value,
    )


def get_context(
    key: str,
):
    return memory_manager.get_context(
        key
    )


def get_all_context():
    return memory_manager.get_all_context()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("MEMORY MANAGER")
    print("=" * 60)

    manager = MemoryManager()

    print()
    print("Database:")
    print(manager.database_path)

    print()
    print("Memory summary:")
    print(manager.get_memory_summary())