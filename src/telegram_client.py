import telebot

from telebot import apihelper
from telebot.types import BotCommand

from config import (
    BOT_TOKEN,
    PROXY_URL,
)


if PROXY_URL:
    apihelper.proxy = {
        "http": PROXY_URL,
        "https": PROXY_URL,
    }


bot = telebot.TeleBot(
    BOT_TOKEN
)


def send_message(
    chat_id,
    text,
):
    try:
        bot.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
        )

        return True

    except Exception as error:
        print(
            f"Ошибка отправки в ТГ "
            f"для {chat_id}: {error}",
            flush=True,
        )

        return False


def set_bot_commands():
    try:
        bot.set_my_commands([
            BotCommand(
                "stop",
                "Отключить сирену",
            ),
            BotCommand(
                "info",
                "Проверить статус бота",
            ),
        ])

        print(
            "Команды Telegram успешно установлены.",
            flush=True,
        )

    except Exception as error:
        print(
            "Не удалось установить "
            "команды бота: "
            f"{error}",
            flush=True,
        )