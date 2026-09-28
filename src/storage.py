import json
import os

from config import (
    DATA_DIR,
    LINKS_FILE,
)


def ensure_data_dir():
    os.makedirs(
        DATA_DIR,
        exist_ok=True,
    )


def load_known_links():
    ensure_data_dir()

    if not os.path.exists(
        LINKS_FILE
    ):
        return set()

    try:
        with open(
            LINKS_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            return set()

        return set(data)

    except Exception as error:
        print(
            f"Ошибка при чтении "
            f"known_links.json: {error}",
            flush=True,
        )

        return set()


def save_known_links(links):
    ensure_data_dir()

    try:
        with open(
            LINKS_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                sorted(links),
                file,
                ensure_ascii=False,
                indent=4,
            )

    except Exception as error:
        print(
            f"Ошибка при сохранении "
            f"known_links.json: {error}",
            flush=True,
        )