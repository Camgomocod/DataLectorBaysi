/* DATOS DE LOS CLIENTES DE MERCADO LIBRE*/

CREATE TABLE cliente(
	id_telefono varchar(255) PRIMARY KEY,
	nombre varchar(255),
	ciudad varchar(255),
	departamento varchar(255),
	direccion varchar(255)
);

CREATE TABLE venta(
	telefono varchar(255) NOT NULL,
	nombre_producto varchar(255),
	cantidad_producto INT,
	facha DATE,
	CONSTRAINT fk_telefono FOREIGN KEY (telefono) REFERENCES cliente (id_telefono)
);

CREATE INDEX fk_telefono
ON venta (telefono);

/* DATOS DE LOS USUARIOS DE LA INTERFAZ */

CREATE TABLE users(
	id_log SERIAL PRIMARY KEY,
	user_name varchar(255) UNIQUE NOT NULL,
	name varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	last_name varchar(255) NOT NULL,
	email varchar(255) NOT NULL
);

CREATE INDEX idx_users_username ON users (user_name);

CREATE INDEX idx_users_email ON users (email);