import sqlite3
from tabulate import tabulate

conexion = sqlite3.connect('users.db')
cursor = conexion.cursor()

def crear_tabla():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conexion.commit()

crear_tabla()

def insertar_usuario(username,name,password): #función para insertar usuarios para pruebas
    cursor.execute('''
        INSERT INTO users (username, name, password)
        VALUES (?, ?, ?)
    ''', (username, name, password))
    conexion.commit()

insertar_usuario('jerichodow4@gmail.com', 'Dow', '3456')

cursor.execute(f"SELECT * FROM users")
filas = cursor.fetchall()
columnas = [descripcion[0] for descripcion in cursor.description] #Coge el primer nombre de las columnas para mostrarlo como encabezados.
# Mostrar la tabla con tabulate
print(tabulate(filas, headers=columnas, tablefmt='grid'))