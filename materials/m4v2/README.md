# 12. Inline query: бот в любом чате

## Ссылки:
- Фреймворк pyTelegramBotAPI на GitHub: https://github.com/eternnoir/pyTelegramBotAPI/
- Презентация inline https://telegram.org/blog/inline-bots
- Inline Bots https://core.telegram.org/bots/inline
- `answerInlineQuery` https://core.telegram.org/bots/api#answerinlinequery
- `InlineQueryResult` https://core.telegram.org/bots/api#inlinequeryresult

### Подсказки
Если бот не получает обновления inline query, попробуйте указать `allowed_updates=[]` в [метод `infinity_polling`](https://pytba.readthedocs.io/ru/latest/sync_version/index.html#telebot.TeleBot.infinity_polling).

[Поле `allowed_updates` в методе `getUpdates`](https://core.telegram.org/bots/api#getupdates:~:text=testing%20purposes%20only.-,allowed_updates,-Array%20of%20String).

