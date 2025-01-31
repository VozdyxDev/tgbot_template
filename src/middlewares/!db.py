from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from ..services.repository import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        db = await self.pool.acquire()
        data["db"] = db
        data["repo"] = Repo(db)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        if db := data.get("db"):
            # check the documentation of your pool implementation
            # for proper way of releasing connection
            await self.pool.release(db)

def setup(dp):
    dp.add_mw(DbMiddleware)
