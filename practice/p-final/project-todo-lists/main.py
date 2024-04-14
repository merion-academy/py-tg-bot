from telebot import TeleBot
from telebot import custom_filters

import config
from commands import default_commands
from handlers import register_handlers


def register_filters(bot: TeleBot):
    bot.add_custom_filter(custom_filters.TextMatchFilter())
    bot.add_custom_filter(custom_filters.ForwardFilter())
    bot.add_custom_filter(custom_filters.IsReplyFilter())
    bot.add_custom_filter(custom_filters.StateFilter(bot))


def init_bot(token: str) -> TeleBot:
    bot = TeleBot(token)
    bot.enable_saving_states()
    bot.set_my_commands(default_commands)
    return bot


def main():
    bot = init_bot(config.BOT_TOKEN)
    register_filters(bot)
    register_handlers(bot)
    bot.infinity_polling(
        skip_pending=True,
        allowed_updates=[],
    )


if __name__ == "__main__":
    main()
