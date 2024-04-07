from telebot import (
    types,
    TeleBot,
)


def send_echo_message(message: types.Message, bot: TeleBot):
    text = message.text
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        entities=message.entities,
    )


def handle_sticker(message: types.Message, bot: TeleBot):
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=message.sticker.file_id,
        reply_to_message_id=message.id,
    )
