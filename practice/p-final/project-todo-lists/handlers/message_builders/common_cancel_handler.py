from telebot import types, TeleBot
from telebot.custom_filters import TextFilter


class CancelHandler:
    def __init__(self, text: str):
        self.text = text

    def __call__(
        self,
        message: types.Message,
        bot: TeleBot,
    ):
        bot.set_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            state=0,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=self.text,
            reply_markup=types.ReplyKeyboardRemove(),
        )

    @classmethod
    def register(
        cls,
        bot: TeleBot,
        on_state,
        cancel_text: str,
        pass_bot: bool = True,
    ):
        bot.register_message_handler(
            callback=cls(text=cancel_text),
            commands=["cancel"],
            state=on_state,
            pass_bot=pass_bot,
        )
        bot.register_message_handler(
            callback=cls(text=cancel_text),
            text=TextFilter(
                equals="отмена",
                ignore_case=True,
            ),
            state=on_state,
            pass_bot=pass_bot,
        )
