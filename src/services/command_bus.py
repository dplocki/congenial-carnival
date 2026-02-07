from typing import Container, Type
from services.store import Store


class CommandBus:

    def __init__(self, store: Store, container: Container):
        self.store = store
        self.container = container

    def handle(self, type: Type, *data) -> None:
        command = self.container.resolve(type)
        for event in command.execute(*data):
            self.store.add_event(event)
