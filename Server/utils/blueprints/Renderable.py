from _testcapi import instancemethod

from .ParentView import View
from typing import TYPE_CHECKING
from flask import render_template
from flask_login import login_required, current_user

if TYPE_CHECKING:
    from ..Server import Server


class Renderable(View):
    def __init__(self, server: 'Server'):
        super().__init__(name=self.__class__.__name__, server=server)
        self.add_url_rule("/", view_func=self.dashboard)
        self.add_url_rule("/login", view_func=self.login)

    @instancemethod
    @login_required
    def dashboard(self):
        print(current_user)
        return render_template("dashboard.html")

    @instancemethod
    def login(self):
        return render_template("login.html")
