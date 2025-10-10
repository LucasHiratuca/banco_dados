#main.py
import streamlit as st
import pandas as pd
import Controllers.FuncionarioController as FuncionariosController
from Models.FreeLancer import FreeLancer
from Models.Vendedor import Vendedor

#Interface principal
st.title('Sistema de cadastro de vendas')
tipo_funcionario = st.selectbox("Selecione o tipo de funcionário:", ['FreeLancer', 'Vendedor'])

if tipo_funcionario == "FreeLancer":
    codigo = st.number_input("Digite um código: ", min_value=0)
    nome = st.text_input("Digite um nome: ")
    diasTrabalhados = st.number_input("Digite dias trabalhados: ", min_value=0)
    valorDia = st.number_input("Digite o valor do dia: ", min_value=0)

elif tipo_funcionario == "Vendedor":
    codigo = st.number_input("Digite um código: ", min_value=0)
    nome = st.text_input("Digite um nome: ")
    salarioBase = st.number_input("Digite o salário base: ", min_value=0)
    comissao = st.number_input("Digite o valor da comissão: ", min_value=0)

if st.button("Inserir Funcionário"):
    if tipo_funcionario == "FreeLancer":
        funcionario = FreeLancer(codigo, nome, diasTrabalhados, valorDia)
    elif tipo_funcionario == "Vendedor":
        funcionario = Vendedor(codigo, nome, salarioBase, comissao)

FuncionariosController.incluirFuncionario(Funcionario)
st.success("Funcionário adicionado com sucesso. ")

if st.button("Consultar funcionário"):
    dados = FuncionariosController.consultarFuncionario()
    if dados:
        #Cria um dataframe com os dados
        tb = pd.DataFrame(dados, columns=["Código", "Nome", "Dias Trabalhados", "Valor do Dia", "Salario Base", "Comissão", "Salário Total"])
        st.header("Lista de Funcionários")
        st.table(tb)
    else:
        st.info("Nenhum Funcionário cdastrado! ")