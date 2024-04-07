from telebot import TeleBot
from telebot import custom_filters

import config
from callback_handlers.register import register_callback_query_handlers
from custom_filters import my_filters
from commands import default_commands
from inline_handlers.register import register_inline_handlers
from message_handlers.commands_handlers.register import register_commands_handlers
from message_handlers.programming_survey.handlers import (
    register_programming_survey_handlers,
)
from message_handlers.register_echo_handlers import register_echo_handlers
from message_handlers.register_talk_handlers import register_regular_messages_handlers
from message_handlers.survey.handlers import register_survey_handlers

# import lines: 16

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.ForwardFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(my_filters.IsUserAdminOfBot())
bot.add_custom_filter(my_filters.HasEntitiesFilter())
bot.add_custom_filter(my_filters.ContainsWordFilter())
bot.add_custom_filter(my_filters.ContainsOneOfWordsFilter())


def register_handlers():
    register_inline_handlers(bot)
    register_commands_handlers(bot)
    register_callback_query_handlers(bot)
    register_survey_handlers(bot)
    register_programming_survey_handlers(bot)
    register_regular_messages_handlers(bot)
    register_echo_handlers(bot)


def main():
    register_handlers()
    bot.enable_saving_states()
    # bot.enable_save_next_step_handlers(delay=2)
    # bot.load_next_step_handlers()
    bot.set_my_commands(default_commands)
    bot.infinity_polling(skip_pending=True, allowed_updates=[])


if __name__ == "__main__":
    main()

# lines total: 686
