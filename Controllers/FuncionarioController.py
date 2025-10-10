# Controllers/FuncionarioController.py
import sqlite3
from Models.FreeLancer import FreeLancer
from Models.Vendedor import Vendedor

def conectaBD():
    conexao = sqlite3.connect("Empresa.db")
    return conexao

def incluirFuncionario(funcionario):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        if isinstance(funcionario, FreeLancer):
            cursor.execute("""
                INSERT INTO funcionario (codigo, nome, tipo, diasTrabalhados, valorDia)
                VALUES (?, ?, ?, ?, ?)
            """, (
                funcionario.get_codigo(),
                funcionario.get_nome(),
                'FreeLancer',
                funcionario.get_diasTrabalhados(),
                funcionario.get_valorDia()
            )) 
        elif isinstance(funcionario, Vendedor):
            cursor.execute("""
                INSERT INTO funcionario (codigo, nome, tipo, salarioBase, comissao)
                VALUES (?, ?, ?, ?, ?)
            """, (
                funcionario.get_codigo(),
                funcionario.get_nome(), 'Vendedor',
                funcionario.get_salarioBase(),
                funcionario.get_comissao()
            ))     
        conexao.commit()
        print("Funcionário inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir funcionário: {e}")
    finally:
        conexao.close()

def consultarFuncionario():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute('SELECT * FROM funcionario')
        rows = cursor.fetchall()
        
        # Lista para armazenar os dados dos funcionários
        dados = []
        
        for row in rows:
            codigo, nome, tipo, diasTrabalhados, valorDia, salarioBase, comissao = row
            
            if tipo == 'FreeLancer':
                funcionario = FreeLancer(codigo, nome, diasTrabalhados, valorDia)
                salario = funcionario.calcularSalario()
            elif tipo == 'Vendedor':
                funcionario = Vendedor(codigo, nome, salarioBase, comissao)
                salario = funcionario.calcularSalario()
            
            # Adiciona os dados do funcionário à lista
            dados.append({
                "Código": codigo,
                "Nome": nome,
                "Tipo": tipo,
                "Dias Trabalhados": diasTrabalhados,
                "Valor Dia": valorDia,
                "Salário Base": salarioBase,
                "Comissão": comissao,
                "Salário Calculado": salario
            })
        
        return dados
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar funcionários: {e}")
        return []
    
    finally:
        conexao.close()
    
def excluirFuncionario(codigo):
    try:
        conexao = conectaBD()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM funcionario WHERE codigo = ?", (codigo,))
        conexao.commit()
        print(f"Funcionario com codigo {codigo} excluído com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir funcionario: {e}")
    finally:
        if conexao:
            conexao.close()

def alterarFuncionario(funcionario):
    try:
        conexao = conectaBD()
        cursor = conexao.cursor()
        cursor.execute('''
            UPDATE funcionario 
            SET codigo = ?, nome = ?, tipo = ?, diasTrabalhados = ?, valorDia = ?, salarioBase = ?, comissao = ?
            WHERE codigo = ?
        ''', (
            funcionario["Código"],
            funcionario["Nome"],
            funcionario["Tipo"],
            funcionario["Dias Trabalhados"],
            funcionario["Valor Dia"],
            funcionario["Salário Base"],
            funcionario["Comissão"],
            funcionario["Código"]
        ))
        conexao.commit()
        print(f"Funcionário com código {funcionario['Código']} alterado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao alterar Funcionário: {e}")
    finally:
        if conexao:
            conexao.close()