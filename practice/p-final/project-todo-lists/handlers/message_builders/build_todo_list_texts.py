from telebot import types

from handlers.keyboards.inline_keyboards.todo_list_actions import (
    create_items_list_actions_kb,
)
from messages import TextTodo
from todo_storage.types import ToDoList


def prepare_todo_list_parts(
    todo_list: ToDoList,
    flag_confirm_delete_todo_id: str | None = None,
) -> tuple[str, types.InlineKeyboardMarkup]:
    text = TextTodo.todos_list_text(todo_list=todo_list)
    kb = create_items_list_actions_kb(
        todo_list=todo_list,
        flag_confirm_delete_todo_id=flag_confirm_delete_todo_id,
    )
    return text, kb
