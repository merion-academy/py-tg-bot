from message_handlers.commands_handlers.basic_commands import (
    register_basic_commands_handlers,
)
from message_handlers.commands_handlers.cat_media_commands import (
    register_cat_commands_handlers,
)
from message_handlers.commands_handlers.command_chat_id import (
    register_chat_id_command_handler,
)
from message_handlers.commands_handlers.command_me import (
    register_command_me_handlers,
)
from message_handlers.commands_handlers.command_secret import (
    register_command_secret_handlers,
)
from message_handlers.commands_handlers.jokes_commands import (
    register_jokes_commands_handlers,
)
from message_handlers.commands_handlers.markdown_commands import (
    register_markdown_handlers,
)
from message_handlers.currencies_handlers.register import (
    register_currencies_handlers,
)


def register_commands_handlers(bot):
    register_basic_commands_handlers(bot)
    register_jokes_commands_handlers(bot)
    register_cat_commands_handlers(bot)
    register_command_me_handlers(bot)
    register_chat_id_command_handler(bot)
    register_command_secret_handlers(bot)
    register_markdown_handlers(bot)
    register_currencies_handlers(bot)
