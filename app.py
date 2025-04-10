from flask import Flask 
from auth_routes import auth_bp  
from rutas_empleados import empleados
from rutas_dispositivos import dispositivos

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura'  # Necesario para manejar sesiones

# Registrar el Blueprint con un prefijo (opcional)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(empleados, url_prefix = '/empleados')
app.register_blueprint(dispositivos, url_prefix = '/dispositivos')

if __name__ == '__main__':
    app.run(debug=True)