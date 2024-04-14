from telebot import TeleBot, types
from telebot.custom_filters import TextFilter

from handlers.callback_handlers.common import empty_func
from handlers.callback_handlers.todo_actions.common import validate_todo_from_callback
from handlers.keyboards.inline_keyboards.todo_list_actions import ToDoItemActionData
from handlers.message_builders.build_todo_list_texts import prepare_todo_list_parts


def handle_toggle_todo_cb(
    call: types.CallbackQuery,
    bot: TeleBot,
):
    success = validate_todo_from_callback(
        bot=bot,
        call=call,
    )
    if not success:
        return

    bot.answer_callback_query(
        callback_query_id=call.id,
        text="✅",
    )

    crud, todo_list, todo_item = success
    todo_item.done = not todo_item.done
    crud.save_state_data()

    text, kb = prepare_todo_list_parts(todo_list)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=text,
        parse_mode="HTML",
        reply_markup=kb,
    )


def register_action_toggle_todo(bot: TeleBot):
    bot.register_callback_query_handler(
        callback=handle_toggle_todo_cb,
        func=empty_func,
        text=TextFilter(
            starts_with=ToDoItemActionData.action_toggle(),
        ),
        pass_bot=True,
    )
