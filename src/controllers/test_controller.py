__author__ = 'nghia'

from src.controllers import BaseTestController
from flask_restful import Resource

class TestController(BaseTestController):
    pass
    # def get(self):
    #     params = {
    #         'where': None
    #     }
    #     res = self.model.get(collection = "Shelves", params = params)
    #     return res
