from flask import Flask,render_template,request,redirect,url_for
import os #Para acceder a los directorios de manera fácil y sencilla
import sqlite3

#acceder al archivo index para que sea lanzado a través de un puerto de nuestro servidor
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #indicamos el nombre del directorio
template_dir = os.path.join(template_dir,'src','templates') #unir src y templates a la carpeta del proyecto

#incializar la aplicación de Flask
app = Flask(__name__,template_folder=template_dir) #Con ello podemos rendereizar (archivo index.html) para que se muestre en el navegador

#Rutas de la aplicación
@app.route('/')
def home():
    conexion = sqlite3.connect('users.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM users")
    miresultado = cursor.fetchall()
    #Convertimos esos datos a un diccionario para poder manipularlos mejor en el front-end
    insertar_objeto = []
    columnNames = [column[0] for column in cursor.description] #accedemos a la descripcion de nombres de columnas
    for record in miresultado:
        insertar_objeto.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html',data=insertar_objeto)

#Ruta para agregar un usuario en la base de datos
@app.route('/user',methods=['POST'])
def add_user():
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]

    if username and name and password:
        conexion = sqlite3.connect('users.db')
        cursor = conexion.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (?, ?, ?)"
        data = (username, name, password)
        cursor.execute(sql, data)
        conexion.commit()
    
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete_user(id):
    conexion = sqlite3.connect('users.db')
    cursor = conexion.cursor()
    sql = "DELETE FROM users WHERE id = ?"
    data = (id,)
    cursor.execute(sql, data)
    conexion.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>',methods=['POST'])
def edit_user(id):
    username = request.form["username"]
    name = request.form["name"]
    password = request.form["password"]

    if username and name and password:
        conexion = sqlite3.connect('users.db')
        cursor = conexion.cursor()
        sql = "UPDATE users SET username = ?, name = ?, password = ? WHERE id = ?"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        conexion.commit()
    
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)