from telebot import (
    TeleBot,
    types,
    util,
    formatting,
)

from events_filters import has_no_command_arguments
from handlers.message_builders.send_current_todo_lists import (
    send_message_show_todo_lists,
)
from messages import TextToDoLists
from todo_storage.todo_list import ToDoListCRUD


def handle_command_rename_current_list_no_command_args(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.please_provide_new_list_name,
        parse_mode="HTML",
    )


def handle_command_rename_current_list(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    arg = util.extract_arguments(message.text)
    todo_list = crud.rename_current_list(new_name=arg)
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.done_rename_list.format(
            list_name=formatting.hbold(todo_list.name),
        ),
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="HTML",
    )
    send_message_show_todo_lists(message, bot)


def register_rename_list_commands_handler(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_command_rename_current_list_no_command_args,
        commands=["rename_list"],
        func=has_no_command_arguments,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_command_rename_current_list,
        commands=["rename_list"],
        pass_bot=True,
    )
