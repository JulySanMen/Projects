

CREATE DATABASE IF NOT EXISTS cuestionario;
USE cuestionario;

CREATE TABLE participantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    correo VARCHAR(255),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT,
    estilo ENUM('Activo', 'Reflexivo', 'Teórico', 'Pragmático')
);

CREATE TABLE respuestas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    pregunta_id INT,
    respuesta INT,
    FOREIGN KEY (participante_id) REFERENCES participantes(id),
    FOREIGN KEY (pregunta_id) REFERENCES preguntas(id)
);

CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participante_id INT,
    activo FLOAT,
    reflexivo FLOAT,
    teorico FLOAT,
    pragmatico FLOAT,
    FOREIGN KEY (participante_id) REFERENCES participantes(id)
);
