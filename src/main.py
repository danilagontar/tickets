import threading
import time

from alarm import AlarmManager
from handlers import register_handlers
from monitor import monitor_tickets
from telegram_client import (
    bot,
    set_bot_commands,
)


POLLING_RESTART_DELAY = 10


def polling_loop():
    while True:
        try:
            print(
                "Подключение к Telegram...",
                flush=True,
            )

            bot.polling(
                none_stop=True,
                timeout=30,
                long_polling_timeout=30,
            )

        except KeyboardInterrupt:
            print(
                "Бот остановлен.",
                flush=True,
            )

            break

        except Exception as error:
            print(
                "Ошибка Telegram polling: "
                f"{error}",
                flush=True,
            )

            print(
                "Повторное подключение "
                f"через "
                f"{POLLING_RESTART_DELAY} сек...",
                flush=True,
            )

            time.sleep(
                POLLING_RESTART_DELAY
            )


def main():
    alarm_manager = AlarmManager()

    register_handlers(
        alarm_manager
    )

    set_bot_commands()

    monitor_thread = threading.Thread(
        target=monitor_tickets,
        args=(alarm_manager,),
        daemon=True,
    )

    monitor_thread.start()

    print(
        "Бот запущен. "
        "Ожидание команд...",
        flush=True,
    )

    polling_loop()


if __name__ == "__main__":
    main()