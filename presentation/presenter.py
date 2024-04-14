from typing import Any


class BasePresenter:
    view: Any

    def __init__(self) -> None:
        self.view = None

    def bind(self, view) -> None:
        self.view = view

    def unbind(self) -> None:
        self.view = None
