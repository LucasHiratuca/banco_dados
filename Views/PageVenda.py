# Views/PageVenda.py
import streamlit as st
import pandas as pd
from datetime import datetime
from Controllers.VendaController import (
    incluir_venda,
    consultar_vendas,
    excluir_venda
)
from Controllers.FuncionarioController import consultarFuncionario
from Controllers.ProdutoController import consultar_produtos
from Models.Venda import Venda

def show_vendas_page():
    st.title('📊 Sistema de Vendas')
    
    # Menu de operações
    operacao = st.sidebar.selectbox(
        "Operações", 
        ["Registrar Venda", "Consultar Vendas", "Excluir Venda"]
    )

    if operacao == "Registrar Venda":
        st.header("Nova Venda")
        st.markdown("---")
        
        # Carrega dados necessários
        funcionarios = consultarFuncionario()
        produtos = consultar_produtos()
        
        if not funcionarios or not produtos:
            st.warning("⚠️ Cadastre funcionários e produtos antes de registrar vendas!")
            return

        # Formulário de venda
        with st.form(key='form_venda', clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                # Seleciona funcionário
                funcionario_options = {f["Código"]: f"{f['Nome']} ({f['Tipo']})" 
                                      for f in funcionarios}
                selected_func = st.selectbox(
                    "Funcionário*:",
                    options=list(funcionario_options.keys()),
                    format_func=lambda x: funcionario_options[x]
                )
                
                # Seleciona produto
                produto_options = {p[0]: f"{p[1]} (Estoque: {p[2]} | R$ {p[3]:.2f})" 
                                       for p in produtos}
                selected_prod = st.selectbox(
                    "Produto*:",
                    options=list(produto_options.keys()),
                    format_func=lambda x: produto_options[x]
                )
                
            with col2:
                # Obtém dados do produto selecionado
                produto_selecionado = next(p for p in produtos if p[0] == selected_prod)
                estoque_atual = produto_selecionado[2]
                valor_unitario = produto_selecionado[3]
                
                # Quantidade
                qtd = st.number_input(
                    "Quantidade*:", 
                    min_value=1, 
                    max_value=estoque_atual,
                    value=1
                )
                
                # Data da venda
                data_venda = st.date_input(
                    "Data da Venda:", 
                    value=datetime.now() )
            
            # Calcula totais
            valor_total = qtd * valor_unitario
            
            # Exibe resumo
            st.markdown("---")
            st.subheader("Resumo da Venda")
            
            cols_resumo = st.columns(3)
            cols_resumo[0].metric("Valor Unitário", f"R$ {valor_unitario:.2f}")
            cols_resumo[1].metric("Quantidade", qtd)
            cols_resumo[2].metric("Valor Total", f"R$ {valor_total:.2f}", delta_color="off")
            
            # Botão de submissão
            if st.form_submit_button("✅ Registrar Venda"):
                try:
                    # Cria objeto venda
                    nova_venda = Venda(
                        codigo=0,
                        data_venda=data_venda.strftime("%Y-%m-%d"),
                        codigo_funcionario=selected_func,
                        codigo_produto=selected_prod,
                        qtd=qtd )
                    
                    # Insere no banco
                    if incluir_venda(nova_venda):
                        st.success("Venda registrada com sucesso!")
                        st.balloons()
                    else:
                        st.error("Erro ao registrar venda")
                        
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

    elif operacao == "Consultar Vendas":
        st.header("Histórico de Vendas")
        st.markdown("---")
        
        # Filtros
        with st.expander("🔍 Filtros", expanded=True):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                data_inicio = st.date_input("Data Início", value=datetime.now().replace(day=1))
            
            with col_f2:
                data_fim = st.date_input("Data Fim", value=datetime.now())
        
        if st.button("🔎 Consultar", key="btn_consultar"):
            with st.spinner("Buscando vendas..."):
                vendas = consultar_vendas()
                
                if vendas:
                    # Filtra por data com tratamento de erro
                    vendas_filtradas = []
                    for v in vendas:
                        try:
                            data_venda = datetime.strptime(v[1], "%Y-%m-%d").date()
                            if data_inicio <= data_venda <= data_fim:
                                vendas_filtradas.append(v)
                        except ValueError as e:
                            st.error(f"Erro ao processar data da venda {v[0]}: Formato inválido")
                            continue
                        except Exception as e:
                            st.error(f"Erro ao processar venda {v[0]}: {str(e)}")
                            continue
                    
                    if vendas_filtradas:
                        # Cria DataFrame
                        df = pd.DataFrame(
                            vendas_filtradas,
                            columns=[
                                "Código", "Data", "Cód. Func.", "Funcionário", 
                                "Cód. Prod.", "Produto", "Qtd", "Vl. Unit.", "Total"
                            ] )
                        
                        # Formatação
                        df["Vl. Unit."] = df["Vl. Unit."].apply(lambda x: f"R$ {float(x):.2f}")
                        df["Total"] = df["Total"].apply(lambda x: f"R$ {float(x):.2f}")
                        
                        # Exibe tabela
                        st.dataframe(
                            df,
                            height=500,
                            column_config={
                                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY")
                            },
                            use_container_width=True )
                        
                        # Exibe totais
                        total_vendas = sum(float(v[8]) for v in vendas_filtradas)
                        st.metric("Total no Período", f"R$ {total_vendas:,.2f}")
                        
                    else:
                        st.warning("Nenhuma venda encontrada no período selecionado")
                else:
                    st.warning("Nenhuma venda registrada ainda")

    elif operacao == "Excluir Venda":
        st.header("Excluir Venda")
        st.markdown("---")
        
        with st.spinner("Carregando vendas..."):
            vendas = consultar_vendas()
            
            if vendas:
                # Seleciona venda para exclusão
                venda_options = {
                    v[0]: f"Venda #{v[0]} - {v[1]} | {v[3]} | {v[5]} | R$ {float(v[8]):.2f}"
                    for v in vendas }
                
                selected_venda = st.selectbox(
                    "Selecione a venda para excluir:",
                    options=list(venda_options.keys()),
                    format_func=lambda x: venda_options[x] )
                
                # Confirmação
                if st.button("🗑️ Excluir Venda", type="primary"):
                    with st.spinner("Excluindo..."):
                        try:
                            if excluir_venda(int(selected_venda)):
                                st.success("Venda excluída com sucesso!")
                                st.rerun()
                            else:
                                st.error("Falha ao excluir venda (registro não encontrado)")
                        except ValueError:
                            st.error("Código de venda inválido")
                        except Exception as e:
                            st.error(f"Erro ao excluir: {str(e)}")
            else:
                st.warning("Nenhuma venda disponível para exclusão")