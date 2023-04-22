import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes", "y")


def load_config(path: str):
    config_ = configparser.ConfigParser()
    config_.read(path)

    tg_bot = config_["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
        ),
        db=DbConfig(**config_["db"]),
    )


config = load_config("config.ini")
