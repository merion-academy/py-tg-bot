from telebot import (
    TeleBot,
    types,
)
from message_handlers.commands_handlers.basic_commands import (
    answer_start_command,
    answer_help_command,
)
from message_handlers.commands_handlers.jokes_commands import (
    send_random_joke,
    send_random_two_part_joke,
)


def register_basic_commands_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=answer_start_command,
        commands=["start"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=answer_help_command,
        commands=["help"],
        pass_bot=True,
    )


def register_jokes_commands_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=send_random_joke,
        commands=["joke"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=send_random_two_part_joke,
        commands=["joke2"],
        pass_bot=True,
    )


def register_commands_handlers(bot):
    register_basic_commands_handlers(bot)
    register_jokes_commands_handlers(bot)
