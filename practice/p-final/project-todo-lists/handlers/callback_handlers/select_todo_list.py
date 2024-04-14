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
from handlers.states.todo_states import AddTodoStates
from messages import TextTodo


def select_current_todo_list_and_wait_for_new_todo(
    call: types.CallbackQuery,
    bot: TeleBot,
):
    select_todo_list_on_callback(
        call=call,
        bot=bot,
        text_template=TextTodo.choose_list,
    )


def no_state_on_select_current_todo_list(
    call: types.CallbackQuery,
    bot: TeleBot,
):
    bot.answer_callback_query(
        callback_query_id=call.id,
        text=TextTodo.oops,
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=TextTodo.invalid_state_on_select_todo_list,
        reply_markup=None,
    )


def register_select_current_list_for_new_todo_callback(bot: TeleBot):
    bot.register_callback_query_handler(
        callback=select_current_todo_list_and_wait_for_new_todo,
        func=empty_func,
        text=TextFilter(
            starts_with=str(ToDoListActionEnum.select_list_for_new_todo),
        ),
        state=AddTodoStates.choose_list_or_add_to_current,
        pass_bot=True,
    )

    bot.register_callback_query_handler(
        callback=no_state_on_select_current_todo_list,
        func=empty_func,
        text=TextFilter(
            starts_with=str(ToDoListActionEnum.select_list_for_new_todo),
        ),
        state="*",
        pass_bot=True,
    )
