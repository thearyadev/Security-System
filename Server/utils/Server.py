from flask import Flask, request
from . import blueprints
from .Console import Console
import inspect
import socket
import waitress
import logging


class Server(Flask):
    def __init__(self):
        super().__init__(__name__)  # init flask app from superclass

        self.console: Console = Console()

        for name, member in inspect.getmembers(blueprints):
            if inspect.isclass(member):
                self.register_blueprint(member(server=self))

        logging.getLogger("waitress.queue").disabled = True

        @self.after_request
        def after_request(response):
            self.console.log(
                f"[yellow][{request.method}][{response.status}][/yellow] [{request.remote_addr}]"
                f"[bold][response.status][/bold] {request.path}")
            return response

    def start(self, host, port):
        self.console.server_log(f"Listening on http://{socket.gethostbyname(socket.gethostname())}:{port}/")
        try:
            waitress.serve(self, host=host, port=port)
        except Exception as e:
            self.console.error_log(e, f"line={e.__traceback__.tb_frame.f_lineno}")
