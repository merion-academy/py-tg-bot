from telebot import types, TeleBot

import messages


def send_markdown_message(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.markdown_text,
        parse_mode="MarkdownV2",
    )


def send_html_message(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.html_text,
        parse_mode="HTML",
    )


def register_markdown_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=send_markdown_message,
        commands=["md"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=send_html_message,
        commands=["html"],
        pass_bot=True,
    )
