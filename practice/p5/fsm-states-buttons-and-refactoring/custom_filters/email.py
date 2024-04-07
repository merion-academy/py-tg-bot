from telebot import types


def is_valid_email(text: str) -> bool:
    return "@" in text and "." in text


def is_valid_email_message_text(message: types.Message) -> bool:
    return message.text and is_valid_email(message.text)
