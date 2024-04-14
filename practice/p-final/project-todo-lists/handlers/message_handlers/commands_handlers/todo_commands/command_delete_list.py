from telebot import (
    TeleBot,
    types,
    util,
    formatting,
)
from telebot.custom_filters import TextFilter

from handlers.keyboards.reply_keyboards.confirm_keyboards import kb_yes_or_no
from handlers.message_builders.common_cancel_handler import CancelHandler
from handlers.states.todo_states import ToDoListActionStates
from messages import TextToDoLists
from todo_storage.todo_list import ToDoListCRUD


def ask_for_current_list_deletion(
    message: types.Message,
    bot: TeleBot,
    text_template: str,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    todo_list = crud.get_current_todo_list()
    bot.send_message(
        chat_id=message.chat.id,
        text=text_template.format(
            list_name=formatting.hbold(todo_list.name),
        ),
        parse_mode="HTML",
        reply_markup=kb_yes_or_no,
    )


def handle_command_delete_current_list(
    message: types.Message,
    bot: TeleBot,
):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=ToDoListActionStates.delete_todo_list,
    )
    ask_for_current_list_deletion(
        message=message,
        bot=bot,
        text_template=TextToDoLists.delete_list_question,
    )


def handle_confirm_delete_list(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    to_be_removed_list = crud.get_current_todo_list()
    current_list = crud.delete_current_todo_list()
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=TextToDoLists.delete_success_and_new_selected.format(
            prev_list_name=formatting.hbold(to_be_removed_list.name),
            new_current_list_name=formatting.hbold(current_list.name),
        ),
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )


def handle_invalid_answer_confirm_delete_list(
    message: types.Message,
    bot: TeleBot,
):
    ask_for_current_list_deletion(
        message=message,
        bot=bot,
        text_template=TextToDoLists.delete_list_unexpected,
    )


def register_delete_list_commands_handler(bot: TeleBot):
    CancelHandler.register(
        bot=bot,
        on_state=ToDoListActionStates.delete_todo_list,
        cancel_text=TextToDoLists.delete_list_cancelled,
    )
    bot.register_message_handler(
        callback=handle_command_delete_current_list,
        commands=["delete_list"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_confirm_delete_list,
        content_types=["text"],
        state=ToDoListActionStates.delete_todo_list,
        text=TextFilter(equals="да", ignore_case=True),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=CancelHandler(text=TextToDoLists.delete_list_cancelled),
        content_types=["text"],
        state=ToDoListActionStates.delete_todo_list,
        text=TextFilter(equals="нет", ignore_case=True),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_invalid_answer_confirm_delete_list,
        content_types=util.content_type_media,
        state=ToDoListActionStates.delete_todo_list,
        pass_bot=True,
    )
