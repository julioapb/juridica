from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, g 
import mysql.connector
import mysql.connector.cursor 


#blueprint
empleados = Blueprint('empleados', __name__)

# Configuración de la base de datos
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="juridica"
        )
    return g.db

@empleados.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@empleados.route('/nuevoEmpleado')
def nuevoEmpleado():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cargo")
    cargos = cursor.fetchall()

    cursor.execute("SELECT * FROM departamento")
    departamentos = cursor.fetchall()
    
    cursor.close()

    return render_template('vista_empleados.html', cargos = cargos, departamentos = departamentos, username=username)


@empleados.route('/guardarEmpleado', methods=['POST'])
def guardarEmpleado():

    nombre = request.form['nombre'].upper()
    correo = request.form['correo']
    cargo_id = request.form['cargo']
    departamento_id = request.form['departamento']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM empleado WHERE correo = %s", (correo,))
    empleado_existente = cursor.fetchone()

    if empleado_existente:
        flash('El correo ya está registrado', 'danger')
        cursor.close()
        return redirect(url_for('empleados.nuevoEmpleado'))


    cursor.execute("""
        INSERT INTO empleado(nombre, correo, id_cargo, id_departamento)
        VALUES (%s, %s, %s, %s)
    """,(nombre, correo, cargo_id, departamento_id)
    )

    db.commit()
    cursor.close()
    flash('✅ Empleado registrado correctamente.', 'success')
    return redirect(url_for('empleados.nuevoEmpleado'))


