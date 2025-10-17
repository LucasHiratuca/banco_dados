import streamlit as st
import pandas as pd
import Controllers.FuncionarioController as FuncionarioController
from Models.FreeLancer import FreeLancer
from Models.Vendedor import Vendedor
st.title('Sistema de Cadastro de Vendas')
tipo_funcionario = st.selectbox("Selecione o tipo de funcionário", ["FreeLancer", "Vendedor"])
if tipo_funcionario == "FreeLancer":
    codigo = st.number_input("Digite um código: ", min_value=0)
    nome = st.text_input("Digite um nome: ")
    diasTrabalhados = st.number_input("Digite os dias trabalhados: ", min_value=0)
    valorDia = st.number_input("Digite o valor do dia: ", min_value=0)
elif tipo_funcionario == "Vendedor":
    codigo = st.number_input("Digite um código: ", min_value=0)
    nome = st.text_input("Digite um nome: ")
    salarioBase = st.number_input("Digite o salário base: ", min_value=0)
    comissao = st.number_input("Digite a comissão: ", min_value=0)
if st.button("Inserir Funcionário"):
    if tipo_funcionario == "FreeLancer":
        funcionario = FreeLancer(codigo, nome, diasTrabalhados, valorDia)
    elif tipo_funcionario == "Vendedor":
        funcionario = Vendedor(codigo, nome, salarioBase, comissao)

    FuncionarioController.incluirFuncionario(funcionario)
    st.success("Funcionário adicionado com sucesso")
if st.button("Consultar Funcionário"):
    dados = FuncionarioController.consultarFuncionario()
    if dados:
        tb = pd.DataFrame(dados, columns=["Código", "Nome", "Tipo", "Dias Trabalhados", "Valor do dia", "Salario Base", "Comissão", "Salário Calculado"])
        st.header("Lista de Funcionários")
        st.table(tb)
    else:
        st.info("Nenhum funcionário cadastrado!")
