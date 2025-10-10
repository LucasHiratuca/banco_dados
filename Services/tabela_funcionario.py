# services/tabela_funcionarios.py 
 
import sqlite3
 
conexao = sqlite3.connect("empresa.db")
 
cursor = conexao.cursor()
 
cursor.execute(
    '''
        CREATE TABLE funcionario(
            codigo INTEGER PRIMARY KEY
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            diasTrabalhados INTEGER,
            valorDia REAL,
            salarioBase REAL,
            comissao REAL 
        );
    '''
)
cursor.close()
print("Tabela FUNCIONÁRIO criada com sucesso")
 