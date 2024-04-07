from telebot import (
    TeleBot,
    custom_filters,
)

from custom_filters.my_filters import UpdatedTextFilter
from message_handlers.message_talk import (
    handle_weather_request,
    handle_photo_with_cat_caption,
    handle_photo,
    handle_hi_message_text,
    handle_reply_message,
    reply_whats_up,
    reply_bye,
)


def register_regular_messages_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_weather_request,
        text=UpdatedTextFilter(
            contains=["погода"],
            ignore_case=True,
        ),
        pass_bot=True,
    )

    bot.register_message_handler(
        callback=handle_photo_with_cat_caption,
        content_types=["photo"],
        contains_word="кот",
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_photo,
        content_types=["photo"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_hi_message_text,
        contains_word="привет",
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_reply_message,
        is_reply=True,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=reply_whats_up,
        contains_word="как дела",
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=reply_bye,
        contains_one_of_words=["пока", "до свидания"],
        pass_bot=True,
    )
