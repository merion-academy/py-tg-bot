import random

from telebot import (
    types,
    TeleBot,
)

import messages


def command_random_handler(message: types.Message, bot: TeleBot):
    keyboard = types.InlineKeyboardMarkup()
    random_org_site_button = types.InlineKeyboardButton(
        text="random org",
        url="https://random.org",
    )
    ya_ru_site_button = types.InlineKeyboardButton(
        text="yandex",
        url="https://ya.ru",
    )
    # keyboard.add(random_org_site_button)
    # keyboard.add(ya_ru_site_button)
    keyboard.row(random_org_site_button, ya_ru_site_button)
    random_int = random.randint(10, 500)
    convert_random_amount_button = types.InlineKeyboardButton(
        text=f"Convert {random_int}",
        # switch_inline_query=str(random_int),
        switch_inline_query_current_chat=str(random_int),
    )
    convert_random_jpy_amount_button = types.InlineKeyboardButton(
        text=f"Convert {random_int} JPY",
        # switch_inline_query=str(random_int),
        switch_inline_query_current_chat=f"{random_int} JPY",
    )
    keyboard.add(convert_random_amount_button)
    keyboard.add(convert_random_jpy_amount_button)

    random_num = random.randint(10, 100)
    random_number_button = types.InlineKeyboardButton(
        text=f"Number {random_num}", callback_data=f"random-num:{random_num}"
    )
    keyboard.add(random_number_button)

    another_random_number = random.randint(50, 200)
    hidden_random_number_button = types.InlineKeyboardButton(
        text=f"Hidden number (click)",
        callback_data=f"hidden-random-num:{another_random_number}",
    )

    keyboard.add(hidden_random_number_button)
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.random_message_text,
        reply_markup=keyboard,
    )


def register_command_random_handler(bot: TeleBot):
    bot.register_message_handler(
        callback=command_random_handler,
        commands=["random"],
        pass_bot=True,
    )
