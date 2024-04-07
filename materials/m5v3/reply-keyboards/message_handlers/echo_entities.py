from telebot import (
    types,
    TeleBot,
    formatting,
)


def echo_and_show_entities(message: types.Message, bot: TeleBot):
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


def echo_and_show_entities_2(message: types.Message, bot: TeleBot):
    entity_names = {formatting.hcode(entity.type) for entity in message.entities}
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
