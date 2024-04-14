from telebot import types, util


def has_no_command_arguments(message: types.Message):
    return not util.extract_arguments(message.text)


def current_chat_is_not_user_chat(message: types.Message):
    return message.chat.id != message.from_user.id
