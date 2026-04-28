import aiosqlite
from pathlib import Path
from typing import Optional


class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    async def init_db(self):
        """初始化数据库表结构（异步）"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS player_bindings (
                    qq_id TEXT PRIMARY KEY,
                    game_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()

    async def bind_player(self, qq_id: str, game_id: str) -> bool:
        """绑定玩家"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO player_bindings (qq_id, game_id)
                    VALUES (?, ?)
                ''', (qq_id, game_id))
                await db.commit()
                return True
        except Exception:
            return False

    async def get_game_id(self, qq_id: str) -> Optional[str]:
        """获取游戏 ID"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                    'SELECT game_id FROM player_bindings WHERE qq_id = ?',
                    (qq_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def unbind_player(self, qq_id: str) -> bool:
        """解除绑定"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    'DELETE FROM player_bindings WHERE qq_id = ?',
                    (qq_id,)
                )
                await db.commit()
                return cursor.rowcount > 0
        except Exception:
            return False

    async def get_all_bindings(self) -> list:
        """获取所有绑定记录"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT qq_id, game_id, created_at FROM player_bindings ORDER BY created_at DESC'
            ) as cursor:
                rows = await cursor.fetchall()
                return rows