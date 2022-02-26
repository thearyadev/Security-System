from flask import Flask
from . import blueprints
from .Console import Console


class Server(Flask):
    def __init__(self):
        super().__init__(__name__)  # init flask app from superclass

        self.console: Console = Console()

        self.register_blueprint()
