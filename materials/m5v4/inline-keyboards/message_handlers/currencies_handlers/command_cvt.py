from telebot import (
    types,
    TeleBot,
    util,
    formatting,
)

import currencies
import messages
from currencies import default_currency_key
from custom_filters.common_filters import has_no_command_arguments


def handle_cvt_currency_no_arguments(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.cvt_how_to,
        parse_mode="HTML",
    )


def handle_cvt_currency(message: types.Message, bot: TeleBot):
    arguments = util.extract_arguments(message.text)
    amount, _, currency = arguments.partition(" ")

    if not amount.isdigit():
        error_text = formatting.format_text(
            messages.invalid_argument_text,
            formatting.hcode(arguments),
            messages.cvt_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=error_text,
            parse_mode="HTML",
        )
        return

    currency = currency.strip()
    default_currency = "RUB"

    user_data = bot.current_states.get_data(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    if user_data and default_currency_key in user_data:
        default_currency = user_data[default_currency_key]

    currency_from, currency_to = currencies.get_currencies_names(
        currency=currency,
        default_to=default_currency,
    )
    ratio = currencies.get_currency_ratio(
        from_currency=currency_from,
        to_currency=currency_to,
    )
    if ratio == currencies.ERROR_FETCHING_VALUE:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_fetching_currencies_text,
        )
        return
    if ratio in {
        currencies.ERROR_CURRENCY_NOT_FOUND,
        currencies.ERROR_CURRENCY_INVALID,
    }:
        bad_currency = currency_from
        if ratio == currencies.ERROR_CURRENCY_INVALID:
            bad_currency = currency_to
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_no_such_currency.format(
                currency=formatting.hcode(bad_currency),
            ),
            parse_mode="HTML",
        )
        return

    from_amount = int(amount)
    result_amount = from_amount * ratio
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.format_currency_convert_message(
            from_currency=currency_from,
            to_currency=currency_to,
            from_amount=from_amount,
            to_amount=result_amount,
        ),
        parse_mode="HTML",
    )


def register_command_cvt_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_cvt_currency_no_arguments,
        commands=["cvt"],
        func=has_no_command_arguments,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_cvt_currency,
        commands=["cvt"],
        pass_bot=True,
    )
