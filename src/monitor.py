import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from alarm import AlarmManager
from config import (
    CHAT_IDS,
    HTTP_TIMEOUT,
    POLL_INTERVAL,
    TARGET_URL,
)
from storage import (
    load_known_links,
    save_known_links,
)
from telegram_client import send_message


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def get_intickets_data():
    try:
        response = requests.get(
            TARGET_URL,
            headers=HEADERS,
            timeout=HTTP_TIMEOUT,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        tickets_data = []

        for link in soup.find_all(
            "a",
            href=True,
        ):
            href = link["href"]

            if "intickets.ru" not in href:
                continue

            time_div = link.find(
                "div",
                class_="t993__btn-text-title",
            )

            guest_div = link.find(
                "div",
                class_="t993__btn-text-descr",
            )

            time_text = (
                time_div.get_text(strip=True)
                if time_div
                else "Время не указано"
            )

            guest_text = (
                guest_div.get_text(strip=True)
                if guest_div
                else "Гость неизвестен"
            )

            tickets_data.append({
                "url": href,
                "time": time_text,
                "guest": guest_text,
            })

        return tickets_data

    except Exception as error:
        print(
            f"Ошибка загрузки страницы: "
            f"{error}",
            flush=True,
        )

        return []


def build_alarm_message(
    tickets,
):
    message = (
        "🚨 Появились новые билеты!\n"
        f"БЕГОМ НА {TARGET_URL}\n\n"
    )

    for ticket in tickets:
        message += (
            f"{ticket['time']} "
            f"{ticket['guest']}: "
            f"{ticket['url']}\n"
        )

    return message


def send_active_alarm(
    alarm_manager,
):
    message = alarm_manager.get_message()

    if not message:
        return

    for chat_id in (
        alarm_manager.get_active_chats()
    ):
        send_message(
            chat_id,
            message,
        )


def monitor_tickets(
    alarm_manager,
):
    print(
        "Начинаем мониторинг "
        f"(поиск каждые "
        f"{POLL_INTERVAL} сек)...",
        flush=True,
    )

    known_links = load_known_links()

    if not known_links:
        initial_data = get_intickets_data()

        if initial_data:
            known_links = {
                item["url"]
                for item in initial_data
            }

            save_known_links(
                known_links
            )

            print(
                "Создана база известных "
                "билетов.",
                flush=True,
            )

    while True:
        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        try:
            send_active_alarm(
                alarm_manager
            )

            known_links = load_known_links()

            current_data = (
                get_intickets_data()
            )

            new_tickets = [
                item
                for item in current_data
                if item["url"]
                not in known_links
            ]

            if new_tickets:
                message = build_alarm_message(
                    new_tickets
                )

                alarm_manager.activate(
                    CHAT_IDS,
                    message,
                )

                known_links.update(
                    item["url"]
                    for item in new_tickets
                )

                save_known_links(
                    known_links
                )

                print(
                    f"[{current_time}] "
                    "🚨 Найдены билеты! "
                    "Включена сирена.",
                    flush=True,
                )

                for chat_id in CHAT_IDS:
                    send_message(
                        chat_id,
                        message,
                    )

            else:
                print(
                    f"[{current_time}] "
                    "Новых билетов не найдено. "
                    "Продолжаем поиск...",
                    flush=True,
                )

        except Exception as error:
            print(
                f"[{current_time}] "
                f"Ошибка мониторинга: "
                f"{error}",
                flush=True,
            )

        time.sleep(
            POLL_INTERVAL
        )