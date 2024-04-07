from telebot import types, TeleBot

import currencies
import messages
from .selected_currency_helper import set_selected_currency


def handle_set_my_currency(message: types.Message, bot: TeleBot):
    set_selected_currency(
        bot=bot,
        message=message,
        data_key=currencies.default_currency_key,
        set_currency_success_message=messages.set_my_currency_success_message_text,
    )


def set_local_currency_handle_not_private_chat(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_local_currency_only_in_private_chat,
    )


def no_arg_to_set_local_currency(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_local_currency_help_message,
        parse_mode="HTML",
    )


def set_local_currency(message: types.Message, bot: TeleBot):
    set_selected_currency(
        bot=bot,
        message=message,
        data_key=currencies.local_currency_key,
        set_currency_success_message=messages.set_local_currency_success_message,
    )


def answer_no_args_to_set_my_currency(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_my_currency_help_message_text,
        parse_mode="HTML",
    )
