from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "начало работы"),
    BotCommand("help", "помощь"),
    BotCommand("joke", "случайная штука"),
    BotCommand("joke2", "шутка с каламбуром"),
    BotCommand("jpy_to_rub", "перевести JPY в RUB"),
    BotCommand("cvt", "конвертировать"),
    BotCommand(
        "set_my_currency",
        "установить целевую валюту",
    ),
    BotCommand(
        "set_local_currency",
        "установить локальную валюту",
    ),
]
