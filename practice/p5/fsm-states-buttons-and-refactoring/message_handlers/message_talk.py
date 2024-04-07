from telebot import (
    types,
    TeleBot,
    formatting,
)

import messages


def handle_weather_request(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        text=formatting.mbold("Хорошая погода!"),
        parse_mode="MarkdownV2",
    )


def handle_photo_with_cat_caption(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.great_cat,
        reply_to_message_id=message.id,
    )


def handle_photo(message: types.Message, bot: TeleBot):
    photo_file_id = message.photo[-1].file_id
    caption_text = "Классное фото!"
    if message.caption:
        caption_text += " Подпись:\n" + message.caption
    bot.send_photo(
        message.chat.id,
        photo=photo_file_id,
        reply_to_message_id=message.id,
        caption=caption_text,
    )


def handle_hi_message_text(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text="И тебе привет!",
    )


content_type_to_ru = {
    "text": "<текст>",
    "photo": "фото",
    "document": "документ",
}


def handle_reply_message(message: types.Message, bot: TeleBot):
    message_type = message.reply_to_message.content_type
    if message_type in content_type_to_ru:
        message_type = content_type_to_ru[message_type]

    text = (
        "Вы <b>ответили</b> на <u>это сообщение</u>, "
        f"тип - {formatting.escape_html(message_type)}."
    )
    bot.send_message(
        message.chat.id,
        text=text,
        reply_to_message_id=message.reply_to_message.id,
        parse_mode="HTML",
    )


def reply_whats_up(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        text=messages.whatsup_message_text,
    )


def reply_bye(message: types.Message, bot: TeleBot):
    bot.send_message(
        message.chat.id,
        text=formatting.mbold(messages.goodbye_message_text),
        parse_mode="MarkdownV2",
    )
