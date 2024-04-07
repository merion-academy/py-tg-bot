from telebot import types, util, formatting, TeleBot

import currencies
import messages


def set_selected_currency(
    bot: TeleBot,
    message: types.Message,
    data_key: str,
    set_currency_success_message: str,
):
    currency = util.extract_arguments(message.text) or ""
    if not currencies.is_currency_available(currency):
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_no_such_currency.format(
                currency=formatting.hcode(currency),
            ),
            parse_mode="HTML",
        )
        return

    if (
        bot.get_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        )
        is None
    ):
        bot.set_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            state=0,
        )

    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        **{data_key: currency},
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=set_currency_success_message.format(
            currency=formatting.hcode(currency.upper()),
        ),
        parse_mode="HTML",
    )
