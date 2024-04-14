from telebot import types, TeleBot, formatting, util

import messages
from custom_filters.email import is_valid_email_message_text
from custom_filters.my_filters import UpdatedTextFilter
from keyboards.common import cancel_kb, yes_or_no_kb
from message_handlers.common_registers import register_cancel_handlers
from message_handlers.survey.states import SurveyStates, all_survey_states


def handle_survey_command_start_survey(message: types.Message, bot: TeleBot):
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


def handle_cancel_survey(message: types.Message, bot: TeleBot):
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


def handle_user_full_name(message: types.Message, bot: TeleBot):
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


def handle_user_full_name_not_text(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_full_name_not_text,
        parse_mode="HTML",
    )


def handle_user_email_ok(message: types.Message, bot: TeleBot):
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


def handle_user_email_not_ok(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_email_not_ok,
        parse_mode="HTML",
    )


def handle_newsletter_yes_or_no(message: types.Message, bot: TeleBot):
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


def handle_email_newsletter_yes_or_no_not_ok(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_invalid_yes_or_no,
        reply_markup=yes_or_no_kb,
    )


def register_survey_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_survey_command_start_survey,
        commands=["survey"],
        pass_bot=True,
    )
    register_cancel_handlers(
        bot=bot,
        handler=handle_cancel_survey,
        states=all_survey_states,
    )
    bot.register_message_handler(
        callback=handle_user_full_name,
        state=SurveyStates.full_name,
        content_types=["text"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_user_full_name_not_text,
        state=SurveyStates.full_name,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_user_email_ok,
        state=SurveyStates.user_email,
        content_types=["text"],
        func=is_valid_email_message_text,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_user_email_not_ok,
        state=SurveyStates.user_email,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_newsletter_yes_or_no,
        state=SurveyStates.email_newsletter,
        content_types=["text"],
        text=UpdatedTextFilter(
            equals="да",
            ignore_case=True,
        ),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_newsletter_yes_or_no,
        state=SurveyStates.email_newsletter,
        content_types=["text"],
        text=UpdatedTextFilter(
            equals="нет",
            ignore_case=True,
        ),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_email_newsletter_yes_or_no_not_ok,
        state=SurveyStates.email_newsletter,
        content_types=util.content_type_media,
        pass_bot=True,
    )
