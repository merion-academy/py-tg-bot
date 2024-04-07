# Практическое задание №5

## Осмысленные диалоги. Кнопки. Рефакторинг

### Описание задания

- Проведите рефакторинг всего написанного кода: разнесите обработчики по модулям;
- Добавьте работу с inline кнопками, реализуйте обработку callback query (например, как показано в видео);
- Создайте новый опрос для пользователя. Например, это может быть опрос для программистов: спросите имя, любимый язык программирования, сколько лет опыта, а также увлекается ли человек фрилансом.
    - Добавьте обработчики для неожиданных случаев;
    - В последнем сообщении (в сводке) добавьте инлайн клавиатуру, в этой клавиатуре может быть ссылка на сайт. Учтите, что нельзя отправить одновременно и inline клавиатуру и команду на удаление клавиатуры, поэтому можно добавить ещё одно сообщение для ответа, чтобы удалить клавиатуру;
- Добавьте команду для начала опроса в сообщение help и в bot commands (чтобы бот установил себе команду при старте);
- Убедитесь, что после всех изменений бот продолжает работать (как и до рефакторинга).

### Ссылки
- Фреймворк pyTelegramBotAPI на GitHub: https://github.com/eternnoir/pyTelegramBotAPI/
- метод `register_message_handler` в `TeleBot` https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.register_message_handler
- класс `ReplyKeyboardMarkup` в `TeleBot` https://pytba.readthedocs.io/ru/latest/types.html#telebot.types.ReplyKeyboardMarkup
- класс `InlineKeyboardMarkup` в `TeleBot` https://pytba.readthedocs.io/ru/latest/types.html#telebot.types.InlineKeyboardMarkup
- метод `set_state` в `TeleBot` https://pytba.readthedocs.io/ru/latest/sync_version/index.html#telebot.TeleBot.set_state
- метод `add_data` в `TeleBot` https://pytba.readthedocs.io/ru/latest/sync_version/index.html#telebot.TeleBot.add_data
- метод `retrieve_data` в `TeleBot` https://pytba.readthedocs.io/ru/latest/sync_version/index.html#telebot.TeleBot.retrieve_data
