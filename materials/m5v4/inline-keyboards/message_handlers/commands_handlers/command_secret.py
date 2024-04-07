from telebot import types, TeleBot

import messages


def handle_admin_secret(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        text=messages.secret_message_for_admin,
    )


def handle_not_admin_request_secret(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        text=messages.secret_message_not_admin,
    )


def register_command_secret_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_admin_secret,
        commands=["secret"],
        is_bot_admin=True,
        pass_bot=True,
    )

    bot.register_message_handler(
        callback=handle_not_admin_request_secret,
        commands=["secret"],
        is_bot_admin=False,
        pass_bot=True,
    )
