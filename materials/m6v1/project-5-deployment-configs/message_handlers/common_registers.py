from typing import Callable

from telebot import TeleBot

from custom_filters.my_filters import UpdatedTextFilter


def register_cancel_handlers(
    bot: TeleBot,
    handler: Callable,
    states: list,
):
    bot.register_message_handler(
        callback=handler,
        commands=["cancel"],
        state=states,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handler,
        text=UpdatedTextFilter(
            equals="отмена",
            ignore_case=True,
        ),
        state=states,
        pass_bot=True,
    )
