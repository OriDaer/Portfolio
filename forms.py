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
