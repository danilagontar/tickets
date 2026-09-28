import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env",
    )
)


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN is not set"
    )


CHAT_IDS = [
    chat_id.strip()
    for chat_id in os.getenv(
        "CHAT_IDS",
        "",
    ).split(",")
    if chat_id.strip()
]


TARGET_URL = os.getenv(
    "TARGET_URL",
    "https://mediumquality.ru/natalnayakarta",
)

PROXY_URL = os.getenv(
    "PROXY_URL",
    "socks5h://127.0.0.1:1080",
)

POLL_INTERVAL = int(
    os.getenv(
        "POLL_INTERVAL",
        "30",
    )
)

HTTP_TIMEOUT = int(
    os.getenv(
        "HTTP_TIMEOUT",
        "15",
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
)

LINKS_FILE = os.path.join(
    DATA_DIR,
    "known_links.json",
)