from telebot import State
from telebot.handler_backends import StatesGroup


class AddTodoStates(StatesGroup):
    choose_list_or_add_to_current = State()
    add_todo_list = State()


class ToDoListActionStates(StatesGroup):
    delete_todo_list = State()
