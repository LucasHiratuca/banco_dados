#Models/Vendedor.py
from Models.Funcionario import Funcionario

class Vendedor(Funcionario):
    def __init__(self, codigo, nome, salarioBase, comissao):
        super().__init__(codigo, nome)
        self._salarioBase = salarioBase #Atributo privado
        self._comissao = comissao

    def get_salarioBase(self):
        return self._salarioBase

    def set_salarioBase(self, salarioBase):
        self._salarioBase = salarioBase   

    def get_comissao(self):
        return self._comissao

    def set_comissao(self, comissao):
        self._comissao = comissao

    def calcularSalario(self):
        return self._salarioBase + self._comissao