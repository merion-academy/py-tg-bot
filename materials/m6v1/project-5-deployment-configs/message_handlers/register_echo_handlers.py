from telebot import (
    TeleBot,
)

from message_handlers.echo import (
    send_echo_message,
    handle_sticker,
)
from message_handlers.echo_entities import (
    echo_and_show_entities,
    echo_and_show_entities_2,
)


def register_echo_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=echo_and_show_entities,
        has_entities=True,
        contains_word="проверка",
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=echo_and_show_entities_2,
        has_entities=True,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_sticker,
        content_types=["sticker"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=send_echo_message,
        content_types=["text"],
        pass_bot=True,
    )
