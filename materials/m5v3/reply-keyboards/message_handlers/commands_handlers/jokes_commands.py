from telebot import (
    types,
    TeleBot,
    formatting,
)

import jokes


def send_random_joke(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        formatting.hcite(jokes.get_random_joke_text()),
        parse_mode="HTML",
    )


def send_random_two_part_joke(message: types.Message, bot: TeleBot):
    setup, delivery = jokes.get_two_part_joke_texts()

    text = formatting.format_text(
        formatting.escape_html(setup),
        formatting.hspoiler(delivery),
    )
    bot.send_message(
        message.chat.id,
        text=text,
        parse_mode="HTML",
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
