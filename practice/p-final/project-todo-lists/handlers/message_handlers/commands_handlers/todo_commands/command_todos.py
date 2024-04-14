from telebot import TeleBot, types

from handlers.message_builders.build_todo_list_texts import prepare_todo_list_parts
from todo_storage.todo_list import ToDoListCRUD


def handle_command_todos_show_current_list_todos(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    todo_list = crud.get_current_todo_list()
    text, kb = prepare_todo_list_parts(todo_list)
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb,
    )


def register_todos_commands_handler(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_command_todos_show_current_list_todos,
        # func=has_no_command_arguments,
        commands=["todos"],
        pass_bot=True,
    )
