from dataclasses import dataclass, field

from utils import generate_id


ToDoIdType = str
ToDoListIdType = str


@dataclass
class ToDoItem:
    id: ToDoIdType = field(default_factory=generate_id)
    title: str = "todo"
    done: bool = False


@dataclass
class ToDoList:
    id: ToDoListIdType = field(default_factory=generate_id)
    name: str = "list"
    items: dict[ToDoIdType, ToDoItem] = field(default_factory=dict)


@dataclass
class ToDoItemsStorage:
    todo_lists: dict[ToDoListIdType, ToDoList] = field(default_factory=dict)
