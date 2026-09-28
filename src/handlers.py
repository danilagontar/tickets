from config import CHAT_IDS
from telegram_client import (
    bot,
    send_message,
)


def register_handlers(
    alarm_manager,
):
    @bot.message_handler(
        commands=["stop"]
    )
    def stop_alarm(message):
        user_chat_id = str(
            message.chat.id
        )

        if user_chat_id not in CHAT_IDS:
            return

        stopped = alarm_manager.stop(
            user_chat_id
        )

        if stopped:
            send_message(
                user_chat_id,
                "✅ Понял! "
                "Сирена отключена.",
            )

            print(
                "Сирена отключена для "
                f"пользователя "
                f"{message.from_user.first_name}.",
                flush=True,
            )

        else:
            send_message(
                user_chat_id,
                "Сирена для тебя "
                "и так выключена.",
            )

    @bot.message_handler(
        commands=["info"]
    )
    def send_info(message):
        user_chat_id = str(
            message.chat.id
        )

        if user_chat_id not in CHAT_IDS:
            return

        send_message(
            user_chat_id,
            "✅ Бот работает штатно. "
            "Мониторинг билетов активен "
            "в фоновом режиме!",
        )