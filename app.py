from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Cambia esto si es necesario
    password="",  # Cambia esto si es necesario
    database="juridica"
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')  # Convertir a bytes

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            # Verificar la contraseña hasheada
            if bcrypt.checkpw(password, user[2].encode('utf-8')):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        # Hashear la contraseña
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        cedula = request.form['cedula']
        tipo_usuario = request.form['tipo_usuario']

        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password, cedula, nombre, fecha, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s)", (username, hashed_password, cedula, nombre, fecha, tipo_usuario))
        db.commit()

        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)