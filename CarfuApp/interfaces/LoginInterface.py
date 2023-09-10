from abc import ABC, abstractmethod


class BaseLogin(type):
    @abstractmethod
    def create(self, data): pass

    def update(self, instance, validated_data): pass

    def list_users(self): pass

    def authenticate(self, request): pass
