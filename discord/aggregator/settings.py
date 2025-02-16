import logging
import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


def setup_app_logging():
    logger = logging.getLogger("discord-aggregator")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

APP_LOGGER = setup_app_logging()

load_dotenv()

# == App Settings == #
DEV = os.getenv("DEV", "false").lower() == "true"
if DEV:
    APP_LOGGER.info("Running in development mode!")

TIMEZONE = ZoneInfo("America/New_York")

VERSION = "2.1.5"

# == Bot Settings == #
BOT_PREFIXES = ["="]

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    msg = "No `BOT_TOKEN` environment variable provided!"
    raise KeyError(msg)

DISCORD_OWNER_ID = int(os.getenv("DISCORD_OWNER_ID")) if "DISCORD_OWNER_ID" in os.environ else None
TESTING_GUILD_ID = int(os.getenv("TESTING_GUILD_ID")) if "TESTING_GUILD_ID" in os.environ else None
TESTING_ADMIN_CHANNEL_ID = (
    int(os.getenv("TESTING_ADMIN_CHANNEL_ID"))
    if "TESTING_ADMIN_CHANNEL_ID" in os.environ
    else None
)

# construct url for database
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_PATH = os.getenv("DATABASE_PATH", "/database.db")
DATABASE_DRIVER = os.getenv("DATABASE_DRIVER", "aiosqlite")

DATABASE_URL = f"{DATABASE_TYPE}+{DATABASE_DRIVER}://{DATABASE_PATH}"

# == Extensions == #
ENABLED_EXTENSIONS = ["ext.utils", "ext.transformer"]
if DEV:
    ENABLED_EXTENSIONS.append("ext.development")

EXTENSION_SETTINGS: dict = {}

if "ext.transformer" in ENABLED_EXTENSIONS:
    EXTENSION_SETTINGS["transformer"] = {
        "valid_guilds": [1340196940310384660],
        "target_channel_id": int(os.getenv("TRANSFORMER_TARGET_CHANNEL_ID")),
        "llm_api_key": os.getenv("OPEN_AI_API_KEY"),
        "transformer_url": os.getenv("TRANSFORMER_URL"),
        "transformer_api_key": os.getenv("TRANSFORMER_API_KEY"),
    }
