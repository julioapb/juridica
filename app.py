from flask import Flask # type: ignore
from auth_routes import auth_bp  # Importar el Blueprint

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura'  # Necesario para manejar sesiones

# Registrar el Blueprint con un prefijo (opcional)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)