import textwrap
from typing import Sequence, Generator

from telebot import formatting
from todo_storage.types import ToDoList, ToDoItem

start_message = """
Привет! Это бот для отслеживания задач.
Добавить новую задачу: /todo

Подробнее: /help
"""

help_message = """
Я помогу отслеживать задачи.
/todo - добавить новую задачу
/todo купить хлеб - быстро добавить одну задачу в текущий список
/todos - список задач
/lists - список списков задач
/add_list - добавить список задач
/rename_list - переименовать текущий список задач
/delete_list - удалить текущий список задач
"""


class TodoDefaults:
    default_list_name = "Список задач"


DONE_FLAGS = ["⚪", "🔳"]


please_text_or_cancel = "Пожалуйста, отправьте текстом или отмените командой /cancel"
cancel_suggestion = formatting.format_text(
    "Отменить командой /cancel или отправьте слово ",
    formatting.hcode("Отмена"),
    separator=" ",
)


class TextTodo:
    btn_text_size_max = 10
    btn_text_collapse_placeholder = "..."

    are_you_sure_you_want_to_delete = "Вы уверены, что хотите удалить эту задачу?"
    deleted_success = "Задача удалена."

    oops_list_not_found = "Список не найден, повторите попытку."
    oops_todo_not_found = "Задача не найдена, повторите попытку."

    please_dont_forward = "Пожалуйста, не пересылайте команды, это не безопасно"
    choose_list = formatting.format_text(
        "Отправьте текст, чтобы добавить задачу в список {list_name}.",
        "",
        "Кнопкой можно сменить список для добавления.",
    )
    chosen_todo_list = formatting.format_text(
        "Выбран список {list_name}.",
        "Новые задачи будут добавлены в этот список.",
    )
    choose_list_try_again: str = formatting.format_text(
        "Не понимаю.",
        please_text_or_cancel,
        choose_list,
    )
    send_todo_text = "Что добавить в список задач? (отправьте текстом)"
    added_to_default = "Добавлено в список {list_name}"
    cancelled_add = "Добавление задачи отменено."
    selected_todo_list = "Выбран список {list_name!r}"

    oops = "Ой..."
    invalid_state_on_select_todo_list = formatting.format_text(
        "Не удалось выбрать список. Попробуйте снова командой /todo",
    )

    @classmethod
    def todos_list_text(cls, todo_list: ToDoList) -> str:
        text_todos = (
            formatting.format_text(
                "-",
                DONE_FLAGS[todo.done],
                todo.title,
                separator=" ",
            )
            for todo in todo_list.items.values()
        )
        if not todo_list.items:
            text_todos = ("Нет задач в списке",)

        return formatting.format_text(
            formatting.format_text(
                "Список задач в списке",
                formatting.hbold(todo_list.name),
                separator=" ",
            ),
            "",
            *text_todos,
        )

    @classmethod
    def todo_item_button_toggle_text(cls, todo: ToDoItem):
        tog = DONE_FLAGS[todo.done]
        text = textwrap.shorten(
            todo.title,
            width=cls.btn_text_size_max,
            placeholder=cls.btn_text_collapse_placeholder,
        )
        if text == cls.btn_text_collapse_placeholder:
            end = cls.btn_text_size_max - len(cls.btn_text_collapse_placeholder)
            text = todo.title[:end] + cls.btn_text_collapse_placeholder

        return formatting.format_text(
            tog,
            text,
            separator=" ",
        )


class TextToDoLists:
    cancelled_create = "Добавление списка отменено. Добавить: /add_list"
    choose_list_try_again: str = formatting.format_text(
        "Не могу использовать это как название списка задач.",
        please_text_or_cancel,
    )
    please_provide_new_list_name: str = formatting.format_text(
        "Пожалуйста, укажите в команде новое имя для текущего списка. Например:",
        formatting.hcode("/rename_list новое название"),
    )
    done_rename_list: str = formatting.format_text(
        "Список успешно переименован.",
        "Новое название: {list_name}",
    )
    delete_list_question: str = formatting.format_text(
        "Вы уверены, что хотите удалить список {list_name}?",
        "",
        cancel_suggestion,
    )
    delete_list_unexpected: str = formatting.format_text(
        "Не могу разобрать. Точно ли нужно удалить список {list_name}?",
        "",
        cancel_suggestion,
    )
    delete_success_and_new_selected: str = formatting.format_text(
        "Список {prev_list_name} удалён.",
        "Список {new_current_list_name} выбран по умолчанию.",
    )
    delete_list_cancelled: str = formatting.format_text("Удаление списка отменено.")

    @classmethod
    def todo_lists_text_parts(
        cls,
        todo_lists: list[ToDoList],
    ) -> Sequence[str] | Generator[str, None, None]:
        if not todo_lists:
            return ("Ещё нет списков задач",)
        return (
            formatting.format_text(
                "-",
                formatting.hitalic(todo_list.name),
                separator=" ",
            )
            for todo_list in todo_lists
        )

    @classmethod
    def todo_lists_text(cls, todo_lists: list[ToDoList]) -> str:
        return formatting.format_text(
            "Ваши списки задач:",
            "",
            *cls.todo_lists_text_parts(todo_lists),
        )

    @classmethod
    def selected_current_todo_list(cls, todo_list: ToDoList) -> str:
        return formatting.format_text(
            "Выбран список",
            todo_list.name,
            separator=" ",
        )

    @classmethod
    def add_todo_list_text(cls, todo_lists: list[ToDoList]) -> str:
        return formatting.format_text(
            "Укажите название для нового списка задач.",
            "Ваши списки:",
            "",
            *cls.todo_lists_text_parts(todo_lists),
        )

    @classmethod
    def todo_list_added_text(cls, todo_list: ToDoList) -> str:
        text: str = formatting.format_text(
            "Добавлен новый список задач {list_name}.",
            "",
            "При добавлении новых задач этот список будет использован по умолчанию.",
        )
        return text.format(
            list_name=formatting.hbold(todo_list.name),
        )
