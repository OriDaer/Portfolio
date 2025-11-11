import os
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from functools import wraps

from forms import LoginForm, ProfileEditForm
from models import db, Usuario
from config import Config


# ---------------------
# Configuración inicial
# ---------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)

# Crear carpeta de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ---------------------
# Helper: requerir login
# ---------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión para acceder a esa página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------
# Inicialización automática
# ---------------------
def inicializar_app():
    """Crea tablas y usuario inicial si no existen."""
    app.app_context().push()  # activa contexto de Flask
    db.create_all()
    # si no existe el usuario principal, lo crea
    usuario_existente = Usuario.query.filter_by(username="daer").first()
    if not usuario_existente:
        hashed_pw = bcrypt.generate_password_hash("123456").decode("utf-8")
        user = Usuario(
            username="daer",
            password=hashed_pw,
            nombre_publico="Daer Oriana Berenice",
            profile_image="default_profile.png"
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Usuario inicial creado: daer / 123456")

# ---------------------
# Rutas
# ---------------------
@app.route('/')
def index():
    usuario = None
    if 'user' in session:
        usuario = Usuario.query.filter_by(username=session['user']).first()
    return render_template('index.html', usuario=usuario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(username=form.username.data).first()

        if usuario and usuario.check_password(bcrypt, form.password.data):
            session['user'] = usuario.username
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Cerraste sesión correctamente.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    usuario = Usuario.query.filter_by(username=session['user']).first()
    form = ProfileEditForm()

    if form.validate_on_submit():
        usuario.nombre_publico = form.nombre_publico.data

        file = form.profile_image.data
        if file:
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(filename)
            filename = f"{usuario.username}{ext}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            usuario.profile_image = filename

        usuario.save()
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        form.nombre_publico.data = usuario.nombre_publico

    return render_template('dashboard.html', usuario=usuario, form=form)


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ---------------------
# Main
# ---------------------
if __name__ == '__main__':
    inicializar_app()  # crea tablas y usuario único
    app.run(debug=True)
