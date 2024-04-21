from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DjangoConfig:
    key: str
    debug: bool
    db_url: str
    superuser_password: str
    superuser_email: str


@dataclass
class PostgreSqlConfig:
    db: str
    host: str
    pas: str
    port: int
    user: str
    driver: str


@dataclass
class EmailConfig:
    user: str
    pas: str


@dataclass
class Config:
    django: DjangoConfig
    pgdb: PostgreSqlConfig
    email: EmailConfig


def load_config(path: Optional[str]) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        django=DjangoConfig(
            key=env.str("SECRET_KEY"),
            debug=env.bool("DEBUG", True),
            db_url=env.str("PRIMARY_DATABASE_URL"),
            superuser_password=env.str("DJANGO_SUPERUSER_PASSWORD"),
            superuser_email=env.str("DJANGO_SUPERUSER_EMAIL"),
        ),
        pgdb=PostgreSqlConfig(
            db=env.str("DB_NAME"),
            host=env.str("DB_HOST"),
            user=env.str("DB_USER"),
            pas=env.str("DB_PASS"),
            port=env.int("DB_PORT"),
            driver=env.str("DB_DRIVERNAME"),
        ),
        email=EmailConfig(
            user=env.str("EMAIL_USER"),
            pas=env.str("EMAIL_PASSWORD"),
        ),
    )
