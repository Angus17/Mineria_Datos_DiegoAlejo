CREATE DATABASE IF NOT EXISTS journalctl;

USE journalctl;

CREATE TABLE IF NOT EXISTS usuario(
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tipo_proceso(
    id_tipo_proceso INT AUTO_INCREMENT PRIMARY KEY,
    tipo_de_proceso VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS proceso(
    id_proceso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proceso VARCHAR(500) NOT NULL,
);

CREATE TABLE IF NOT EXISTS severidad(
    id_severidad INT AUTO_INCREMENT PRIMARY KEY,
    nivel_severidad VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS logs_sistema(
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    fecha_proceso DATETIME NOT NULL,
    id_usuario INT NOT NULL,
    id_proceso INT NOT NULL,
    id_tipo_proceso INT NOT NULL,
    pid INT NOT NULL,
    uso_cpu FLOAT NOT NULL,
    uso_ram FLOAT NOT NULL,
    estado_proceso VARCHAR(20) NOT NULL,
    longitud_mensaje INT NOT NULL,
    mensaje_log TEXT NOT NULL,
    id_severidad INT NOT NULL,
    is_error TINYINT(1) NOT NULL,
    CONSTRAINT fk_usuario_log FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT fk_tipo_proceso_log FOREIGN KEY (id_tipo_proceso) REFERENCES tipo_proceso(id_tipo_proceso),
    CONSTRAINT fk_proceso_log FOREIGN KEY (id_proceso) REFERENCES proceso(id_proceso),
    CONSTRAINT fk_severidad_log FOREIGN KEY (id_severidad) REFERENCES severidad(id_severidad)
)

CREATE INDEX idx_fecha_proceso ON logs_sistema(fecha_proceso);