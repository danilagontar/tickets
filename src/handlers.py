from datetime import datetime

from config import CHAT_IDS
from monitor_state import get_status
from telegram_client import (
    bot,
    send_message,
)
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def register_handlers(
    alarm_manager,
):
    @bot.message_handler(
        commands=["menu"]
    )
    def show_menu(message):
        user_chat_id = str(
            message.chat.id
        )

        if user_chat_id not in CHAT_IDS:
            return

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton(
                "ℹ️ Информация",
                callback_data="menu_info",
            )
        )

        bot.send_message(
            user_chat_id,
            "🖥 ГЛАВНОЕ МЕНЮ",
            reply_markup=keyboard,
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "menu_info"
    )
    def menu_info(call):
        user_chat_id = str(
            call.message.chat.id
        )

        if user_chat_id not in CHAT_IDS:
            return

        status = get_status()

        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton(
                "ℹ️ Обновить",
                callback_data="menu_info",
            )
        )

        if status["last_check"] is None:
            last_check_text = (
                "ещё не выполнялась"
            )
        else:
            last_check_text = (
                status["last_check"]
                .strftime("%H:%M:%S")
            )

        if status["last_success"] is None:
            last_success_text = (
                "ещё не было"
            )
        else:
            last_success_text = (
                status["last_success"]
                .strftime("%H:%M:%S")
            )

        if status["last_error"]:
            monitor_status = (
                "🔴 ошибка"
            )

            error_text = (
                "\n\n"
                "❌ Последняя ошибка:\n"
                f"{status['last_error']}"
            )
        else:
            monitor_status = (
                "🟢 работает"
            )

            error_text = ""

        text = (
            "🖥 СТАТУС БОТА\n\n"
            "🟢 Telegram: работает\n"
            f"{monitor_status} "
            "Мониторинг билетов\n"
            f"🔄 Последняя попытка: "
            f"{last_check_text}\n"
            f"✅ Последняя успешная проверка: "
            f"{last_success_text}"
            f"{error_text}"
        )

        bot.answer_callback_query(
            call.id
        )

        bot.edit_message_text(
            text,
            chat_id=user_chat_id,
            message_id=call.message.message_id,
            reply_markup=keyboard,
        )

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
                "✅ Понял Лерусь! "
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
                "выключена, любимка",
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