from _testcapi import instancemethod

from .ParentView import View
from typing import TYPE_CHECKING
from flask import render_template

if TYPE_CHECKING:
    from ..Server import Server


class Renderable(View):
    def __init__(self, server: 'Server'):
        super().__init__(name=self.__class__.__name__, server=server)
        self.add_url_rule("/", view_func=self.dashboard)

    @instancemethod
    def dashboard(self):
        return render_template("dashboard.html")
