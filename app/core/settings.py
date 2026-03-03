from __future__ import annotations

from dataclasses import dataclass
import os


def _parse_csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def _get_env(name: str, default: str | None = None, *, required: bool = False) -> str:
    val = os.getenv(name, default)
    if required and (val is None or val.strip() == ""):
        raise ValueError(f"Missing required environment variable: {name}")
    return val if val is not None else ""


@dataclass(frozen=True)
class Settings:
    app_env: str
    db_path: str
    watchlist: list[str]
    news_lookback_hours: int
    reddit_lookback_hours: int


def load_settings() -> Settings:
    app_env = _get_env("APP_ENV", "dev")
    db_path = _get_env("DB_PATH", "./data/app.db")
    watchlist = _parse_csv(_get_env("WATCHLIST", "EURUSD,XAUUSD"))

    news_hours = int(_get_env("NEWS_LOOKBACK_HOURS", "48"))
    reddit_hours = int(_get_env("REDDIT_LOOKBACK_HOURS", "48"))

    if news_hours <= 0:
        raise ValueError("NEWS_LOOKBACK_HOURS must be > 0")
    if reddit_hours <= 0:
        raise ValueError("REDDIT_LOOKBACK_HOURS must be > 0")

    return Settings(
        app_env=app_env,
        db_path=db_path,
        watchlist=watchlist,
        news_lookback_hours=news_hours,
        reddit_lookback_hours=reddit_hours,
    )
    
