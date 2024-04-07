from telebot import types
from telebot.types import InlineQuery

import currencies


def is_query_only_digits(query: types.InlineQuery):
    # return query.query.isdigit()
    if query and query.query:
        return query.query.isdigit()
    return False


def is_query_amount_and_available_currency(query: InlineQuery):
    text = query.query or ""
    amount, _, currency = text.partition(" ")
    if not amount.isdigit():
        return False

    return currencies.is_currency_available(currency)


def is_query_amount_and_available_currencies_from_and_to(query: InlineQuery):
    text = query.query or ""
    amount, _, currencies_from_and_to = text.partition(" ")
    if not amount.isdigit():
        return False

    from_currency, _, to_currency = currencies_from_and_to.partition(" ")
    if not currencies.is_currency_available(from_currency):
        return False
    if not currencies.is_currency_available(to_currency):
        return False
    return True


def any_query(query: types.InlineQuery):
    print(query)
    return True
