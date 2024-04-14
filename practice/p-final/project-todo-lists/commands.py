from telebot.types import BotCommand

default_commands = [
    BotCommand("start", "начало работы"),
    BotCommand("help", "помощь"),
    BotCommand("todo", "добавить задачу"),
    BotCommand("todos", "список задач"),
    BotCommand("lists", "список списков задач"),
    BotCommand("add_list", "добавить список задач"),
    BotCommand("rename_list", "переименовать текущий список задач"),
    BotCommand("delete_list", "удалить текущий список задач"),
]
