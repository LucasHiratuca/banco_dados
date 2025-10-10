# services/database.py 
import sqlite3 
 
server = ''
username = ''
password = ''
database = 'empresa.db'
conexao = sqlite3.connect(database)
print("Banco de dados da empresa criado com sucesso")
 