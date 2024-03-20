from telebot.types import Message
from telebot.custom_filters import (
    SimpleCustomFilter,
    AdvancedCustomFilter,
)

import config


class IsUserAdminOfBot(SimpleCustomFilter):
    key = "is_bot_admin"

    def check(self, message: Message):
        return message.from_user.id in config.BOT_ADMIN_USER_IDS


class ContainsWordFilter(AdvancedCustomFilter):
    key = "contains_word"

    def check(self, message: Message, word: str) -> bool:
        text = message.text or message.caption
        if not text:
            return False

        return word in text.lower()
