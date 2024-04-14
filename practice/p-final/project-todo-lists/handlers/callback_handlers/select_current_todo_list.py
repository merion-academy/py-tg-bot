from telebot import (
    TeleBot,
    types,
)
from telebot.custom_filters import TextFilter

from handlers.callback_handlers.common import empty_func
from handlers.keyboards.inline_keyboards.todo_lists import (
    ToDoListActionEnum,
)
from handlers.message_builders.common_select_todo_list_on_callback_button import (
    select_todo_list_on_callback,
)
from messages import TextTodo


def select_current_todo_list(
    call: types.CallbackQuery,
    bot: TeleBot,
):
    select_todo_list_on_callback(
        call=call,
        bot=bot,
        text_template=TextTodo.chosen_todo_list,
    )


def register_select_current_list_callback(bot: TeleBot):
    bot.register_callback_query_handler(
        callback=select_current_todo_list,
        func=empty_func,
        text=TextFilter(
            starts_with=str(ToDoListActionEnum.select_current_list),
        ),
        state="*",
        pass_bot=True,
    )
