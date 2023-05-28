import configparser
from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class BotConfig:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    bot = config["bot"]

    return Config(
        bot=BotConfig(
            token=bot.get("token"),
            admin_id=bot.getint("admin_id"),
            use_redis=bot.getboolean("use_redis"),
        ),
        db=DBConfig(**config["db"]),
    )
