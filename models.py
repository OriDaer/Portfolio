from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# -------------------------------
# POO: Herencia (Inheritance)
# Creamos una clase base que otros modelos pueden heredar.
# -------------------------------
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # POO: Abstracción (Abstraction)
    # Método que abstrae la acción de guardar en la DB
    def save(self):
        db.session.add(self)
        db.session.commit()

# -------------------------------
# POO: Encapsulación (Encapsulation)
# El modelo mantiene los datos y métodos que operan sobre ellos.
# Los atributos (columnas) están encapsulados dentro del objeto.
# -------------------------------
class Usuario(BaseModel):
    __tablename__ = 'usuario'
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed password
    nombre_publico = db.Column(db.String(120), default='Tu Nombre')
    profile_image = db.Column(db.String(255), default='default_profile.png')
    acerca_de_mi = db.Column(db.Text, default="¡Hola! Soy desarrolladora web con enfoque en front-end.")

    def check_password(self, bcrypt, plain_password):
        """Envuelve la comprobación de contraseña para encapsular la lógica."""
        return bcrypt.check_password_hash(self.password, plain_password)

    def set_profile_image(self, filename):
        """Pequeña función para actualizar imagen (encapsula validaciones si agregas)."""
        self.profile_image = filename
        self.save()

# -------------------------------
# POO: Polimorfismo (Polymorphism)
# Ejemplo sencillo: podemos definir otra clase de usuario que sobreescriba comportamiento.
# No es necesario para el app, pero lo dejo ilustrado.
# -------------------------------
class AdminUser(Usuario):
    __tablename__ = 'admin_user'
    __mapper_args__ = {'polymorphic_identity': 'admin_user'}
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    def can_edit(self):
        # sobrescribimos/extendemos método (polimorfismo simple)
        return True

# -----------------------------
# Clase Persona (para mostrar info pública)
# -----------------------------
class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    contacto_email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)



class Experiencia(db.Model):
    __tablename__ = 'experiencia'
    id = db.Column(db.Integer, primary_key=True)
    proyecto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    puesto = db.Column(db.String(200), nullable=False)
    periodo = db.Column(db.String(120), nullable=False)
    logros = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Educacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    institucion = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(255))
    periodo = db.Column(db.String(150))
    estado = db.Column(db.String(100))

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    institucion = db.Column(db.String(200), nullable=False)
    periodo = db.Column(db.String(150))

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(300))
    fecha = db.Column(db.String(50))
    github_url = db.Column(db.String(200))
    imagen = db.Column(db.String(255))
