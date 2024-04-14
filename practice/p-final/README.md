# Проектная работа

## Списки задач

### Описание задания

**Создайте бот для управления задачами (ToDo tracker).**

**Требуемые возможности:**

- выбор текущего списка задач;
- добавление новых задач в текущий список задач;
- отметка задачи выполнено / не выполнено;
- удаление задачи (с подтверждением);
- добавление нового списка задач;
- переименование текущего списка задач;
- удаление текущего списка задач (с подтверждением);

**Рекомендации по использованию возможностей библиотеки pyTelegramBotAPI:**

- используйте машину состояний для отслеживания этапов последовательности;
- записывайте информацию по задачам в состояние (data в состоянии);
- сохраняйте данные состояния на диск;
- доставайте аргументы команд при помощи `extract_arguments`;

### Ссылки
- Фреймворк pyTelegramBotAPI на GitHub: https://github.com/eternnoir/pyTelegramBotAPI/
- Документация `pyTelegramBotAPI` https://pytba.readthedocs.io/ru/latest/