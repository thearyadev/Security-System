from _testcapi import instancemethod

from .ParentView import View
from typing import TYPE_CHECKING
from flask import send_from_directory, redirect, request, url_for, make_response
from werkzeug.exceptions import BadRequestKeyError
from flask_login import login_manager, login_user, logout_user, current_user
import uuid

if TYPE_CHECKING:
    from ..Server import Server


class API(View):
    def __init__(self, server: 'Server'):
        super().__init__(name=self.__class__.__name__, server=server)
        self.url_prefix = "/api"
        self.add_url_rule("/static/<path:path>", view_func=self.static)
        self.add_url_rule("/login", view_func=self.login, methods=['POST'])
        self.add_url_rule("/register", view_func=self.register_user, methods=['POST'])
        self.add_url_rule("/logout", view_func=self.logout)
        self.add_url_rule("/set_profile_picture", view_func=self.set_profile_picture, methods=['POST'])

    @instancemethod
    def static(self, path):
        return send_from_directory(directory="../static", path=path)

    @instancemethod
    def login(self):
        try:
            username = request.form["username"]
            password = request.form['password']
        except BadRequestKeyError as e:  # if the login forms are malformed.
            self.server.console.error_log(e)
            return redirect(url_for('Renderable.login'))  # refresh login page
        else:
            user = self.server.User.query.filter_by(username=username).first()
            if user and self.server.bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("Renderable.dashboard"))
            else:
                return redirect(url_for('Renderable.login'))  # refresh login page

    @instancemethod
    def register_user(self):
        try:
            username = request.form["username"]
            password = request.form['password']
        except BadRequestKeyError as e:  # if the login forms are malformed.
            self.server.console.error_log(e)
            return redirect(url_for('Renderable.login'))  # refresh login page
        else:
            # create user account
            user = self.server.User(
                username=username,
                password=self.server.bcrypt.generate_password_hash(password).decode("utf-8"),
            )

            self.server.db.session.add(user)
            self.server.db.session.commit()
            return redirect(url_for("Renderable.dashboard"))

    @instancemethod
    def logout(self):
        logout_user()
        return redirect(url_for("Renderable.login"))

    @instancemethod
    def set_profile_picture(self):
        file_data = request.files['pfp-upload']
        if "image" in file_data.content_type:
            filename = uuid.uuid4().hex + "." + file_data.filename.split(".")[-1]
            current_user.picture = filename
            self.server.db.session.commit()
            file_data.save(dst="static/img/profiles/" + filename)
        return redirect(url_for("Renderable.account"))
