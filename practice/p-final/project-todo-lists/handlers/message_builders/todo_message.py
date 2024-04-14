from telebot import types, formatting

from handlers.keyboards.inline_keyboards.todo_lists import (
    create_select_list_kb,
)
from messages import TextTodo
from todo_storage.types import ToDoList


def todo_message_parts(
    callback_prefix,
    current_list: ToDoList,
    todo_lists: list[ToDoList],
    text_template: str = TextTodo.choose_list,
) -> tuple[str, types.InlineKeyboardMarkup]:
    kb = create_select_list_kb(
        callback_prefix=callback_prefix,
        todo_lists=todo_lists,
        selected_list_id=current_list.id,
    )
    text = text_template.format(
        list_name=formatting.hbold(current_list.name),
    )
    return text, kb
