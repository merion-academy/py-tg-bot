from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from messages import TextTodo
from todo_storage.types import ToDoList


class ToDoItemActionData:
    sep = "|"
    prefix = "td-act"
    #

    toggle = "tog"
    delete = "del"
    confirm_delete = "conf-del"

    @classmethod
    def build(cls, *values) -> str:
        return cls.sep.join([cls.prefix, *map(str, values)])

    @classmethod
    def action_toggle(cls, *values) -> str:
        return cls.build(cls.toggle, *values)

    @classmethod
    def action_delete(cls, *values) -> str:
        return cls.build(cls.delete, *values)

    @classmethod
    def action_confirm_delete(cls, *values) -> str:
        return cls.build(cls.confirm_delete, *values)


def create_items_list_actions_kb(
    todo_list: ToDoList,
    flag_confirm_delete_todo_id: str | None = None,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    for todo in todo_list.items.values():
        this_todo_is_flag_confirm_delete = (
            flag_confirm_delete_todo_id and todo.id == flag_confirm_delete_todo_id
        )
        button_toggle = InlineKeyboardButton(
            text=TextTodo.todo_item_button_toggle_text(todo),
            callback_data=ToDoItemActionData.action_toggle(todo_list.id, todo.id),
        )
        if this_todo_is_flag_confirm_delete:
            action_del = ToDoItemActionData.action_confirm_delete
            delete_text = "🗑️⁉️"
        else:
            action_del = ToDoItemActionData.action_delete
            delete_text = "🗑️"

        button_delete = InlineKeyboardButton(
            text=delete_text,
            callback_data=action_del(todo_list.id, todo.id),
        )
        kb.row(button_toggle, button_delete)
    return kb
