from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, g # type: ignore
import mysql.connector 
from mysql.connector import Error 
import bcrypt 
# Crear un Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

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

@auth_bp.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@auth_bp.route('/')
def home():
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '').encode('utf-8')

        if not username or not password:
            flash('Usuario y contraseña son obligatorios.', 'error')
            return redirect(url_for('auth.login'))

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
                session['username'] = username
                return redirect(url_for('auth.dashboard'))
            else:
                flash('Usuario o contraseña incorrectos.', 'error')
        except Error as e:
            flash('Error en la base de datos. Inténtalo de nuevo.', 'error')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '').encode('utf-8')
        nombre = request.form.get('nombre')
        fecha = request.form.get('fecha')
        cedula = request.form.get('cedula')
        tipo_usuario = request.form.get('tipo_usuario')

        if not all([username, password, nombre, fecha, cedula, tipo_usuario]):
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('auth.register'))

        try:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, cedula, nombre, fecha, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, hashed_password, cedula, nombre, fecha, tipo_usuario)
            )
            db.commit()
            cursor.close()
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Error as e:
            flash('Error en la base de datos. Inténtalo de nuevo.', 'error')

    return render_template('register.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))