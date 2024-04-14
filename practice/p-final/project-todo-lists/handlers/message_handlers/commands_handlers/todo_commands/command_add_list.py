from telebot import TeleBot, types, util

from events_filters import has_no_command_arguments
from handlers.message_builders.common_cancel_handler import CancelHandler
from handlers.message_builders.new_todo_list_creation import (
    add_new_todo_list_and_notify,
)
from handlers.states.todo_states import AddTodoStates
from messages import TextToDoLists
from todo_storage.todo_list import ToDoListCRUD


def handle_command_add_list_show_all_lists(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    todo_lists = crud.get_lists()
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=AddTodoStates.add_todo_list,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.add_todo_list_text(todo_lists=todo_lists),
        parse_mode="HTML",
    )


def handle_text_add_todo_list(
    message: types.Message,
    bot: TeleBot,
):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    add_new_todo_list_and_notify(
        new_list_name=message.text,
        message=message,
        bot=bot,
    )


def handle_invalid_type_on_add_todo_list(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.choose_list_try_again,
    )


def handle_command_add_list_instantly(
    message: types.Message,
    bot: TeleBot,
):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    add_new_todo_list_and_notify(
        new_list_name=util.extract_arguments(message.text),
        message=message,
        bot=bot,
    )


def register_add_list_commands_handler(bot: TeleBot):
    CancelHandler.register(
        bot=bot,
        on_state=AddTodoStates.add_todo_list,
        cancel_text=TextToDoLists.cancelled_create,
    )
    bot.register_message_handler(
        callback=handle_command_add_list_show_all_lists,
        func=has_no_command_arguments,
        commands=["add_list"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_command_add_list_instantly,
        commands=["add_list"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_text_add_todo_list,
        content_types=["text"],
        state=AddTodoStates.add_todo_list,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_invalid_type_on_add_todo_list,
        content_types=util.content_type_media,
        state=AddTodoStates.add_todo_list,
        pass_bot=True,
    )
