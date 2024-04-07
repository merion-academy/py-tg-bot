from telebot import (
    types,
    TeleBot,
    formatting,
)


def handle_chat_id_request(message: types.Message, bot: TeleBot):
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


def register_chat_id_command_handler(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_chat_id_request,
        commands=["chat_id"],
        pass_bot=True,
    )
