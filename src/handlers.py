from config import CHAT_IDS
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

        bot.answer_callback_query(
            call.id
        )

        bot.edit_message_text(
            "✅ Бот работает штатно. "
            "Мониторинг билетов активен "
            "в фоновом режиме!",
            chat_id=user_chat_id,
            message_id=call.message.message_id,
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