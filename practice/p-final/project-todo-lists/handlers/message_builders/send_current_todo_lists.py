from telebot import types, TeleBot

from handlers.keyboards.inline_keyboards.todo_lists import (
    create_select_list_kb,
    ToDoListActionEnum,
)
from messages import TextToDoLists
from todo_storage.todo_list import ToDoListCRUD


def send_message_show_todo_lists(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    current_list = crud.get_current_todo_list()
    todo_lists = crud.get_lists()
    kb = create_select_list_kb(
        callback_prefix=ToDoListActionEnum.select_current_list,
        todo_lists=todo_lists,
        selected_list_id=current_list.id,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.todo_lists_text(todo_lists=todo_lists),
        reply_markup=kb,
        parse_mode="HTML",
    )
