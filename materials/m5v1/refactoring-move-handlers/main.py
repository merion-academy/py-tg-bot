from io import StringIO

from telebot import TeleBot
from telebot import types
from telebot import custom_filters
from telebot import formatting
from telebot import util

import config
import messages
from custom_filters import my_filters
import currencies
from commands import default_commands
from currencies import (
    default_currency_key,
)
from inline_handlers.register import register_inline_handlers
from message_handlers.commands_handlers.register import register_commands_handlers
from message_handlers.echo_register_handlers import register_echo_handlers

# import lines: 16

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(my_filters.IsUserAdminOfBot())
bot.add_custom_filter(my_filters.HasEntitiesFilter())
bot.add_custom_filter(my_filters.ContainsWordFilter())
bot.add_custom_filter(my_filters.ContainsOneOfWordsFilter())


def register_handlers():
    register_commands_handlers(bot)
    register_inline_handlers(bot)
    # at the end:
    # register_echo_handlers(bot)


register_handlers()


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
            ),
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


def has_no_command_arguments(message: types.Message):
    return not util.extract_arguments(message.text)


@bot.message_handler(commands=["cvt"], func=has_no_command_arguments)
def handle_cvt_currency_no_arguments(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.cvt_how_to,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["cvt"])
def handle_cvt_currency(message: types.Message):
    arguments = util.extract_arguments(message.text)
    amount, _, currency = arguments.partition(" ")

    if not amount.isdigit():
        error_text = formatting.format_text(
            messages.invalid_argument_text,
            formatting.hcode(arguments),
            messages.cvt_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=error_text,
            parse_mode="HTML",
        )
        return

    currency = currency.strip()
    default_currency = "RUB"

    user_data = bot.current_states.get_data(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    )
    if user_data and default_currency_key in user_data:
        default_currency = user_data[default_currency_key]

    currency_from, currency_to = currencies.get_currencies_names(
        currency=currency,
        default_to=default_currency,
    )
    ratio = currencies.get_currency_ratio(
        from_currency=currency_from,
        to_currency=currency_to,
    )
    if ratio == currencies.ERROR_FETCHING_VALUE:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_fetching_currencies_text,
        )
        return
    if ratio in {
        currencies.ERROR_CURRENCY_NOT_FOUND,
        currencies.ERROR_CURRENCY_INVALID,
    }:
        bad_currency = currency_from
        if ratio == currencies.ERROR_CURRENCY_INVALID:
            bad_currency = currency_to
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_no_such_currency.format(
                currency=formatting.hcode(bad_currency),
            ),
            parse_mode="HTML",
        )
        return

    from_amount = int(amount)
    result_amount = from_amount * ratio
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.format_currency_convert_message(
            from_currency=currency_from,
            to_currency=currency_to,
            from_amount=from_amount,
            to_amount=result_amount,
        ),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["jpy_to_rub"])
def convert_jpy_to_rub(message: types.Message):
    arguments = util.extract_arguments(message.text)
    if not arguments:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.cvt_jpy_to_rub_how_to,
            parse_mode="HTML",
        )
        return

    if not arguments.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                messages.invalid_argument_text,
                formatting.hcode(arguments),
                separator=" ",
            ),
            messages.cvt_jpy_to_rub_how_to,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode="HTML",
        )
        return

    jpy_amount = int(arguments)
    ratio = currencies.get_jpy_to_rub_ratio()
    rub_amount = jpy_amount * ratio

    bot.send_message(
        chat_id=message.chat.id,
        text=messages.format_jpy_to_rub_message(
            jpy_amount=jpy_amount,
            rub_amount=rub_amount,
        ),
        parse_mode="HTML",
    )


@bot.message_handler(
    commands=["set_my_currency"],
    func=has_no_command_arguments,
)
def handle_no_args_to_set_my_currency(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_my_currency_help_message_text,
        parse_mode="HTML",
    )


def set_selected_currency(
    message: types.Message,
    data_key: str,
    set_currency_success_message: str,
):
    currency = util.extract_arguments(message.text) or ""
    if not currencies.is_currency_available(currency):
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_no_such_currency.format(
                currency=formatting.hcode(currency),
            ),
            parse_mode="HTML",
        )
        return

    if (
        bot.get_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
        )
        is None
    ):
        bot.set_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            state=0,
        )

    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        **{data_key: currency},
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=set_currency_success_message.format(
            currency=formatting.hcode(currency.upper()),
        ),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["set_my_currency"])
def handle_set_my_currency(message: types.Message):
    set_selected_currency(
        message=message,
        data_key=currencies.default_currency_key,
        set_currency_success_message=messages.set_my_currency_success_message_text,
    )


def current_chat_is_not_user_chat(message: types.Message):
    return message.chat.id != message.from_user.id


@bot.message_handler(
    commands=["set_local_currency"],
    func=current_chat_is_not_user_chat,
)
def set_local_currency_handle_not_private_chat(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_local_currency_only_in_private_chat,
    )


@bot.message_handler(
    commands=["set_local_currency"],
    func=has_no_command_arguments,
)
def no_arg_to_set_local_currency(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.set_local_currency_help_message,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["set_local_currency"])
def set_local_currency(message: types.Message):
    set_selected_currency(
        message=message,
        data_key=currencies.local_currency_key,
        set_currency_success_message=messages.set_local_currency_success_message,
    )


@bot.message_handler(
    text=custom_filters.TextFilter(
        contains=["погода"],
        ignore_case=True,
    )
)
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


register_echo_handlers(bot)


if __name__ == "__main__":

    bot.enable_saving_states()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True, allowed_updates=[])

# lines total: 686
