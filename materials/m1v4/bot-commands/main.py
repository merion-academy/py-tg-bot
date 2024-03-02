import random

from telebot import TeleBot, types

import config

bot = TeleBot(config.BOT_TOKEN)


help_message = """Привет! Доступные команды:
- /start - начало работы с ботом
- /help - помощь (это сообщение)
- /joke - случайная шутка

Этот бот отправит вам то же сообщение, что и вы ему!
"""

KNOWN_JOKES = [
    "Купил мужик шляпу, а она ему как раз.",
    "Король никогда не ответит матом.",
    "Ученые изобрели кружку для левшей.",
]


@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Привет! Давай знакомиться!",
    )


@bot.message_handler(commands=["help"])
def send_help_message(message: types.Message):
    bot.send_message(
        message.chat.id,
        help_message,
    )


@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        random.choice(KNOWN_JOKES),
    )


@bot.message_handler()
def echo_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'И тебе привет!'
    # if 'как дела' in text.lower():
    #     text = '...'
    bot.send_message(
        message.chat.id,
        text,
    )


bot.infinity_polling(skip_pending=True)
