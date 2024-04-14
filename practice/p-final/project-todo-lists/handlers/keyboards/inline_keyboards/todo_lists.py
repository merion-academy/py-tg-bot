from enum import Enum, auto

from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from todo_storage.types import ToDoList


class ToDoListActionEnum(Enum):
    select_list_for_new_todo = auto()
    select_current_list = auto()


def create_select_list_kb(
    callback_prefix,
    todo_lists: list[ToDoList],
    selected_list_id: str | None = None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for todo_list in todo_lists:
        text_parts = []
        if selected_list_id is not None and selected_list_id == todo_list.id:
            text_parts.append("🔹")
        text_parts.append(todo_list.name)
        btn_text = " ".join(text_parts)
        btn = InlineKeyboardButton(
            btn_text,
            callback_data=f"{callback_prefix}|{todo_list.id}",
        )
        kb.add(btn)
    return kb
