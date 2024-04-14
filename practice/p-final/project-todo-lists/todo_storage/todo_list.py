from typing import Any

from telebot import TeleBot

from messages import TodoDefaults
from .constants import TodoStorageConstant
from .types import ToDoItemsStorage, ToDoList, ToDoItem


class ToDoListCRUD:
    def __init__(
        self,
        bot: TeleBot,
        user_id: int | str,
        chat_id: int | str,
    ) -> None:
        self.bot = bot
        self.user_id = user_id
        self.chat_id = chat_id

        self.init_data()

    def init_data(self) -> None:
        """
        Initializes data if it doesn't exist yet
        :return:
        """
        if self.get_data() is not None:
            return

        self.bot.set_state(
            user_id=self.user_id,
            chat_id=self.chat_id,
            state=0,
        )

    def get_data(self) -> dict | None:
        return self.bot.current_states.get_data(
            user_id=self.user_id,
            chat_id=self.chat_id,
        )

    def set_data(self, key: str | int | Any, value: Any) -> None:
        self.bot.current_states.set_data(
            user_id=self.user_id,
            chat_id=self.chat_id,
            key=key,
            value=value,
        )

    def save_state_data(self) -> None:
        self.bot.current_states.save(
            user_id=self.user_id,
            chat_id=self.chat_id,
            data=self.get_data(),
        )

    def get_todos_storage(self) -> ToDoItemsStorage:
        data = self.get_data()
        key = TodoStorageConstant.storage
        if key in data:
            return data[key]

        new_storage = ToDoItemsStorage()
        self.set_data(
            key=key,
            value=new_storage,
        )
        return new_storage

    def get_todo_list(
        self,
        list_id: str,
    ) -> ToDoList | None:
        storage: ToDoItemsStorage = self.get_todos_storage()
        return storage.todo_lists.get(list_id)

    def create_todo_list(
        self,
        name: str,
    ) -> ToDoList:
        storage: ToDoItemsStorage = self.get_todos_storage()
        todo_list = ToDoList(name=name)
        storage.todo_lists[todo_list.id] = todo_list
        self.save_state_data()
        return todo_list

    def set_current_todo_list(self, todo_list_id: str) -> None:
        self.set_data(
            key=TodoStorageConstant.current_list_id_key,
            value=todo_list_id,
        )

    def get_current_todo_list_id(self) -> str | None:
        key = TodoStorageConstant.current_list_id_key
        data = self.get_data()
        if key in data:
            return data[key]

    def create_todo_list_and_set_as_current(self, name: str) -> ToDoList:
        new_list = self.create_todo_list(name=name)
        self.set_current_todo_list(new_list.id)
        return new_list

    def create_and_set_default_todo_list(self) -> ToDoList:
        return self.create_todo_list_and_set_as_current(
            name=TodoDefaults.default_list_name,
        )

    def get_current_todo_list(self) -> ToDoList:
        current_list_id = self.get_current_todo_list_id()
        if current_list_id is not None:
            todo_list = self.get_todo_list(list_id=current_list_id)
            if todo_list is not None:
                return todo_list

        return self.create_and_set_default_todo_list()

    def delete_current_todo_list(self) -> ToDoList:
        storage: ToDoItemsStorage = self.get_todos_storage()
        current_list_id = self.get_current_todo_list_id()
        if current_list_id in storage.todo_lists:
            storage.todo_lists.pop(current_list_id)
        if not storage.todo_lists:
            return self.create_and_set_default_todo_list()
        todo_list: ToDoList = next(iter(storage.todo_lists.values()))
        self.set_current_todo_list(todo_list.id)
        return todo_list

    def add_todo_item_to_current_list(
        self,
        todo_text: str,
    ) -> tuple[ToDoList, ToDoItem]:
        todo_list = self.get_current_todo_list()
        todo_item = ToDoItem(title=todo_text)
        todo_list.items[todo_item.id] = todo_item
        self.save_state_data()
        return todo_list, todo_item

    def get_lists(self) -> list[ToDoList]:
        storage: ToDoItemsStorage = self.get_todos_storage()
        return list(storage.todo_lists.values())

    def get_list(self, list_key: int | str) -> ToDoList | None:
        storage: ToDoItemsStorage = self.get_todos_storage()
        return storage.todo_lists.get(list_key)

    def rename_current_list(self, new_name: str) -> ToDoList:
        todo_list = self.get_current_todo_list()
        todo_list.name = new_name
        self.save_state_data()
        return todo_list
