import requests
from bs4 import BeautifulSoup
import time
import telebot
from telebot import apihelper
from telebot.types import BotCommand
import json
import os
from datetime import datetime
import threading

URL = "https://mediumquality.ru/natalnayakarta"
BOT_TOKEN = "8152169533:AAFQrjkgvrDJ1lo5k-lHYO-TCZmPbEjrhDE"
CHAT_IDS = ["431869701", "789916429"]
LINKS_FILE = "known_links.json"

apihelper.proxy = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080"
}

bot = telebot.TeleBot(BOT_TOKEN)

active_alarms = set()
alarm_message = ""


def load_known_links():
    if os.path.exists(LINKS_FILE):
        try:
            with open(LINKS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return set()
    return set()


def save_known_links(links):
    try:
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(links), f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


def get_intickets_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        all_links = soup.find_all("a", href=True)
        tickets_data = []

        for link in all_links:
            href = link["href"]

            if "intickets.ru" in href:
                try:
                    time_div = link.find("div", class_="t993__btn-text-title")
                    guest_div = link.find("div", class_="t993__btn-text-descr")

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
                except Exception:
                    time_text = "Время не указано"
                    guest_text = "Гость неизвестен"

                tickets_data.append({
                    "url": href,
                    "time": time_text,
                    "guest": guest_text
                })

        return tickets_data

    except Exception as e:
        print(f"Ошибка загрузки страницы: {e}")
        return []


def monitor_tickets():
    global active_alarms, alarm_message

    print("Начинаем мониторинг (поиск каждые 30 сек)...")

    known_links = load_known_links()

    if not known_links:
        print("Первый запуск. Собираем базу текущих билетов...")

        initial_data = get_intickets_data()

        for item in initial_data:
            known_links.add(item["url"])

        save_known_links(known_links)

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        if active_alarms:
            for chat_id in list(active_alarms):
                try:
                    bot.send_message(
                        chat_id,
                        alarm_message,
                        disable_web_page_preview=True
                    )
                except Exception as e:
                    print(
                        f"[{current_time}] Ошибка отправки в ТГ "
                        f"({chat_id}): {e}"
                    )

            print(
                f"[{current_time}] Сирена активна "
                f"для {len(active_alarms)} чел."
            )

            time.sleep(30)
            continue

        current_data = get_intickets_data()
        new_tickets = []

        for item in current_data:
            if item["url"] not in known_links:
                new_tickets.append(item)
                known_links.add(item["url"])

        if new_tickets:
            message = (
                "🚨 Появились новые билеты!\n"
                "БЕГОМ НА https://mediumquality.ru/natalnayakarta\n\n"
            )

            for ticket in new_tickets:
                message += (
                    f"{ticket['time']} {ticket['guest']}: "
                    f"{ticket['url']}\n"
                )

            alarm_message = message

            for chat_id in CHAT_IDS:
                active_alarms.add(str(chat_id))

            save_known_links(known_links)

            print(
                f"[{current_time}] 🚨 Найдены билеты! "
                f"Включена сирена."
            )

            for chat_id in CHAT_IDS:
                try:
                    bot.send_message(
                        chat_id,
                        alarm_message,
                        disable_web_page_preview=True
                    )
                except Exception as e:
                    print(
                        f"[{current_time}] Ошибка отправки в ТГ "
                        f"({chat_id}): {e}"
                    )

        else:
            print(
                f"[{current_time}] Новых билетов не найдено. "
                f"Продолжаем поиск..."
            )

        time.sleep(30)


@bot.message_handler(commands=["stop"])
def stop_alarm(message):
    global active_alarms

    user_chat_id = str(message.chat.id)

    if user_chat_id not in CHAT_IDS:
        return

    if user_chat_id in active_alarms:
        active_alarms.remove(user_chat_id)

        bot.send_message(
            user_chat_id,
            "✅ Понял! Сирена отключена."
        )

        print(
            f"Сирена отключена для пользователя "
            f"{message.from_user.first_name}."
        )
    else:
        bot.send_message(
            user_chat_id,
            "Сирена для тебя и так выключена."
        )


@bot.message_handler(commands=["info"])
def send_info(message):
    user_chat_id = str(message.chat.id)

    if user_chat_id not in CHAT_IDS:
        return

    bot.send_message(
        user_chat_id,
        "✅ Бот работает штатно. Мониторинг билетов активен в фоновом режиме!"
    )


if __name__ == "__main__":
    bot.set_my_commands([
        BotCommand("stop", "Отключить сирену"),
        BotCommand("info", "Проверить статус бота")
    ])

    parser_thread = threading.Thread(
        target=monitor_tickets,
        daemon=True
    )
    parser_thread.start()

    print("Бот запущен. Ожидание команд...")

    bot.polling(none_stop=True)