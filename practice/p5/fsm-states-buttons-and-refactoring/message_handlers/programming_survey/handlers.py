from telebot import TeleBot, types, util, formatting

import messages
from custom_filters.my_filters import UpdatedTextFilter
from keyboards.common import yes_or_no_kb, cancel_kb
from keyboards.programming_survey import (
    known_programming_languages_keyboard,
    final_keyboard,
)
from message_handlers.common_registers import register_cancel_handlers
from message_handlers.programming_survey.states import (
    ProgrammingSurveyStates,
    all_programming_survey_states,
)


def handle_start_programming_survey(message: types.Message, bot: TeleBot):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=ProgrammingSurveyStates.full_name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_start_ask_full_name,
        parse_mode="HTML",
        reply_markup=cancel_kb,
    )


def handle_cancel_programming_survey(message: types.Message, bot: TeleBot):
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        data.pop("full_name", "")
        data.pop("programming_language", "")
        data.pop("experience_years", "")

    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_cancelled,
        reply_markup=types.ReplyKeyboardRemove(),
    )


def handle_programmer_user_full_name(message: types.Message, bot: TeleBot):
    full_name = message.text
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        full_name=full_name,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=ProgrammingSurveyStates.favourite_language,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_full_name_ok_and_ask_for_programming_language.format(
            full_name=formatting.hbold(full_name),
        ),
        parse_mode="HTML",
        reply_markup=known_programming_languages_keyboard,
    )


def handle_programmer_user_full_name_not_text(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_full_name_not_text,
        parse_mode="HTML",
        reply_markup=cancel_kb,
    )


def handle_favourite_language_text(message: types.Message, bot: TeleBot):
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        programming_language=message.text,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=ProgrammingSurveyStates.experience_years,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_programming_language_ok_ask_experience_years,
        reply_markup=types.ReplyKeyboardRemove(),
    )


def handle_favourite_language_not_text(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_programming_language_not_text,
        parse_mode="HTML",
        reply_markup=known_programming_languages_keyboard,
    )


def handle_experience_years_ok(message: types.Message, bot: TeleBot):
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        experience_years=message.text,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=ProgrammingSurveyStates.freelance,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_experience_number_ok_do_you_freelance,
        reply_markup=yes_or_no_kb,
    )


def handle_experience_years_not_digit(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.programming_survey_message_invalid_experience_number,
    )


def prepare_result_message_text(data: dict, message: types.Message):
    full_name = data.pop("full_name", "")
    programming_language = data.pop("programming_language", "")
    experience_years = data.pop("experience_years", "")

    text = formatting.format_text(
        "Спасибо что прошли наш опрос!",
        formatting.format_text(
            "Имя:",
            formatting.hbold(full_name),
            separator=" ",
        ),
        formatting.format_text(
            "Любимый язык программирования:",
            formatting.hcode(programming_language),
            separator=" ",
        ),
        formatting.format_text(
            "Опыт (в годах):",
            formatting.hbold(experience_years),
            separator=" ",
        ),
        formatting.format_text(
            "Увлекаетесь фрилансом:",
            formatting.hitalic(message.text.title()),
            separator=" ",
        ),
    )
    return text


def handle_freelance_yes_or_no(message: types.Message, bot: TeleBot):
    if "да" in message.text.lower():
        txt = messages.programming_survey_freelance_me_too
    else:
        txt = messages.programming_survey_freelance_its_okay
    bot.send_message(
        chat_id=message.chat.id,
        text=txt,
        reply_to_message_id=message.id,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        text = prepare_result_message_text(data, message)
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=final_keyboard,
    )


def handle_freelance_yes_or_no_not_ok(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.survey_message_invalid_yes_or_no,
        reply_markup=yes_or_no_kb,
    )


def register_programming_survey_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_start_programming_survey,
        commands=["programming_survey"],
        pass_bot=True,
    )
    register_cancel_handlers(
        bot=bot,
        handler=handle_cancel_programming_survey,
        states=all_programming_survey_states,
    )
    bot.register_message_handler(
        callback=handle_programmer_user_full_name,
        state=ProgrammingSurveyStates.full_name,
        content_types=["text"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_programmer_user_full_name_not_text,
        state=ProgrammingSurveyStates.full_name,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_favourite_language_text,
        state=ProgrammingSurveyStates.favourite_language,
        content_types=["text"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_favourite_language_not_text,
        state=ProgrammingSurveyStates.favourite_language,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_experience_years_ok,
        state=ProgrammingSurveyStates.experience_years,
        content_types=["text"],
        is_digit=True,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_experience_years_not_digit,
        state=ProgrammingSurveyStates.experience_years,
        content_types=util.content_type_media,
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_freelance_yes_or_no,
        state=ProgrammingSurveyStates.freelance,
        content_types=["text"],
        text=UpdatedTextFilter(
            equals="да",
            ignore_case=True,
        ),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_freelance_yes_or_no,
        state=ProgrammingSurveyStates.freelance,
        content_types=["text"],
        text=UpdatedTextFilter(
            equals="нет",
            ignore_case=True,
        ),
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_freelance_yes_or_no_not_ok,
        state=ProgrammingSurveyStates.freelance,
        content_types=util.content_type_media,
        pass_bot=True,
    )
