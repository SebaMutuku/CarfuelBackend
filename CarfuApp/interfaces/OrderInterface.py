from abc import ABC, abstractmethod


class OrderInterface(ABC):
    @abstractmethod
    def create(self, data): pass

    def update(self, data): pass

    def list_orders(self): pass
