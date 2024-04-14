from telebot import TeleBot

from handlers.message_handlers import register_message_handlers
from handlers.callback_handlers import register_callback_handlers


def register_handlers(bot: TeleBot):
    register_message_handlers(bot)
    register_callback_handlers(bot)
