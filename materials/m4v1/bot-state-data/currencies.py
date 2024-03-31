import requests
from decimal import Decimal

JPY_RUB = 0.606


ERROR_FETCHING_VALUE = -1
ERROR_CURRENCY_NOT_FOUND = -2
ERROR_CURRENCY_INVALID = -3

CURRENCIES_API_URL = (
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api"
    "@latest/v1/currencies/{currency}.json"
)

ALL_CURRENCIES_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.min.json"


def fetch_available_currencies():
    response = requests.get(ALL_CURRENCIES_URL)
    if response.status_code != 200:
        return {}
    return response.json()


def is_currency_available(currency: str) -> bool:
    return currency.lower() in fetch_available_currencies()


def get_currency_ratio(from_currency, to_currency):
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()
    url = CURRENCIES_API_URL.format(currency=from_currency)
    response = requests.get(url)
    if response.status_code != 200:
        if response.status_code == 404:
            return ERROR_CURRENCY_NOT_FOUND
        return ERROR_FETCHING_VALUE

    json_data = response.json(parse_float=Decimal)
    values = json_data[from_currency]
    if to_currency not in values:
        return ERROR_CURRENCY_INVALID
    return values[to_currency]


def get_jpy_to_rub_ratio():
    return get_currency_ratio(
        from_currency="JPY",
        to_currency="RUB",
    )


def get_currencies_names(currency: str, default_to: str = "RUB"):
    if " " in currency:
        currency_from, _, currency_to = currency.partition(" ")
        currency_from = currency_from.strip()
        currency_to = currency_to.strip()
    else:
        currency_from = currency
        currency_to = default_to

    return currency_from, currency_to
