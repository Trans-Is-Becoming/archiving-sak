from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self):
        self.handles = []

    def handle(self, url, args):
        pass
