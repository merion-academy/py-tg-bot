from telebot import TeleBot

from .select_current_todo_list import register_select_current_list_callback
from .select_todo_list import register_select_current_list_for_new_todo_callback
from .todo_actions import register_todo_actions


def register_callback_handlers(bot: TeleBot):
    register_todo_actions(bot)
    register_select_current_list_for_new_todo_callback(bot)
    register_select_current_list_callback(bot)
