from telebot import TeleBot

from callback_handlers.random_numbers import (
    register_random_number_callback_query_handlers,
)


def register_callback_query_handlers(bot: TeleBot):
    register_random_number_callback_query_handlers(bot)
