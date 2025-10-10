#Models/Funcionario.py
from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, codigo, nome):
        self._codigo = codigo
        self._nome = nome 

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        self._codigo = codigo   

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    @abstractmethod
    def calcularSalario(self):
        pass


