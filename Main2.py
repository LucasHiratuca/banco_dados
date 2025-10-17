# main.py
import streamlit as st
import sys
from pathlib import Path
import importlib

# 1. Configuração ABSOLUTA PRIMEIRO
st.set_page_config(page_title="Sistema de Cadastro", layout="wide", initial_sidebar_state="auto")

# 2. Configuração de imports DEPOIS da configuração
sys.path.append(str(Path(__file__).parent))

# 3. Dicionário de páginas disponíveis
PAGES = { "Funcionário": "Views.PageFuncionario", "Produto": "Views.PageProduto", "Vendas": "Views.PageVenda"}

# 4. Função para carregar páginas de forma dinâmica
def load_page(page_name):
    """Carrega um módulo de página dinamicamente com tratamento de erros"""
    try:
        module = importlib.import_module(PAGES[page_name])
        # Remove acentos e formata o nome da função corretamentepython 
        page_name_clean = page_name.lower().replace("á", "a").replace("é", "e")
        return getattr(module, f"show_{page_name_clean}_page")
    except (ImportError, AttributeError, KeyError) as e:
        st.error(f"Erro ao carregar a página {page_name}: {e}")
        st.warning("Entre em contato com o administrador do sistema.")
        return None

# 5. Função principal
def main():
    st.title('Sistema de Cadastro de Vendas')
    
    with st.sidebar:
        st.title("Menu")
        page_selection = st.selectbox("Selecione uma opção", list(PAGES.keys()))
    
    # Carrega a página selecionada
    show_page = load_page(page_selection)
    if show_page: show_page()

# 6. Ponto de entrada
if __name__ == "__main__":
    main()