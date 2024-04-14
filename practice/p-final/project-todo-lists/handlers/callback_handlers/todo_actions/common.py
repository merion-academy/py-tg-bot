from telebot import TeleBot, types

from handlers.keyboards.inline_keyboards.todo_list_actions import ToDoItemActionData
from messages import TextTodo
from todo_storage.todo_list import ToDoListCRUD
from todo_storage.types import ToDoList, ToDoItem


def validate_todo_from_callback(
    bot: TeleBot,
    call: types.CallbackQuery,
) -> tuple[ToDoListCRUD, ToDoList, ToDoItem] | None:
    prefix, action, todo_list_id, todo_id = call.data.split(ToDoItemActionData.sep)
    crud = ToDoListCRUD(
        bot=bot,
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
    )
    todo_list = crud.get_todo_list(todo_list_id)
    if not todo_list:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=TextTodo.oops_list_not_found,
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=TextTodo.oops_list_not_found,
            reply_markup=None,
        )
        return None

    todo_item = todo_list.items.get(todo_id)
    if not todo_item:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=TextTodo.oops_todo_not_found,
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=TextTodo.oops_todo_not_found,
            reply_markup=None,
        )
        return None

    return crud, todo_list, todo_item
