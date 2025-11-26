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
from models import db, Usuario, Experiencia, Educacion, Curso
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
            profile_image="daer.png"
        )
        db.session.add(user)
        db.session.commit()
        print("✅ Usuario inicial creado: daer / 123456")

# ---------------------
# Rutas
# ---------------------
@app.route('/')
def index():
    usuario = Usuario.query.filter_by(username="daer").first()
    educacion = Educacion.query.filter_by(usuario_id=usuario.id).all()
    cursos = Curso.query.filter_by(usuario_id=usuario.id).all()

    experiencias = Experiencia.query.filter_by(usuario_id=usuario.id).all()
    if 'user' in session:
        usuario = Usuario.query.filter_by(username=session['user']).first()
        experiencias = Experiencia.query.filter_by(usuario_id=usuario.id).all()

    return render_template('index.html', usuario=usuario , experiencias=experiencias, educacion=educacion, cursos=cursos)


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

    return render_template('dashboard.html', usuario=usuario, form=form, )


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/editar-acerca', methods=['POST'])
@login_required
def editar_acerca():
    usuario = Usuario.query.filter_by(username=session['user']).first()
    usuario.acerca_de_mi = request.form['acerca']
    usuario.save()
    flash("Sección actualizada", "success")
    return redirect(url_for('index'))

@app.route('/editar_experiencia', methods=['POST'])
@login_required
def editar_experiencia():
    usuario = Usuario.query.filter_by(username=session['user']).first()
    experiencias = Experiencia.query.filter_by(usuario_id=usuario.id).all()

    for exp in experiencias:
        exp.proyecto = request.form.get(f"proyecto_{exp.id}")
        exp.descripcion = request.form.get(f"descripcion_{exp.id}")
        exp.puesto = request.form.get(f"puesto_{exp.id}")
        exp.periodo = request.form.get(f"periodo_{exp.id}")
        exp.logros = request.form.get(f"logros_{exp.id}")

    db.session.commit()
    flash("Experiencia laboral actualizada exitosamente", "success")
    return redirect(url_for('index'))

@app.route('/agregar_experiencia', methods=['POST'])
@login_required
def agregar_experiencia():
    usuario = Usuario.query.filter_by(username=session['user']).first()

    nueva = Experiencia(
        proyecto=request.form['proyecto'],
        descripcion=request.form['descripcion'],
        puesto=request.form['puesto'],
        periodo=request.form['periodo'],
        logros=request.form['logros'],
        usuario_id=usuario.id
    )

    db.session.add(nueva)
    db.session.commit()
    flash("Nueva experiencia agregada", "success")
    return redirect(url_for('index'))

@app.route('/eliminar_experiencia/<int:exp_id>', methods=['POST'])
@login_required
def eliminar_experiencia(exp_id):
    exp = Experiencia.query.get(exp_id)
    if exp:
        db.session.delete(exp)
        db.session.commit()
        flash("Experiencia eliminada", "info")
    return redirect(url_for('index'))

#-----------EDUCACION ROUTES  ----------------
@app.route('/agregar_educacion', methods=['POST'])
@login_required
def agregar_educacion():
    usuario = Usuario.query.filter_by(username=session['user']).first()
    #carga logo si existe
    file= request.files.get('logo')
    filename= None
    if file and file.filename:
        filename=secure_filename(file.filename)
        path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
    edu=Educacion(
        usuario_id = usuario.id,
        titulo=request.form['titulo'],
        institucion=request.form['institucion'],
        periodo=request.form['periodo'],
        estado=request.form['estado'],
        logo=filename
    )
    db.session.add(edu)
    db.session.commit()
    flash("Nueva educación agregada", "success")
    return redirect(url_for('dashboard')) 

@app.route('/eliminar_educacion/<int:edu_id>', methods=['POST'])
@login_required
def eliminar_educacion(edu_id):
    edu = Educacion.query.get(edu_id)
    if edu:
        db.session.delete(edu)
        db.session.commit()
        flash("Educación eliminada", "info")
    return redirect(url_for('dashboard'))

@app.route('/agregar_curso', methods=['POST'])
@login_required
def agregar_curso():
    usuario = Usuario.query.filter_by(username=session['user']).first()

    curso = Curso(
        usuario_id=usuario.id,
        nombre=request.form['nombre'],
        institucion=request.form['institucion'],
        periodo=request.form['periodo'],
        certificacion_url=request.form.get('certificacion_url')
    )

    db.session.add(curso)
    db.session.commit()
    flash("Curso agregado", "success")
    return redirect(url_for('dashboard'))

@app.route('/eliminar_curso/<int:curso_id>', methods=['POST'])
@login_required
def eliminar_curso(curso_id):
    curso = Curso.query.get(curso_id)
    if curso:
        db.session.delete(curso)
        db.session.commit()
        flash("Curso eliminado", "info")
    return redirect(url_for('dashboard'))


# ---------------------
# Main
# ---------------------
if __name__ == '__main__':
    inicializar_app()  # crea tablas y usuario único
    app.run(debug=True)
