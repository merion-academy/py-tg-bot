from telebot import TeleBot, types, util


def send_echo_message(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_message(
        chat_id=message.chat.id,
        text=message.text,
        entities=message.entities,
    )


def handle_sticker(
    message: types.Message,
    bot: TeleBot,
):
    bot.send_sticker(
        chat_id=message.chat.id,
        sticker=message.sticker.file_id,
        reply_to_message_id=message.id,
    )


def handle_any_other_message(
    message: types.Message,
    bot: TeleBot,
):
    bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.id,
    )


def register_echo_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_sticker,
        content_types=["sticker"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=send_echo_message,
        content_types=["text"],
        pass_bot=True,
    )
    bot.register_message_handler(
        callback=handle_any_other_message,
        content_types=util.content_type_media,
        pass_bot=True,
    )
