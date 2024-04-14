from telebot import TeleBot, types

from handlers.message_builders.send_current_todo_lists import (
    send_message_show_todo_lists,
)


def handle_command_lists_show_all_lists(
    message: types.Message,
    bot: TeleBot,
):
    send_message_show_todo_lists(message, bot)


def register_lists_commands_handler(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_command_lists_show_all_lists,
        commands=["lists"],
        pass_bot=True,
    )
