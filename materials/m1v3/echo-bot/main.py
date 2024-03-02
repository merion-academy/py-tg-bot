from telebot import TeleBot, types

TOKEN = '7090687777:AAF3C9_NXMDrR7rexV-895QkhJRc5sYhwmY'

bot = TeleBot(TOKEN)


@bot.message_handler()
def send_some_message(message: types.Message):
    text = message.text
    if 'привет' in text.lower():
        text = 'И тебе привет!'
    # if 'как дела' in text.lower():
    #     text = '...'
    bot.send_message(
        message.chat.id,
        text,
    )


bot.infinity_polling()
