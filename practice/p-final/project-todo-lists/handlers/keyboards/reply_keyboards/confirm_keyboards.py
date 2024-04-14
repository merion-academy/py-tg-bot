from telebot.types import ReplyKeyboardMarkup


def create_yes_or_no_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Да", "Нет")
    return kb


def create_confirm_or_cancel_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Да", "Нет")
    kb.add("Отмена")
    return kb


kb_yes_or_no = create_yes_or_no_keyboard()
kb_confirm_or_cancel = create_confirm_or_cancel_keyboard()
