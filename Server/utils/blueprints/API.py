from flask import Blueprint
from .ParentView import View
from ...utils.Server import Server


class API(View):
    def __init__(self, server: Server):
        super().__init__(name=self.__class__.__name__, server=server)
