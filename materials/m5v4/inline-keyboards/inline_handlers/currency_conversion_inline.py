from telebot import (
    types,
    TeleBot,
)
from telebot.types import InlineQuery

import currencies
import messages
from currencies import local_currency_key


def handle_any_convert_to_many_inline_query(
    bot: TeleBot,
    query: types.InlineQuery,
    amount: int,
    from_currency: str,
    target_currencies: list[str],
):
    ratios = currencies.get_currencies_ratios(
        from_currency=from_currency,
        to_currencies=target_currencies,
    )

    results = []

    for currency_rate, currency_name in zip(
        ratios,
        target_currencies,
    ):
        total_amount = amount * currency_rate
        result = messages.format_content_to_result_article(
            from_currency=from_currency,
            to_currency=currency_name,
            amount=amount,
            total_amount=total_amount,
        )
        results.append(result)

    bot.answer_inline_query(
        inline_query_id=query.id,
        results=results,
        cache_time=10,
    )


def handle_convert_inline_query(query: types.InlineQuery, bot: TeleBot):
    amount = int(query.query)

    target_currencies = currencies.FAVOURITE_CURRENCIES
    from_currency = currencies.DEFAULT_LOCAL_CURRENCY
    user_data = bot.current_states.get_data(
        user_id=query.from_user.id,
        chat_id=query.from_user.id,
    )
    if user_data and local_currency_key in user_data:
        from_currency = user_data[local_currency_key]

    handle_any_convert_to_many_inline_query(
        bot=bot,
        query=query,
        amount=amount,
        from_currency=from_currency,
        target_currencies=target_currencies,
    )


def handle_convert_query_with_selected_currency(query: InlineQuery, bot: TeleBot):
    amount_str, _, currency = query.query.partition(" ")
    amount = int(amount_str)
    target_currencies = currencies.FAVOURITE_CURRENCIES

    handle_any_convert_to_many_inline_query(
        bot=bot,
        query=query,
        amount=amount,
        from_currency=currency,
        target_currencies=target_currencies,
    )


def handle_convert_query_with_selected_currency_and_target_currency(query: InlineQuery, bot: TeleBot):
    amount_str, from_currency, to_currency = query.query.split(" ", maxsplit=2)
    amount = int(amount_str)
    target_currencies = [to_currency]

    handle_any_convert_to_many_inline_query(
        bot=bot,
        query=query,
        amount=amount,
        from_currency=from_currency,
        target_currencies=target_currencies,
    )
