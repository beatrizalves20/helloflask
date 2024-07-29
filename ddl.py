import sqlite3

connection = sqlite3.connect('controleestoque.db')

with open('schema.sql') as f:
    connection.executescript(f.read())


connection.close()