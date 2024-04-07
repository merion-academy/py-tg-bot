from telebot import types, TeleBot, util, formatting

import currencies
import messages


def send_convert_jpy_to_rub(message: types.Message, bot: TeleBot):
    arguments = util.extract_arguments(message.text)
    if not arguments:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.cvt_jpy_to_rub_how_to,
            parse_mode="HTML",
        )
        return

    if not arguments.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                messages.invalid_argument_text,
                formatting.hcode(arguments),
                separator=" ",
            ),
            messages.cvt_jpy_to_rub_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML",
        )
        return

    jpy_amount = int(arguments)
    ratio = currencies.get_jpy_to_rub_ratio()
    rub_amount = jpy_amount * ratio

    bot.send_message(
        chat_id=message.chat.id,
        text=messages.format_jpy_to_rub_message(
            jpy_amount=jpy_amount,
            rub_amount=rub_amount,
        ),
        parse_mode="HTML",
    )
