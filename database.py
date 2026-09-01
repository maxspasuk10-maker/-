"""Асинхронная работа с SQLite."""
import datetime
from typing import Optional

import aiosqlite


class Database:
    """Обертка над aiosqlite."""

    def __init__(self, db_path: str = "looksmaxing.db") -> None:
        self.db_path = db_path

    async def _connect(self) -> aiosqlite.Connection:
        return await aiosqlite.connect(self.db_path)

    async def init(self) -> None:
        """Создать таблицы при первом запуске."""
        async with await self._connect() as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    school_class TEXT,
                    status TEXT DEFAULT 'PENDING',
                    score REAL,
                    feedback TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    admin_chat_id INTEGER,
                    group_chat_id INTEGER,
                    invite_link TEXT
                )
                """
            )
            await db.execute(
                """
                INSERT OR IGNORE INTO settings (id, admin_chat_id, group_chat_id, invite_link)
                VALUES (1, NULL, NULL, NULL)
                """
            )
            await db.commit()

    async def add_user(
        self,
        telegram_id: int,
        full_name: Optional[str] = None,
        school_class: Optional[str] = None,
    ) -> None:
        async with await self._connect() as db:
            await db.execute(
                """
                INSERT OR REPLACE INTO users (telegram_id, full_name, school_class, status, created_at)
                VALUES (?, ?, ?, 'PENDING', ?)
                """,
                (telegram_id, full_name, school_class, datetime.datetime.now()),
            )
            await db.commit()

    async def set_score_and_feedback(
        self,
        telegram_id: int,
        score: float,
        feedback: Optional[str] = None,
    ) -> None:
        status = "APPROVED" if score >= 4.0 else "REJECTED"
        async with await self._connect() as db:
            await db.execute(
                """
                UPDATE users
                SET score = ?, feedback = ?, status = ?
                WHERE telegram_id = ?
                """,
                (score, feedback, status, telegram_id),
            )
            await db.commit()

    async def get_user(self, telegram_id: int) -> Optional[dict]:
        async with await self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_settings(self) -> dict:
        async with await self._connect() as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM settings WHERE id = 1") as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else {}

    async def update_invite_link(self, link: str) -> None:
        async with await self._connect() as db:
            await db.execute(
                "UPDATE settings SET invite_link = ? WHERE id = 1", (link,)
            )
            await db.commit()


db = Database()
