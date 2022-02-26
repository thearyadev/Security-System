from _testcapi import instancemethod

from .ParentView import View
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Server import Server


class Logging(View):
    def __init__(self, server: 'Server'):
        super().__init__(name=self.__class__.__name__, server=server)
