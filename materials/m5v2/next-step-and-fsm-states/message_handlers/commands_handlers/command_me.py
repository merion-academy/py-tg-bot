from io import StringIO

from telebot import (
    types,
    TeleBot,
)

import messages


def handle_forwarded_text_command(message: types.Message, bot: TeleBot):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.dont_forward_commands,
    )


def send_text_doc_from_memory(message: types.Message, bot: TeleBot):
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


def register_command_me_handlers(bot: TeleBot):
    bot.register_message_handler(
        callback=handle_forwarded_text_command,
        commands=["me"],
        is_forwarded=True,
        pass_bot=True,
    )

    bot.register_message_handler(
        callback=send_text_doc_from_memory,
        commands=["me"],
        pass_bot=True,
    )
