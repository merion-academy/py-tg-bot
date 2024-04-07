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
