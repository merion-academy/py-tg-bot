from telebot import types


def get_yes_or_no_kb():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    keyboard.add("Да", "Нет")
    return keyboard


def get_cancel_keyboard():
    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    kb.add("Отмена")
    return kb


yes_or_no_kb = get_yes_or_no_kb()
cancel_kb = get_cancel_keyboard()
