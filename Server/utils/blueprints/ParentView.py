from flask import Blueprint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Server import Server


class View(Blueprint):
    def __init__(self, name: str, server: 'Server'):
        super().__init__(name, __name__)  # init blueprint from superclass Blueprint
        self.server = server
        self.server.console.info_log(f"blueprint:[green]{self.name}[/green] loaded successfully")
