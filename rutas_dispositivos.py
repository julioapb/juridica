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


    return render_template('vista_dispositivos.html')




