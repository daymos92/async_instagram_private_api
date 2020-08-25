from abc import ABC


class Repository(ABC):
    def __init__(self, client):
        self.client = client
