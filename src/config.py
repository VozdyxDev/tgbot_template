from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    port: int


@dataclass
class BotConfig:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig

    def __init__(self, config: ConfigParser):
        bot = config["bot"]
        db = config["db"]
        self.bot = BotConfig(
            token=bot.get("token"),
            admin_id=bot.getint("admin_id"),
            use_redis=bot.getboolean("use_redis")
        )
        self.db = DBConfig(**db)
