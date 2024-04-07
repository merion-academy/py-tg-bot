from telebot import (
    types,
    TeleBot,
)

import config


def send_cat_photo_as_file(message: types.Message, bot: TeleBot):
    bot.send_document(
        chat_id=message.chat.id,
        document=config.CAT_PIC_URL,
    )


def send_cat_photo(message: types.Message, bot: TeleBot):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=config.CAT_PIC_URL,
        reply_to_message_id=message.id,
    )


def register_cat_commands_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=send_cat_photo_as_file,
        commands=["cat_file"],
        pass_bot=True

    )
    bot.register_message_handler(
        callback=send_cat_photo,
        commands=["cat"],
        pass_bot=True

    )
