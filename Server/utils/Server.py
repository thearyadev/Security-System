from flask import Flask


class Server(Flask):
    def __init__(self):
        super().__init__(__name__)