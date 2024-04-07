from enum import StrEnum

from telebot import (
    TeleBot,
    types,
    util,
    formatting,
)
from telebot import custom_filters
from telebot.handler_backends import StatesGroup, State

import config
import messages
from custom_filters import my_filters
from commands import default_commands
from inline_handlers.register import register_inline_handlers
from message_handlers.commands_handlers.register import register_commands_handlers
from message_handlers.register_echo_handlers import register_echo_handlers
from message_handlers.register_talk_handlers import register_regular_messages_handlers

# import lines: 16

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(my_filters.IsUserAdminOfBot())
bot.add_custom_filter(my_filters.HasEntitiesFilter())
bot.add_custom_filter(my_filters.ContainsWordFilter())
bot.add_custom_filter(my_filters.ContainsOneOfWordsFilter())

# def register_handlers():
#     register_inline_handlers(bot)
#     register_commands_handlers(bot)
#     register_regular_messages_handlers(bot)
#     register_echo_handlers(bot)


register_inline_handlers(bot)
register_commands_handlers(bot)


class SurveyStates(StatesGroup):
    full_name = State()
    user_email = State()
    email_newsletter = State()


all_survey_states = SurveyStates().state_list


def get_yes_or_no_kb():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    keyboard.add("Да", "Нет")
    return keyboard


yes_or_no_kb = get_yes_or_no_kb()

cancel_kb = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
)
cancel_kb.add("Отмена")


def is_valid_email(text: str) -> bool:
    return (
        "@" in text
        and
        "." in text
    )


def is_valid_email_message_text(message: types.Message) -> bool:
    return message.text and is_valid_email(message.text)


@bot.message_handler(commands=["survey"])
def handle_survey_command_start_survey(message: types.Message):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=SurveyStates.full_name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_welcome_what_is_your_full_name,
        parse_mode="HTML",
        reply_markup=cancel_kb,
    )


@bot.message_handler(
    commands=["cancel"],
    state=all_survey_states,
)
@bot.message_handler(
    text=custom_filters.TextFilter(
        equals="отмена",
        ignore_case=True,
    ),
    state=all_survey_states,
)
def handle_cancel_survey(message: types.Message):
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        data.pop("full_name", "")
        data.pop("user_email", "")

    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_cancelled,
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(
    state=SurveyStates.full_name,
    content_types=["text"],
)
def handle_user_full_name(message: types.Message):
    full_name = message.text
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        full_name=full_name,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=SurveyStates.user_email,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_full_name_ok_and_ask_for_email.format(
            full_name=formatting.hbold(full_name),
        ),
        parse_mode="HTML",
    )


@bot.message_handler(
    state=SurveyStates.full_name,
    content_types=util.content_type_media,
)
def handle_user_full_name_not_text(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_full_name_not_text,
        parse_mode="HTML",
    )


@bot.message_handler(
    state=SurveyStates.user_email,
    content_types=["text"],
    func=is_valid_email_message_text,
)
def handle_user_email_ok(message: types.Message):
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        user_email=message.text,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=SurveyStates.email_newsletter,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_email_ok,
        reply_markup=yes_or_no_kb,
    )


@bot.message_handler(
    state=SurveyStates.user_email,
    content_types=util.content_type_media,
)
def handle_user_email_not_ok(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_email_not_ok,
        parse_mode="HTML",
    )


@bot.message_handler(
    state=SurveyStates.email_newsletter,
    content_types=["text"],
    text=custom_filters.TextFilter(
        equals="да",
        ignore_case=True,
    )
)
@bot.message_handler(
    state=SurveyStates.email_newsletter,
    content_types=["text"],
    text=custom_filters.TextFilter(
        equals="нет",
        ignore_case=True,
    )
)
def handle_newsletter_yes_or_no(message: types.Message):
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        # full_name = data["full_name"]
        # user_email = data["user_email"]
        full_name = data.pop("full_name", "-")
        user_email = data.pop("user_email", "-@")

    text = formatting.format_text(
        "Спасибо что прошли наш опрос!",
        formatting.format_text(
            "Ваше имя:",
            formatting.hbold(full_name),
            separator=" ",
        ),
        formatting.format_text(
            "Ваш email:",
            formatting.hcode(user_email),
            separator=" ",
        ),
        formatting.format_text(
            "Подписка на рассылку:",
            formatting.hitalic(message.text.title()),
            separator=" ",
        ),
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@bot.message_handler(
    state=SurveyStates.email_newsletter,
    content_types=util.content_type_media,
)
def handle_email_newsletter_yes_or_no_not_ok(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_invalid_yes_or_no,
        reply_markup=yes_or_no_kb,
    )


register_regular_messages_handlers(bot)
register_echo_handlers(bot)


def main():
    # register_handlers()
    bot.enable_saving_states()
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True, allowed_updates=[])


if __name__ == "__main__":
    main()

# lines total: 686
