from flask import Flask, request
from . import blueprints
from .Console import Console
import inspect
import socket
import waitress
import logging
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


class Server(Flask):
    def __init__(self):
        super().__init__(__name__, template_folder="../templates", static_folder="../static",
                         static_url_path="/")  # init flask app from superclass

        self.console: Console = Console()

        for name, member in inspect.getmembers(blueprints):
            if inspect.isclass(member):
                self.register_blueprint(member(server=self))

        logging.getLogger("waitress.queue").disabled = True
        self.after_request(self.after_request_)  # request console logging

        self.config['SECRET_KEY'] = "1234556778"
        self.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../site/users.db"
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(self)

        class User(self.db.Model, UserMixin):
            id = self.db.Column(self.db.Integer, primary_key=True)
            username = self.db.Column(self.db.String(20), unique=True, nullable=False)
            password = self.db.Column(self.db.String(60), unique=True, nullable=False)
            picture = self.db.Column(self.db.String(16), unique=False, nullable=True, default="default.jpg")

            def __repr__(self):
                return f"User('{self.id}', '{self.username}', '{self.password}', '{self.picture}')"

            def to_dict(self):
                return {"id": self.id, "username": self.username, "picture": self.picture}

        self.User = User  # class reference

        try:  # create db
            os.mkdir("../site")
        except FileExistsError:
            pass
        finally:
            self.db.create_all()

        self.bcrypt = Bcrypt(self)
        self.login_manager = LoginManager(self)
        self.login_manager.login_view = "Renderable.login"

        self.login_manager.user_loader(self.load_user)

    def start(self, host, port):
        self.console.server_log(f"Listening on http://{socket.gethostbyname(socket.gethostname())}:{port}/")
        try:
            waitress.serve(self, host=host, port=port)
        except Exception as e:
            self.console.error_log(e, f"line={e.__traceback__.tb_frame.f_lineno}")

    def after_request_(self, response):
        self.console.server_log(
            f"[yellow][{request.method}] [{response.status}][/yellow] [{request.remote_addr}]"
            f"[bold][response.status][/bold] {request.path}")
        return response

    def load_user(self, user_id):
        return self.User.query.filter_by(id=user_id).first()
