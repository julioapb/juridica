from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, g 
import mysql.connector
import mysql.connector.cursor 


#blueprint
dispositivos = Blueprint('dispositivos', __name__)

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

@dispositivos.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@dispositivos.route('/nuevoDispositivo')
def nuevoDispositivo():
    
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tipo_dispositivo ORDER BY dispositivo ASC")
    tipo_dispositivos = cursor.fetchall()

    cursor.execute("SELECT * FROM estado_dispositivo ORDER BY estado ASC")
    estados_dispositivo = cursor.fetchall()

    cursor.execute("SELECT * FROM estado_asignacion ORDER BY estado ASC")
    estados_asignacion = cursor.fetchall()

    return render_template('vista_dispositivos.html', username = username, tipo_dispositivos = tipo_dispositivos, estados_dispositivo = estados_dispositivo, estados_asignacion = estados_asignacion)


@dispositivos.route('/guardarDispositivo', methods = ['POST'])
def guardarDsipositivo():

    tipo_dispositivo = request.form['tipo_dispositivo'].upper()
    no_serie = request.form['no_serie']
    marca = request.form['marca'].upper()
    modelo = request.form['modelo'].upper()
    color = request.form['color'].upper()
    disco = request.form['disco']
    ram = request.form['ram']
    procesador = request.form['procesador'].upper()
    sistema_operativo = request.form['sistema_operativo'].upper()
    fecha_ingreso = request.form['fecha_ingreso']
    estado_asignacion = request.form['estado_asignacion']
    estado_dispositivo = request.form['id_estado_dispositivo']

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM dispositivo WHERE no_serie = %s", (no_serie,))
    dispositivo_existente = cursor.fetchone()

    if dispositivo_existente:
        flash('El dispositivo ya está registrado', 'danger')
        cursor.close()
        return redirect(url_for('dispositivos.nuevoDispositivo'))
    
    cursor.execute("""
        INSERT INTO dispositivo(no_serie, marca, id_tipo_dispositivo, modelo, color, disco, ram, procesador, sistema_operativo, fecha_ingreso, 
                   id_estado_dispositivo, id_estado_asignacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,(no_serie, marca, tipo_dispositivo, modelo, color, disco, ram, procesador, sistema_operativo, fecha_ingreso, estado_dispositivo, estado_asignacion  )
    )

    db.commit()
    cursor.close()
    flash('✅ Dsipositivo registrado correctamente.', 'success')
    return redirect(url_for('dispositivos.nuevoDsipositivo'))

