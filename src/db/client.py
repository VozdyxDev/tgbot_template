import asyncio

import asyncpg

from ..config import DBConfig


class Client:

    def __init__(self, bot, config: DBConfig,
                 loop: asyncio.AbstractEventLoop | asyncio.ProactorEventLoop | None = None) -> None:
        self.bot = bot
        self.cfg = config
        self.loop = loop or asyncio.get_event_loop()
        self._conn = self._get_connection()
        self.load_tables()

    async def _create_database(self, **kwargs):
        user = kwargs.get("user")
        conn = await self._connect(database='postgres', **kwargs)
        await conn.execute(f'CREATE DATABASE "{user}" OWNER "{user}"')
        await conn.close()

    async def _connect(self, **kwargs) -> asyncpg.Pool:
        try:
            return await asyncpg.create_pool(**kwargs)
        except asyncpg.InvalidCatalogNameError:
            await self._create_database(**kwargs)
            return await asyncpg.create_pool(**kwargs)

    def _get_connection(self) -> asyncpg.Pool:
        return self.loop.run_until_complete(
            self._connect(host=self.cfg.host, port=self.cfg.port, user=self.cfg.user, password=self.cfg.password))

    async def execute(self, query: str, *args) -> str:
        return await self._conn.execute(query, *args)

    def load_tables(self):
        with open('database/tables.sql', 'r', encoding='utf8') as fp:
            self.loop.run_until_complete(self.execute(fp.read()))
