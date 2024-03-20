from io import StringIO

from telebot import TeleBot
from telebot import types
from telebot import custom_filters
from telebot import formatting

import config
import jokes
import messages
import my_filters

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(my_filters.IsUserAdminOfBot())
bot.add_custom_filter(my_filters.HasEntitiesFilter())
bot.add_custom_filter(my_filters.ContainsWordFilter())
bot.add_custom_filter(my_filters.ContainsOneOfWordsFilter())


@bot.message_handler(commands=["start"])
def handle_start_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.start_text,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["help"])
def handle_help_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.help_text,
    )


@bot.message_handler(commands=["joke"])
def send_random_joke(message: types.Message):
    bot.send_message(
        message.chat.id,
        formatting.hcite(
            jokes.get_random_joke_text()
        ),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["joke2"])
def send_random_two_part_joke(message: types.Message):
    setup, delivery = jokes.get_two_part_joke_texts()

    text = formatting.format_text(
        formatting.escape_html(setup),
        formatting.hspoiler(delivery),
    )
    bot.send_message(
        message.chat.id,
        text=text,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["cat_file"])
def send_cat_photo_as_file(message: types.Message):
    bot.send_document(
        chat_id=message.chat.id,
        document=config.CAT_PIC_URL,
    )


@bot.message_handler(commands=["cat"])
def send_cat_photo(message: types.Message):
    bot.send_photo(
        chat_id=message.chat.id,
        photo=config.CAT_PIC_URL,
        reply_to_message_id=message.id,
    )


@bot.message_handler(commands=["me"], is_forwarded=True)
def handle_forwarded_text_command(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.dont_forward_commands,
    )


@bot.message_handler(commands=["me"])
def send_text_doc_from_memory(message: types.Message):
    file = StringIO()
    file.write("User info:\n")
    file.write("User id: ")
    file.write(str(message.from_user.id))
    file.write("\n")
    file.write("First name: ")
    file.write(message.from_user.first_name)
    file.write("\n")
    file.write("Last name: ")
    file.write(message.from_user.last_name)
    file.write("\n")
    file.write("username: ")
    file.write(message.from_user.username)
    file.write("\n")
    file.seek(0)
    file_text_doc = types.InputFile(file)
    bot.send_document(
        chat_id=message.chat.id,
        document=file_text_doc,
        visible_file_name="your-info.txt",
        caption=messages.user_info_doc_caption,
    )


@bot.message_handler(commands=["chat_id"])
def handle_chat_id_request(message: types.Message):
    text = formatting.format_text(
        formatting.format_text(
            "Айди чата:",
            formatting.hcode(str(message.chat.id)),
            separator=" ",
        ),
        formatting.format_text(
            "Айди отправителя:",
            formatting.hcode(str(message.from_user.id)),
            separator=" ",
        ),
    )
    if message.reply_to_message:
        text = formatting.format_text(
            text,
            formatting.format_text(
                "Отвечено на сообщение от",
                formatting.hcode(str(message.reply_to_message.from_user.id)),
            )
        )
    bot.send_message(
        message.chat.id,
        text=text,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["secret"], is_bot_admin=True)
def handle_admin_secret(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=messages.secret_message_for_admin,
    )


@bot.message_handler(commands=["secret"], is_bot_admin=False)
def handle_not_admin_request_secret(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=messages.secret_message_not_admin,
    )


@bot.message_handler(commands=["md"])
def send_markdown_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.markdown_text,
        parse_mode="MarkdownV2",
    )


@bot.message_handler(commands=["html"])
def send_html_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.html_text,
        parse_mode="HTML",
    )


@bot.message_handler(text=custom_filters.TextFilter(
    contains=["погода"],
    ignore_case=True,
))
def handle_weather_request(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=formatting.mbold("Хорошая погода!"),
        parse_mode="MarkdownV2",
    )


@bot.message_handler(
    content_types=["photo"],
    contains_word="кот",
)
def handle_photo_with_cat_caption(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.great_cat,
        reply_to_message_id=message.id,
    )


@bot.message_handler(content_types=["photo"])
def handle_photo(message: types.Message):
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


@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: types.Message):
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=message.sticker.file_id,
        reply_to_message_id=message.id,
    )


@bot.message_handler(contains_word="привет")
def handle_hi_message_text(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="И тебе привет!",
    )


content_type_to_ru = {
    "text": "<текст>",
    "photo": "фото",
    "document": "документ",
}


@bot.message_handler(is_reply=True)
def handle_reply_message(message: types.Message):
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


@bot.message_handler(contains_word="как дела")
def reply_whats_up(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=messages.whatsup_message_text,
    )


@bot.message_handler(contains_one_of_words=["пока", "до свидания"])
def reply_bye(message: types.Message):
    bot.send_message(
        message.chat.id,
        text=formatting.mbold(messages.goodbye_message_text),
        parse_mode="MarkdownV2",
    )


@bot.message_handler(has_entities=True, contains_word="проверка")
def echo_and_show_entities(message: types.Message):
    named_entities = {entity.type for entity in message.entities}
    text = formatting.format_text(
        message.text,
        f"Entities: {', '.join(named_entities)}",
        separator="\n\n",
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        entities=message.entities,
    )


@bot.message_handler(has_entities=True)
def echo_and_show_entities_2(message: types.Message):
    entity_names = {
        formatting.hcode(entity.type)
        for entity in message.entities
    }
    text = formatting.format_text(
        message.html_text,
        formatting.format_text(
            "Entities:",
            ", ".join(entity_names),
            separator=" ",
        ),
        separator="\n\n",
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
    )


@bot.message_handler()
def send_echo_message(message: types.Message):
    text = message.text
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        entities=message.entities,
    )


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
