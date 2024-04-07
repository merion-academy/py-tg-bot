from telebot import TeleBot

from custom_filters.common_filters import (
    has_no_command_arguments,
    current_chat_is_not_user_chat,
)
from message_handlers.currencies_handlers.command_cvt import (
    register_command_cvt_handlers,
)
from message_handlers.currencies_handlers.convert_jpy_to_rub import (
    send_convert_jpy_to_rub,
)
from message_handlers.currencies_handlers.set_currencies_commands import (
    answer_no_args_to_set_my_currency,
    handle_set_my_currency,
    set_local_currency_handle_not_private_chat,
    no_arg_to_set_local_currency,
    set_local_currency,
)


def register_currencies_handlers(bot: TeleBot):
    register_command_cvt_handlers(bot)
    bot.register_message_handler(
        callback=send_convert_jpy_to_rub,
        commands=["jpy_to_rub"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=answer_no_args_to_set_my_currency,
        commands=["set_my_currency"],
        func=has_no_command_arguments,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_set_my_currency,
        commands=["set_my_currency"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=set_local_currency_handle_not_private_chat,
        commands=["set_local_currency"],
        func=current_chat_is_not_user_chat,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=no_arg_to_set_local_currency,
        commands=["set_local_currency"],
        func=has_no_command_arguments,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=set_local_currency,
        commands=["set_local_currency"],
        pass_bot=True,
    )
