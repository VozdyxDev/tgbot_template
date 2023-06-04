import configparser
from aiogram import Bot as abot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from .config import Config
from .db import Client
from .dispatcher import Dispatcher


class Bot(abot):
    config: Config
    db: Client
    dp: Dispatcher

    def __init__(self, *args, **kwargs):
        self.load_config()
        kwargs['token'] = self.config.bot.token
        super().__init__(*args, **kwargs)

        storage = RedisStorage() if self.config.bot.use_redis else MemoryStorage()
        self.dp = Dispatcher(self, storage=storage)

    def load_config(self, path: str = "bot.ini"):
        config = configparser.ConfigParser()
        config.read(path)

        self.config = Config(config)

    def load_database(self):
        self.db = Client(self, self.config.db)
