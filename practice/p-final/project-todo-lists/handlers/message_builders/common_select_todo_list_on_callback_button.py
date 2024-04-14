from telebot import types, TeleBot

from handlers.message_builders.todo_message import todo_message_parts
from messages import TextTodo
from todo_storage.todo_list import ToDoListCRUD


def select_todo_list_on_callback(
    call: types.CallbackQuery,
    bot: TeleBot,
    text_template: str,
) -> None:
    crud = ToDoListCRUD(
        bot=bot,
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
    )
    # callback_data=f"{prefix}|{todo_list.id}",
    callback_prefix, _, list_id = call.data.partition("|")
    crud.set_current_todo_list(list_id)
    current_list = crud.get_current_todo_list()
    bot.answer_callback_query(
        callback_query_id=call.id,
        text=TextTodo.selected_todo_list.format(
            list_name=current_list.name,
        ),
    )
    todo_lists = crud.get_lists()
    text, kb = todo_message_parts(
        callback_prefix=callback_prefix,
        current_list=current_list,
        todo_lists=todo_lists,
        text_template=text_template,
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb,
    )
