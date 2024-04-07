from telebot import (
    types,
    TeleBot,
)

import messages


def answer_start_command(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        messages.start_text,
        parse_mode="HTML",
    )


def answer_help_command(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        messages.help_text,
    )


def register_basic_commands_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=answer_start_command,
        commands=["start"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=answer_help_command,
        commands=["help"],
        pass_bot=True,
    )
