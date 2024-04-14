from telebot import TeleBot

from handlers.callback_handlers.todo_actions.action_confirm_delete import (
    register_action_confirm_delete_todo,
)
from handlers.callback_handlers.todo_actions.action_delete import (
    register_action_want_to_delete_todo,
)
from handlers.callback_handlers.todo_actions.action_toggle import (
    register_action_toggle_todo,
)


def register_todo_actions(bot: TeleBot):
    register_action_toggle_todo(bot)
    register_action_want_to_delete_todo(bot)
    register_action_confirm_delete_todo(bot)
