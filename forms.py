from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Ingresar')

class ProfileEditForm(FlaskForm):
    nombre_publico = StringField('Nombre público', validators=[DataRequired(), Length(max=120)])
    profile_image = FileField('Foto de perfil', validators=[FileAllowed(['png','jpg','jpeg','gif'], 'Solo imágenes')])
    submit = SubmitField('Guardar')

#EXPERIENCIAAA
class AddExperienciaForm(FlaskForm):
    proyecto = StringField('Proyecto', validators=[DataRequired(), Length(max=200)])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(max=500)])
    puesto = StringField('Puesto', validators=[DataRequired(), Length(max=150)])
    periodo = StringField('Periodo', validators=[DataRequired(), Length(max=150)])
    logros = StringField('Logros', validators=[Length(max=500)])
    submit = SubmitField('Agregar')

class EditExperienciaForm(FlaskForm):
    proyecto = StringField('Proyecto', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])
    puesto = StringField('Puesto', validators=[DataRequired()])
    periodo = StringField('Periodo', validators=[DataRequired()])
    logros = StringField('Logros')
    submit = SubmitField('Guardar cambios')

class DeleteExperienciaForm(FlaskForm):
    submit = SubmitField('Eliminar') 


class EducacionForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    institucion = StringField("Institución", validators=[DataRequired()])
    periodo = StringField("Periodo")
    estado = StringField("Estado")

    logo = FileField("Logo de la institución", validators=[
        FileAllowed(['png', 'jpg', 'jpeg'])
    ])

    submit = SubmitField("Agregar")
    
class EditarEducacionForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    institucion = StringField("Institución", validators=[DataRequired()])
    periodo = StringField("Periodo")
    estado = StringField("Estado")
    logo = FileField("Logo", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Guardar cambios")

class EliminarEducacionForm(FlaskForm):
    submit = SubmitField("Eliminar")

class CursoForm(FlaskForm):
    nombre = StringField("Nombre del curso", validators=[DataRequired()])
    institucion = StringField("Institución", validators=[DataRequired()])
    periodo = StringField("Periodo")
    certificacion_url = StringField("URL del certificado")
    submit = SubmitField("Agregar")
    

class EditarCursoForm(FlaskForm):
    nombre = StringField("Nombre del curso", validators=[DataRequired()])
    institucion = StringField("Institución", validators=[DataRequired()])
    periodo = StringField("Periodo")
    submit = SubmitField("Guardar cambios")


class EliminarCursoForm(FlaskForm):
    submit = SubmitField("Eliminar")

class ProyectoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    descripcion = StringField("Descripción") 
    fecha = StringField("Fecha")
    github_url = StringField("GitHub", validators=[DataRequired()])
    imagen = FileField("Imagen del proyecto", validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Guardar")