from telebot import TeleBot

from .basic_commands import register_basic_commands


def register_commands(bot: TeleBot):
    register_basic_commands(bot)
