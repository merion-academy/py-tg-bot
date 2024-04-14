from telebot import TeleBot, types

import messages


def handle_start_command(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.start_message,
    )


def handle_help_command(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.help_message,
    )


def register_basic_commands(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_start_command,
        commands=["start"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_help_command,
        commands=["help"],
        pass_bot=True,
    )
