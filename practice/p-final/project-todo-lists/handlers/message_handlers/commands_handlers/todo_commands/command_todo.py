from telebot import TeleBot, types, util, formatting

from handlers.keyboards.inline_keyboards.todo_lists import ToDoListActionEnum
from handlers.message_builders.common_cancel_handler import CancelHandler
from handlers.message_builders.todo_message import todo_message_parts
from handlers.states.todo_states import AddTodoStates
from messages import TextTodo
from events_filters import has_no_command_arguments
from todo_storage.todo_list import ToDoListCRUD


def handle_forwarded_command_todo(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=TextTodo.please_dont_forward,
    )


def handle_empty_command_todo(
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
    text, kb = todo_message_parts(
        callback_prefix=ToDoListActionEnum.select_list_for_new_todo,
        current_list=current_list,
        todo_lists=todo_lists,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=AddTodoStates.choose_list_or_add_to_current,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb,
    )


def handle_add_todo_to_current_list(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    current_list, _ = crud.add_todo_item_to_current_list(
        todo_text=message.text,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=TextTodo.added_to_default.format(
            list_name=formatting.hbold(current_list.name),
        ),
        parse_mode="HTML",
    )


def handle_invalid_select_current_todo_list_or_add_todo(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    todo_lists = crud.get_lists()
    current_list = crud.get_current_todo_list()
    text, kb = todo_message_parts(
        callback_prefix=ToDoListActionEnum.select_list_for_new_todo,
        current_list=current_list,
        todo_lists=todo_lists,
        text_template=TextTodo.choose_list_try_again,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb,
    )


def handle_command_todo_with_args(
    message: types.Message,
    bot: TeleBot,
):
    crud = ToDoListCRUD(
        bot=bot,
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    )
    command_arg = util.extract_arguments(message.text) or ""
    current_list, _ = crud.add_todo_item_to_current_list(command_arg)

    bot.send_message(
        chat_id=message.chat.id,
        text=TextTodo.added_to_default.format(
            list_name=formatting.hbold(current_list.name),
        ),
        parse_mode="HTML",
    )


def register_todo_commands_handler(bot: TeleBot):
    CancelHandler.register(
        bot=bot,
        on_state=AddTodoStates.choose_list_or_add_to_current,
        cancel_text=TextTodo.cancelled_add,
    )
    bot.register_message_handler(
        callback=handle_forwarded_command_todo,
        is_forwarded=True,
        commands=["todo"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_empty_command_todo,
        func=has_no_command_arguments,
        commands=["todo"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_add_todo_to_current_list,
        state=AddTodoStates.choose_list_or_add_to_current,
        content_types=["text"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_invalid_select_current_todo_list_or_add_todo,
        state=AddTodoStates.choose_list_or_add_to_current,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_command_todo_with_args,
        commands=["todo"],
        pass_bot=True,
    )
