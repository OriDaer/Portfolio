CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    nombre_publico VARCHAR(120),
    profile_image VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP ,
    acerca_de_mi TEXT not null
);
CREATE tabLE IF NOT EXISTS persona (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    contacto_email VARCHAR(150) NOT NULL,
    telefono VARCHAR(200) NOT NULL,
    direccion VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS experiencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proyecto VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    puesto VARCHAR(200) NOT NULL,
    periodo VARCHAR(120) NOT NULL,
    logros TEXT NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS educacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    institucion VARCHAR(200) NOT NULL,
    logo VARCHAR(255),
    periodo VARCHAR(150),
    estado VARCHAR(100),  -- "En curso", "Finalizado", etc.
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    institucion VARCHAR(200) NOT NULL,
    periodo VARCHAR(150)
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha VARCHAR(50),
    github_url VARCHAR(255),
    imagen VARCHAR(255)  -- aquí guardamos el nombre del archivo subido
);
