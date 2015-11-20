__author__ = 'nghia'

from app.controllers import BaseTestController
from flask_restful import Resource

class TestController(BaseTestController):

    def get(self):
        params = {
            'where': None
        }
        res = self.model.get(collection = "Shelves", params = params)
        return res
