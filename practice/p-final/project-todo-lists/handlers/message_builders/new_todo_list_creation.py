from telebot import types, TeleBot

from messages import TextToDoLists
from todo_storage.todo_list import ToDoListCRUD


def add_new_todo_list_and_notify(
    new_list_name: str,
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    new_list = crud.create_todo_list_and_set_as_current(new_list_name)
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.todo_list_added_text(todo_list=new_list),
        parse_mode="HTML",
    )
