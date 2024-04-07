from telebot import (
    TeleBot,
)

from custom_filters.inline_filters import (
    is_query_only_digits,
    is_query_amount_and_available_currency,
    is_query_amount_and_available_currencies_from_and_to,
    any_query,
)
from inline_handlers.any_inline_query import handle_any_inline_query
from inline_handlers.currency_conversion_inline import (
    handle_convert_inline_query,
    handle_convert_query_with_selected_currency,
    handle_convert_query_with_selected_currency_and_target_currency,
)


def register_currency_conversion_inline_handlers(bot: TeleBot):
    bot.register_inline_handler(
        callback=handle_convert_inline_query,
        func=is_query_only_digits,
        pass_bot=True,
    )
    bot.register_inline_handler(
        callback=handle_convert_query_with_selected_currency,
        func=is_query_amount_and_available_currency,
        pass_bot=True,
    )
    bot.register_inline_handler(
        callback=handle_convert_query_with_selected_currency_and_target_currency,
        func=is_query_amount_and_available_currencies_from_and_to,
        pass_bot=True,
    )


def register_any_inline_query_handlers(bot: TeleBot):
    bot.register_inline_handler(
        callback=handle_any_inline_query,
        func=any_query,
        pass_bot=True,
    )


def register_inline_handlers(bot: TeleBot):
    register_currency_conversion_inline_handlers(bot)
    register_any_inline_query_handlers(bot)
