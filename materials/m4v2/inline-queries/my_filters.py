from typing import Iterable

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


class HasEntitiesFilter(SimpleCustomFilter):
    key = "has_entities"

    def check(self, message: Message) -> bool:
        return bool(message.entities)


class ContainsWordFilter(AdvancedCustomFilter):
    key = "contains_word"

    def check(self, message: Message, word: str) -> bool:
        text = message.text or message.caption
        if not text:
            return False

        return word in text.lower()


class ContainsOneOfWordsFilter(AdvancedCustomFilter):
    key = "contains_one_of_words"

    def check(self, message: Message, words: Iterable[str]) -> bool:
        text = message.text or message.caption
        if not text:
            return False

        text_lower = text.lower()
        # for word in words:
        #     if word.lower() in text_lower:
        #         return True
        # return False
        return any(word.lower() in text_lower for word in words)
