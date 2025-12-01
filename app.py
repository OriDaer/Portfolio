import os
from flask import (
    Flask, render_template, redirect, url_for,
    request, flash, session, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from functools import wraps

from forms import (LoginForm, ProfileEditForm,DeleteExperienciaForm,
    AddExperienciaForm,EditExperienciaForm,EducacionForm, 
    EditarEducacionForm,EliminarEducacionForm,CursoForm,
    EditarCursoForm,EliminarCursoForm,ProyectoForm
    )
from models import db, Usuario, Experiencia, Educacion, Curso,Proyecto
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

@app.route('/descargar-cv')
def descargar_cv():
    # Ajusta el nombre y la ubicación exacta de tu PDF
    cv_path = os.path.join(app.root_path, 'static/uploads')
    return send_from_directory(cv_path, 'CV_Daer_Oriana_Berenice.pdf', as_attachment=True)

@app.route('/')
def index():
    usuario = Usuario.query.filter_by(username="daer").first()
    educacion = Educacion.query.filter_by(usuario_id=usuario.id).all()
    cursos = Curso.query.filter_by(usuario_id=usuario.id).all()
    educacion = Educacion.query.filter_by(usuario_id=usuario.id).all()
    edit_form = EditExperienciaForm()
    form=EducacionForm()
    form_editar = EditarEducacionForm()
    form_eliminar = EliminarEducacionForm()
    experiencias = Experiencia.query.all()
    add_form = AddExperienciaForm()
    delete_forms = {exp.id: DeleteExperienciaForm() for exp in experiencias}
    form_elim_curso= EliminarCursoForm()
    form_modif_curso = EditarCursoForm()
    form_curso=CursoForm()
    proyectos= Proyecto.query.all()
    form_proyect= ProyectoForm()
    form_modif_proyect=ProyectoForm()
    form_eliminar_proyecto=ProyectoForm()

    return render_template('index.html', usuario=usuario , experiencias=experiencias,add_form=add_form,edit_form=edit_form,
    delete_forms=delete_forms, form=form,form_eliminar=form_eliminar,
    form_editar=form_editar,educacion=educacion,
    cursos=cursos,form_elim_curso=form_elim_curso,
    form_curso=form_curso,form_modif_curso=form_modif_curso,
    form_proyect=form_proyect,proyectos=proyectos,
    form_modif_proyect=form_modif_proyect,form_eliminar_proyecto=form_eliminar_proyecto
    )


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



@app.route('/agregar_experiencia', methods=['POST'])
@login_required
def agregar_experiencia():
    form = AddExperienciaForm()
    if form.validate_on_submit():
        nueva = Experiencia(
            proyecto=form.proyecto.data,
            descripcion=form.descripcion.data,
            puesto=form.puesto.data,
            periodo=form.periodo.data,
            logros=form.logros.data
        )
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/modificar_experiencia/<int:exp_id>', methods=['POST'])
def modificar_experiencia(exp_id):
    exp = Experiencia.query.get_or_404(exp_id)

    exp.proyecto = request.form['proyecto']
    exp.puesto = request.form['puesto']
    exp.periodo = request.form['periodo']
    exp.descripcion = request.form['descripcion']
    exp.logros = request.form['logros']

    db.session.commit()
    flash("Experiencia modificada correctamente", "success")

    return redirect(url_for('index'))


@app.route('/eliminar_experiencia/<int:exp_id>', methods=['POST'])
@login_required
def eliminar_experiencia(exp_id):
    form=DeleteExperienciaForm()

    if not form.validate_on_submit(): #confirma q el post viene dese el formulario propio del lugar
        flash('solicitud invalida',"danger")
        return redirect(url_for('index'))
    
    #busca experiencia
    exp=Experiencia.query.get_or_404(exp_id) #si el id no existe, con el get on 404 se cortaria

    # Eliminar experienia
    db.session.delete(exp)
    db.session.commit()
    flash("Experiencia eliminada", "info")
    return redirect(url_for('index'))



#-----------EDUCACION ROUTES  ----------------

@app.route("/agregar_educacion", methods=["POST"])
@login_required
def agregar_educacion():
    form = EducacionForm()

    if not form.validate_on_submit():
        flash("Error en el formulario de educación.", "danger")
        return redirect(url_for("index"))

    usuario = Usuario.query.filter_by(username=session['user']).first()

    # Procesar archivo
    filename = None
    if form.logo.data:
        file = form.logo.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    # Guardar en DB
    nueva = Educacion(
        usuario_id=usuario.id,
        titulo=form.titulo.data,
        institucion=form.institucion.data,
        periodo=form.periodo.data,
        estado=form.estado.data,
        logo=filename
    )

    db.session.add(nueva)
    db.session.commit()

    flash("Formación agregada correctamente.", "success")
    return redirect(url_for("index"))

@app.route("/educacion/eliminar/<int:edu_id>", methods=["POST"])
def eliminar_educacion(edu_id):
    form = EliminarEducacionForm()
    if form.validate_on_submit():
        edu = Educacion.query.get_or_404(edu_id)
        db.session.delete(edu)
        db.session.commit()
    return redirect(url_for("index"))

@app.route('/modificar_educacion/<int:edu_id>', methods=['POST'])
@login_required
def modificar_educacion(edu_id):
    edu = Educacion.query.get_or_404(edu_id)

    form = EducacionForm()

    if form.validate_on_submit():
        edu.titulo = form.titulo.data
        edu.institucion = form.institucion.data
        edu.periodo = form.periodo.data
        edu.estado = form.estado.data

        # Si sube un nuevo logo, lo reemplaza
        if form.logo.data:
            file = form.logo.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            edu.logo = filename

        db.session.commit()
        flash("Formación modificada correctamente.", "success")

    return redirect(url_for("index"))


#---------------CURSOS SECCIONNN------------------
@app.route('/agregar_curso', methods=['POST'])
@login_required
def agregar_curso():
    form_curso= CursoForm()

    if not form_curso.validate_on_submit():
        flash("Error en el formulario del curso.", "danger")
        return redirect(url_for("dashboard"))

    usuario = Usuario.query.filter_by(username=session['user']).first()

    nuevo = Curso(
        usuario_id=usuario.id,
        nombre=form_curso.nombre.data,
        institucion=form_curso.institucion.data,
        periodo=form_curso.periodo.data,
        certificacion_url=form_curso.certificacion_url.data
    )

    db.session.add(nuevo)
    db.session.commit()

    flash("Curso agregado correctamente.", "success")
    return redirect(url_for('index'))

@app.route('/eliminar_curso/<int:curso_id>', methods=['POST'])
@login_required
def eliminar_curso(curso_id):
    form_elim_curso = EliminarCursoForm()
    
    if form_elim_curso.validate_on_submit():
        curso = Curso.query.get_or_404(curso_id)
        db.session.delete(curso)
        db.session.commit()
        flash("Curso eliminado.", "info")

    return redirect(url_for('index'))

@app.route('/modificar_curso/<int:curso_id>', methods=['POST'])
@login_required
def modificar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    form_modif_curso = EditarCursoForm()

    if form_modif_curso.validate_on_submit():
        curso.nombre = form_modif_curso.nombre.data
        curso.institucion = form_modif_curso.institucion.data
        curso.periodo = form_modif_curso.periodo.data

        db.session.commit()
        flash("Curso modificado correctamente.", "success")

    return redirect(url_for("index"))


# ------------------- Proyectos -------------------
#
@app.route('/agregar_proyecto', methods=['POST'])
@login_required
def agregar_proyecto():
    form_proyect= ProyectoForm()
    if form_proyect.validate_on_submit():
        imagen_filename = None
        if form_proyect.imagen.data:
            file = form_proyect.imagen.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imagen_filename = filename

        nuevo = Proyecto(
            titulo=form_proyect.titulo.data,
            descripcion=form_proyect.descripcion.data,
            fecha=form_proyect.fecha.data,
            github_url=form_proyect.github_url.data,
            imagen=imagen_filename
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Proyecto agregado correctamente.", "success")
    return redirect(url_for('index'))


@app.route('/modificar_proyecto/<int:proy_id>', methods=['POST'])
@login_required
def modificar_proyecto(proy_id):
    proyecto = Proyecto.query.get_or_404(proy_id)
    form_modif_proyect = ProyectoForm()
    if form_modif_proyect.validate_on_submit():
        proyecto.titulo = form_modif_proyect.titulo.data
        proyecto.descripcion = form_modif_proyect.descripcion.data
        proyecto.fecha = form_modif_proyect.fecha.data
        proyecto.github_url = form_modif_proyect.github_url.data

        if form_modif_proyect.imagen.data:
            file = form_modif_proyect.imagen.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            proyecto.imagen = filename

        db.session.commit()
        flash("Proyecto modificado correctamente.", "success")
    return redirect(url_for('index'))


@app.route('/eliminar_proyecto/<int:proy_id>', methods=['POST'])
@login_required
def eliminar_proyecto(proy_id):
    proyecto = Proyecto.query.get_or_404(proy_id)
    db.session.delete(proyecto)
    db.session.commit()
    flash("Proyecto eliminado.", "info")
    return redirect(url_for('index'))


# ---------------------
# Main
# ---------------------
if __name__ == '__main__':
    inicializar_app()  # crea tablas y usuario único
    app.run(debug=True)
