from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "начало работы"),
    BotCommand("help", "помощь"),
    BotCommand("joke", "случайная штука"),
    BotCommand("joke2", "случайная штука (из двух частей)"),
    BotCommand("jpy_to_rub", "конвертировать JPY в RUB"),
    BotCommand("cvt", "конвертировать валюту"),
    BotCommand("set_my_currency", "установить целевую валюту для конвертации"),
    BotCommand("set_local_currency", "установить локальную валюту для конвертации"),
]
