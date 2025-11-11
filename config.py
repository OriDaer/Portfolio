import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cambia_esto_por_una_llave_segura')
    #os.environ.get('DATABASE_URL') lo que hace es buscar una variable de entorno llamada DATABASE_URL y si no la encuentra, usa la cadena por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root@localhost/portfolio_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
