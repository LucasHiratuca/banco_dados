# Views/PageFuncionario.py
import streamlit as st
import pandas as pd
import Controllers.FuncionarioController as funcionarioController
from Models.FreeLancer import FreeLancer
from Models.Vendedor import Vendedor

def show_funcionario_page():
    st.title('Cadastro de Funcionários')

    # Menu de operações para Funcionário
    Page_Funcionario = st.sidebar.selectbox("Operações", ["Incluir", "Consultar", "Excluir", "Alterar"])

    if Page_Funcionario == "Incluir":
        tipo_funcionario = st.selectbox("Selecione o tipo de funcionário", ["FreeLancer", "Vendedor"])

        if tipo_funcionario == "FreeLancer":
            # Criar instância de FreeLancer
            freelancer = FreeLancer(0, "", 0, 0.0)
            
            # Usar setters
            freelancer.set_codigo(st.number_input("Digite seu código: ", min_value=0))
            freelancer.set_nome(st.text_input("Digite seu nome: "))
            freelancer.set_diasTrabalhados(st.number_input("Digite os dias trabalhados: ", min_value=0))
            freelancer.set_valorDia(st.number_input("Digite o valor por dia: ", min_value=0.0, format="%.2f"))
            
            # Calcular salário
            salario = freelancer.calcularSalario()
            st.write(f"Salário Atual: R$ {salario:.2f}")

            # Botão para inserir
            if st.button("Inserir"):
                funcionarioController.incluirFuncionario(freelancer)
                st.success("FreeLancer adicionado com sucesso!")

        elif tipo_funcionario == "Vendedor":
            # Criar instância de Vendedor
            vendedor = Vendedor(0, "", 0.0, 0.0)
            
            # Usar setters
            vendedor.set_codigo(st.number_input("Digite seu código: ", min_value=0))
            vendedor.set_nome(st.text_input("Digite seu nome: "))
            vendedor.set_salarioBase(st.number_input("Digite o salário base: ", min_value=0.0, format="%.2f"))
            vendedor.set_comissao(st.number_input("Digite a comissão: ", min_value=0.0, format="%.2f"))
            
            # Calcular salário
            salario = vendedor.calcularSalario()
            st.write(f"Salário Atual: R$ {salario:.2f}")

            # Botão para inserir
            if st.button("Inserir"):
                funcionarioController.incluirFuncionario(vendedor)
                st.success("Vendedor adicionado com sucesso!")

    elif Page_Funcionario == "Consultar":
        if st.button("Consultar"):
            dados = funcionarioController.consultarFuncionario()
            if dados:
                # Formatação dos dados
                for item in dados:
                    for key in ["Valor Dia", "Salário Base", "Comissão", "Salário Calculado"]:
                        if item[key] is not None:
                            item[key] = round(item[key], 2)
                
                tb = pd.DataFrame(dados, columns=["Código", "Nome", "Tipo", "Dias Trabalhados", 
                                                 "Valor Dia", "Salário Base", "Comissão", "Salário Calculado"])
                st.header("Lista de Funcionários")
                st.dataframe(tb, width=1000)
            else:
                st.info("Nenhum Funcionário cadastrado.")

    elif Page_Funcionario == "Excluir":
        st.subheader("Excluir Funcionário")
        dados = funcionarioController.consultarFuncionario()

        if dados:
            df = pd.DataFrame(dados, columns=["Código", "Nome", "Tipo", "Dias Trabalhados", 
                                            "Valor Dia", "Salário Base", "Comissão", "Salário Calculado"])
            st.table(df)

            codigo_excluir = st.number_input("Digite o código do funcionário que deseja excluir", min_value=1, step=1)
            if st.button("Excluir"):
                try:
                    funcionarioController.excluirFuncionario(codigo_excluir)
                    st.success(f"Funcionário com código {codigo_excluir} excluído com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir funcionário: {e}")
        else:
            st.info("Nenhum funcionário cadastrado.")

    elif Page_Funcionario == "Alterar":
        st.subheader("Alterar Funcionário")
        dados = funcionarioController.consultarFuncionario()

        if dados:
            df = pd.DataFrame(dados, columns=["Código", "Nome", "Tipo", "Dias Trabalhados", 
                                            "Valor Dia", "Salário Base", "Comissão", "Salário Calculado"])
            st.table(df)

            codigo_alterar = st.number_input("Digite o código do funcionário que deseja alterar", min_value=1, step=1)
            funcionario_data = next((item for item in dados if item["Código"] == codigo_alterar), None)

            if funcionario_data:
                if funcionario_data["Tipo"] == "FreeLancer":
                    # Criar instância de FreeLancer com os dados atuais
                    funcionario = FreeLancer(
                        funcionario_data["Código"],
                        funcionario_data["Nome"],
                        funcionario_data["Dias Trabalhados"],
                        funcionario_data["Valor Dia"]
                    )
                else:
                    # Criar instância de Vendedor com os dados atuais
                    funcionario = Vendedor(
                        funcionario_data["Código"],
                        funcionario_data["Nome"],
                        funcionario_data["Salário Base"],
                        funcionario_data["Comissão"]
                    )

                with st.form(key="alteraFuncionario"):
                    # Usar setters para atualizar os valores
                    st.write(f"Tipo: {funcionario_data['Tipo']}")
                    funcionario.set_codigo(st.number_input("Código: ", min_value=0, value=funcionario.get_codigo()))
                    funcionario.set_nome(st.text_input("Nome: ", value=funcionario.get_nome()))

                    if funcionario_data["Tipo"] == "FreeLancer":
                        funcionario.set_diasTrabalhados(st.number_input("Dias trabalhados: ", 
                                                                      min_value=0, 
                                                                      value=funcionario.get_diasTrabalhados()))
                        funcionario.set_valorDia(st.number_input("Valor por dia: ", 
                                                               min_value=0.0, 
                                                               format="%.2f", 
                                                               value=funcionario.get_valorDia()))
                    else:
                        funcionario.set_salarioBase(st.number_input("Salário base: ", 
                                                                  min_value=0.0, 
                                                                  format="%.2f", 
                                                                  value=funcionario.get_salarioBase()))
                        funcionario.set_comissao(st.number_input("Comissão: ", 
                                                               min_value=0.0, 
                                                               format="%.2f", 
                                                               value=funcionario.get_comissao()))

                    # Mostrar salário calculado
                    salario = funcionario.calcularSalario()
                    st.write(f"Salário Calculado: R$ {salario:.2f}")

                    if st.form_submit_button("Confirmar Alterações"):
                        try:
                            # Preparar dados para atualização
                            dados_atualizados = {
                                "Código": funcionario.get_codigo(),
                                "Nome": funcionario.get_nome(),
                                "Tipo": funcionario_data["Tipo"],
                                "Dias Trabalhados": funcionario.get_diasTrabalhados() if hasattr(funcionario, 'get_diasTrabalhados') else None,
                                "Valor Dia": funcionario.get_valorDia() if hasattr(funcionario, 'get_valorDia') else None,
                                "Salário Base": funcionario.get_salarioBase() if hasattr(funcionario, 'get_salarioBase') else None,
                                "Comissão": funcionario.get_comissao() if hasattr(funcionario, 'get_comissao') else None
                            }
                            
                            funcionarioController.alterarFuncionario(dados_atualizados)
                            st.success("Funcionário alterado com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao alterar funcionário: {e}")
            else:
                st.error("Funcionário não encontrado.")
        else:
            st.info("Nenhum funcionário cadastrado.")