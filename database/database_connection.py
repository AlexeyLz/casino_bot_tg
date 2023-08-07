import sqlite3

connection = sqlite3.connect('casino.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id BIGINT, username TEXT, balance REAL)')
cursor.close()
