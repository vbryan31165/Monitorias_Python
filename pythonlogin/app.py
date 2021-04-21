# app.py
from typing import Final
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flaskext.mysql import MySQL
import pymysql
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'cairocoders-ednalan'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'proyecto'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# http://localhost:5000/pythonlogin/ - this will be the login page


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Usuario' in request.form and 'password' in request.form:
        # Create variables for easy access
        Usuario = request.form['Usuario']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM usuarios us INNER JOIN roles r ON (r.ID_ROL = us.ID_ROL) WHERE us.Estado=1 AND us.Usuario = %s AND us.Contraseña = %s', (Usuario, password))
        # Fetch one record and return result
        account = cursor.fetchone()
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['ID_USUARIO']
            session['Usuario'] = account['Usuario']
            session['ID_ROL'] = account['ID_ROL']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Cedula' in request.form and 'Nombres' in request.form and 'Apellidos' in request.form and 'Telefono' in request.form and 'Usuario' in request.form and 'password' in request.form and 'Correo' in request.form:
        # Create variables for easy
        Cedula = request.form['Cedula']
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        Correo = request.form['Correo']
        Telefono = request.form['Telefono']
        Usuario = request.form['Usuario']
        password = request.form['password']
        Select_Rol = request.form.get('Perfil')
  # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM usuarios WHERE Estado=1 AND Usuario = %s', (Usuario))
        account = cursor.fetchone()

        # If account exists show error and validation checks

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Correo):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', Usuario):
            msg = 'Username must contain only characters and numbers!'
        elif not Usuario or not password or not Correo:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO usuarios VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s,NULL)',
                           (Cedula, Nombres, Apellidos, Correo, Telefono, Usuario, password, Select_Rol, 1))
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:

        # User is loggedin show them the home page
        return render_template('home.html', Usuario=session['Usuario'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('Usuario', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users


@app.route('/profile')
def profile():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT * FROM usuarios us INNER JOIN roles rol on (rol.ID_ROL=us.ID_ROL) WHERE us.Estado=1 AND us.ID_USUARIO = %s', [session['id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR USUARIOS----------------------------------###


@app.route('/Consulta_Usuario')
def Consulta_Usuario():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT us.ID_USUARIO, us.Cedula, CONCAT(us.Nombres, " ", us.Apellidos) AS Nombres, us.Correo,us.Telefono,rol.Rol,us.Usuario FROM usuarios us INNER JOIN roles rol ON (rol.ID_ROL=us.ID_ROL) WHERE us.Estado=1 AND Rol.Estado=1 ')

        data = cursor.fetchall()
        cursor.close()
    # Show the profile page with account info
    return render_template('Consulta_Usuario.html', employee=data)

    # User is not loggedin redirect to login page
    """ return redirect(url_for('Consulta_Usuario')) """


@app.route('/add_contact', methods=['POST'])
def add_employee():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Cedula = request.form['Cedula']
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        Correo = request.form['Correo']
        Telefono = request.form['Telefono']
        Usuario = request.form['Usuario']
        Contraseña = request.form['password']
        Select_Rol = request.form.get('Perfil')

        cur.execute(
            "INSERT INTO usuarios (Cedula, Nombres, Apellidos,Correo,Telefono,Usuario,Contraseña,ID_ROL,Estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Cedula, Nombres, Apellidos, Correo, Telefono, Usuario, Contraseña, Select_Rol, 1))
        conn.commit()
        flash('Employee Added successfully')
        return redirect(url_for('Consulta_Usuario'))


@app.route('/update/<id>', methods=['POST'])
def update_employee(id):
    if request.method == 'POST':
        Cedula = request.form['Cedula']
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        Correo = request.form['Correo']
        Telefono = request.form['Telefono']
        Usuario = request.form['Usuario']
        Contraseña = request.form['password']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""UPDATE usuarios SET Cedula = %s, Nombres = %s, Apellidos = %s,Correo = %s,Telefono = %s,Usuario = %s, Contraseña = %s WHERE ID_USUARIO = %s""",
                    (Cedula, Nombres, Apellidos, Correo, Telefono, Usuario, Contraseña, id))
        flash('Usuario editado correctamente')
        conn.commit()
        return redirect(url_for('Consulta_Usuario'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'SELECT * FROM usuarios WHERE Estado=1 AND ID_USUARIO = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', employee=data[0])


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'UPDATE usuarios SET Estado=2 WHERE ID_USUARIO = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Consulta_Usuario'))

###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR USUARIOS----------------------------------###


###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR MODULOS----------------------------------###

@app.route('/Agregar_Modulos')
def Agregar_Modulos():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT * FROM asignatura WHERE Estado=1')

        data = cursor.fetchall()
        cursor.close()
    # Show the profile page with account info
    return render_template('Agregar_Modulos.html', employee=data)


@app.route('/add_Modulo', methods=['POST'])
def add_Modulo():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        Asignatura = request.form['Asignatura']
        cur.execute(
            "INSERT INTO asignatura (Asignatura,Estado) VALUES (%s,%s)", (Asignatura, 1))
        conn.commit()
        flash('Employee Added successfully')
        return redirect(url_for('Agregar_Modulos'))


@app.route('/update_Modulo/<id>', methods=['POST'])
def update_Modulo(id):
    if request.method == 'POST':
        Asignatura = request.form['Asignatura']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""UPDATE asignatura SET Asignatura = %s WHERE ID_ASIGNATURA = %s""",
                    (Asignatura, id))
        flash('Modulo editado correctamente')
        conn.commit()
        return redirect(url_for('Agregar_Modulos'))


@app.route('/edit_Modulo/<id>', methods=['POST', 'GET'])
def get_Modulo(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'SELECT * FROM Asignatura WHERE Estado=1 and ID_ASIGNATURA = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_Modulo.html', employee_Modulo=data[0])


@app.route('/delete_Modulo/<string:id>', methods=['POST', 'GET'])
def delete_Modulo(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'UPDATE asignatura SET Estado=2 WHERE ID_ASIGNATURA = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Agregar_Modulos'))


###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR MODULOS----------------------------------###

###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR DISPONIBILIDAD ASESOR----------------------------------###

@app.route('/Agregar_Disponibilidad')
def Agregar_Disponibilidad():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT dis.ID,dis.Hora_Inicial, dis.Hora_Final, us.Nombres AS Asesor FROM disponibilidad_asesor dis INNER JOIN usuarios us ON (us.ID_USUARIO=dis.ID_USUARIO) WHERE dis.Estado=1')

        data = cursor.fetchall()
        cursor.close()
    # Show the profile page with account info
    return render_template('Agregar_Disponibilidad.html', employee=data)


@app.route('/add_Disponibilidad', methods=['POST'])
def add_Disponibilidad():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        ID_USUARIO = session['id']
        Hora_Inicio = request.form['Hora_Inicio']
        Hora_Final = request.form['Hora_Final']

        cur.execute(
            "INSERT INTO disponibilidad_asesor (ID_USUARIO,Hora_Inicial,Hora_Final,Estado) VALUES (%s,%s,%s,%s)", (ID_USUARIO, Hora_Inicio, Hora_Final, 1))
        conn.commit()
        flash('Employee Added successfully')
        return redirect(url_for('Agregar_Disponibilidad'))


@app.route('/update__Disponibilidad/<id>', methods=['POST'])
def update__Disponibilidad(id):
    if request.method == 'POST':
        Asignatura = request.form['Asignatura']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""UPDATE asignatura SET Asignatura = %s WHERE ID_ASIGNATURA = %s""",
                    (Asignatura, id))
        flash('Modulo editado correctamente')
        conn.commit()
        return redirect(url_for('Agregar_Disponibilidad'))


@app.route('/edit_Disponibilidad/<id>', methods=['POST', 'GET'])
def get_Disponibilidad(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'SELECT * FROM disponibilidad_asesor WHERE Estado=1 and ID = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_Disponibilidad.html', employee_Disponibilidad=data[0])


@app.route('/delete_Disponibilidad/<string:id>', methods=['POST', 'GET'])
def delete_Disponibilidad(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        'UPDATE disponibilidad_asesor SET Estado=2 WHERE ID = {0}'.format(id))
    conn.commit()
    flash('Employee Removed Successfully')
    return redirect(url_for('Agregar_Disponibilidad'))

###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR DISPONIBILIDAD ASESOR----------------------------------###

###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR SOLICITUDES----------------------------------###


@app.route('/Agregar_Solicitudes')
def Agregar_Solicitudes():
 # Check if account exists using MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor1 = conn.cursor(pymysql.cursors.DictCursor)
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT dis.ID,dis.Hora_Inicial, dis.Hora_Final, us.Nombres AS Asesor ,"" AS modulo FROM disponibilidad_asesor dis INNER JOIN usuarios us ON (us.ID_USUARIO=dis.ID_USUARIO) WHERE dis.Estado=1')
        data = cursor.fetchall()
        cursor.execute(
            'SELECT ID_ASIGNATURA,Asignatura FROM asignatura WHERE Estado=1')
        data1 = cursor.fetchall()
        if session['ID_ROL'] == 1:
            cursor1.execute(
                'SELECT CONCAT(ase.Nombres, " ", ase.Apellidos) AS Asesor ,Asg.Asignatura,Rl.Hora_Inicial,Rl.Hora_Final,ase.Telefono FROM relacion_usuario Rl INNER JOIN asignatura Asg ON (Asg.ID_ASIGNATURA=Rl.ID_ASIGNATURA) INNER JOIN usuarios ase ON (ase.ID_USUARIO=Rl.ID_ASESOR) INNER JOIN usuarios est ON (est.ID_USUARIO=Rl.ID_USUARIO) WHERE Rl.Estado=1')
            data2 = cursor1.fetchall()
        else:
            cursor1.execute(
                'SELECT CONCAT(ase.Nombres, " ", ase.Apellidos) AS Asesor ,Asg.Asignatura,Rl.Hora_Inicial,Rl.Hora_Final,ase.Telefono FROM relacion_usuario Rl INNER JOIN asignatura Asg ON (Asg.ID_ASIGNATURA=Rl.ID_ASIGNATURA) INNER JOIN usuarios ase ON (ase.ID_USUARIO=Rl.ID_ASESOR) INNER JOIN usuarios est ON (est.ID_USUARIO=Rl.ID_USUARIO) WHERE Rl.Estado=1 AND Rl.ID_USUARIO=%s', (session['id']))
            data2 = cursor1.fetchall()
        cursor.close()

    # Show the profile page with account info
    """ print(data1) """
    return render_template('Agregar_Solicitudes.html', employee=data, asignatura=data1, Asignacion_S=data2)


@app.route('/Asignar_Solicitud/', methods=['POST', 'GET'])
def Asignar_Solicitud():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cursor1 = conn.cursor(pymysql.cursors.DictCursor)
    cursor2 = conn.cursor(pymysql.cursors.DictCursor)
    select = request.form.get('Asignatura')
    ID_Asignacion = request.form.get('ID_Asignacion')

    cur.execute(
        'SELECT dis.ID,dis.Hora_Inicial, dis.Hora_Final, dis.ID_USUARIO AS ID_Asesor,us.Nombres AS Asesor ,"" AS modulo FROM disponibilidad_asesor dis INNER JOIN usuarios us ON (us.ID_USUARIO=dis.ID_USUARIO) WHERE dis.Estado=1 AND dis.ID= %s', (ID_Asignacion))
    data = cur.fetchall()

    print(session['id'])
    print(session['Usuario'])
    for resultado in data:
        ID_Asesor = resultado['ID_Asesor']
        Hora_Inicial = resultado['Hora_Inicial']
        Hora_Final = resultado['Hora_Final']

    cursor1.execute('INSERT INTO relacion_usuario VALUES (NULL,%s, %s, %s, %s, %s, %s)',
                    (session['id'], select, ID_Asesor, 1, Hora_Inicial, Hora_Final))

    cursor2.execute('UPDATE disponibilidad_asesor SET Estado = %s  WHERE ID=%s',
                    (2, ID_Asignacion))

    conn.commit()

    flash('Employee Removed Successfully')
    return redirect(url_for('Agregar_Solicitudes'))


###-----------------------------------------------CONSULTAR, EDITAR Y ELIMINAR SOLICITUDES----------------------------------###
if __name__ == '__main__':
    app.run(debug=True)
