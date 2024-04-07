from telebot import (
    types,
    TeleBot,
    custom_filters,
)

from custom_filters.my_filters import UpdatedTextFilter


def random_num_callback(query: types.CallbackQuery, bot: TeleBot):
    prefix, _, number = query.data.partition(":")
    text = f"число: {number}"
    bot.answer_callback_query(
        callback_query_id=query.id,
        text=text,
        cache_time=5,
    )


def hidden_random_num_callback(query: types.CallbackQuery, bot: TeleBot):
    prefix, _, number = query.data.partition(":")
    text = f"число: {number}"
    bot.answer_callback_query(
        callback_query_id=query.id,
        text=text,
        cache_time=5,
        show_alert=True,
    )


def register_random_number_callback_query_handlers(bot: TeleBot):
    bot.register_callback_query_handler(
        callback=random_num_callback,
        func=None,
        text=UpdatedTextFilter(starts_with="random-num:"),
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        callback=hidden_random_num_callback,
        func=None,
        text=UpdatedTextFilter(starts_with="hidden-random-num:"),
        pass_bot=True,
    )
