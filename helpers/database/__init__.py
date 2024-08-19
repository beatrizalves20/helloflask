import sqlite3
from Globals import DATABASE_NAME
# Aqui era armazenar os dados especificos 
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as e:    
        print('Não foi possível conectar')

    return conn
