from telebot import TeleBot

from .command_add_list import register_add_list_commands_handler
from .command_delete_list import register_delete_list_commands_handler
from .command_rename_list import register_rename_list_commands_handler
from .command_todo import register_todo_commands_handler
from .command_todos import register_todos_commands_handler
from .command_lists import register_lists_commands_handler


def register_todo_handlers(bot: TeleBot):
    register_lists_commands_handler(bot)
    register_add_list_commands_handler(bot)
    register_rename_list_commands_handler(bot)
    register_delete_list_commands_handler(bot)
    register_todo_commands_handler(bot)
    register_todos_commands_handler(bot)
