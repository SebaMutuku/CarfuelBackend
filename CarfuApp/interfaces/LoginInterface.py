from abc import ABC, abstractmethod


class LoginInterface(ABC):
    @abstractmethod
    def create(self, data): pass

    def update(self, data): pass

    def list_users(self): pass
