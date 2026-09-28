import threading


class AlarmManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._active_chats = set()
        self._message = ""

    def activate(
        self,
        chat_ids,
        message,
    ):
        with self._lock:
            self._message = message

            for chat_id in chat_ids:
                self._active_chats.add(
                    str(chat_id)
                )

    def stop(self, chat_id):
        chat_id = str(chat_id)

        with self._lock:
            if chat_id not in self._active_chats:
                return False

            self._active_chats.remove(
                chat_id
            )

            return True

    def get_active_chats(self):
        with self._lock:
            return list(
                self._active_chats
            )

    def get_message(self):
        with self._lock:
            return self._message