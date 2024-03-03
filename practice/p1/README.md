# Практическое задание №1

## Мой первый бот

### Описание задания

- Создайте новый проект с виртуальным окружением;
- Перейдите в терминал, убедитесь, что виртуальное окружение активировано;
- Установите `pyTelegramBotAPI` и заморозьте зависимости в файл `requirements.txt`, для этого используйте команду `pip freeze > requirements.txt`;
- Создайте бот через BotFather, получите токен;
- Научите бот обрабатывать все входящие сообщения, отвечая на них тем же текстом, что и пришёл (echo message);
- Научите бот обрабатывать команду `/start` (отдельным обработчиком);
- Научите бот обрабатывать команду `/help` (отдельным обработчиком);
- Научите бот обрабатывать команду `/joke` (отдельным обработчиком);
- В BotFather установите для своего бота известные команды;
- Вынесите токен в Python файл `config.py` (как показано на занятии);
- Создайте отдельный Python файл `messages.py`, перенесите туда все сообщения (строковые / текстовые переменные) из обработчиков команд `start` и `help`. Импортируйте `messages` по аналогии с `config`, укажите нужные переменные в соответствующих обработчиках;
- Создайте отдельный Python модуль `jokes` (файл `jokes.py`), перенесите туда список с шутками. Дополните список своими любимыми шутками. По аналогии с `config` и `messages` импортируйте модуль в основной файл `main.py`, там подключите значения из модуля в нужный обработчик;
- В обработчик всех сообщений добавьте три дополнительных условия, чтобы менять текст (как показано на занятии; убедитесь, что вы проверяете текст в нижнем регистре):
    - если в тексте сообщения содержится `"привет"`, бот должен ответить `"И тебе привет!"`;
    - если в тексте сообщения содержится `"как дела"`, бот должен ответить `"Хорошо! А у вас как?"`;
    - если в тексте сообщения содержится `"пока"` или в тексте сообщения содержится `"до свидания"`, бот должен ответить `"До новых встреч!"`;
- При старте бот должен пропускать все “ожидающие” события (это удобно при разработке, обычно при полноценном запуске бота это выключают).

### Ссылки
- Фреймворк pyTelegramBotAPI на GitHub: https://github.com/eternnoir/pyTelegramBotAPI/
- Пример обработки команд и эхо сообщений (документация pyTelegramBotAPI): https://pytba.readthedocs.io/ru/latest/quick_start.html