from telebot import types


known_programming_languages = [
    "Python",
    "Go",
    "Java",
    "JavaScript",
]


def get_known_programming_languages_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    for name in known_programming_languages:
        keyboard.add(name)
    return keyboard


def get_final_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            text="Наш сайт",
            url="https://wiki.merionet.ru/merion-academy/",
        )
    )
    return keyboard


known_programming_languages_keyboard = get_known_programming_languages_keyboard()

final_keyboard = get_final_keyboard()
