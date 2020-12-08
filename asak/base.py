from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self):
        pass

    def handle(self, url, args):
        pass
