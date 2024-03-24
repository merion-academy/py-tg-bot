import requests
from decimal import Decimal

JPY_RUB = 0.606


ERROR_FETCHING_VALUE = -1
ERROR_CURRENCY_NOT_FOUND = -2

CURRENCIES_API_URL = (
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api"
    "@latest/v1/currencies/{currency}.json"
)


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
    return json_data[from_currency][to_currency]


def get_jpy_to_rub_ratio():
    return get_currency_ratio(
        from_currency="JPY",
        to_currency="RUB",
    )
