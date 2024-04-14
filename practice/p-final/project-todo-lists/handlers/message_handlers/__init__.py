from telebot import TeleBot

from handlers.message_handlers.commands_handlers import register_commands
from handlers.message_handlers.commands_handlers.todo_commands import (
    register_todo_handlers,
)
from handlers.message_handlers.echo import register_echo_handlers


def register_message_handlers(bot: TeleBot):
    register_commands(bot)
    register_todo_handlers(bot)
    # last line!
    register_echo_handlers(bot)
