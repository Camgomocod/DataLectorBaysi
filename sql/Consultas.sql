/* ### PARA CLIENTE */
SELECT * FROM cliente;

DELETE FROM cliente WHERE id_telefono = '3507803680'

DELETE FROM cliente CASCADE;

/* ### PARA VENTA */
SELECT * FROM venta;

DELETE FROM venta WHERE telefono = '3507803680'

/* # Para buscar a clientes con varias compras */
SELECT * FROM venta WHERE telefono = '3002124669'

SELECT * FROM venta WHERE telefono = '3209907208'

TRUNCATE TABLE venta;


/* ### PRUEBAS DE CONSULTAS GENERALES */

SELECT E.id_telefono, E.nombre, C.nombre_producto, C.cantidad_producto
FROM cliente E INNER JOIN venta C
ON E.id_telefono = C.telefono
WHERE C.cantidad_producto > '2'

SELECT E.id_telefono, E.nombre, C.nombre_producto, C.cantidad_producto
FROM cliente E INNER JOIN venta C
ON E.id_telefono = C.telefono
WHERE cantidad_producto = '3';

SELECT E.id_telefono, E.nombre, C.nombre_producto, C.cantidad_producto
FROM cliente E INNER JOIN venta C
ON E.id_telefono = C.telefono
WHERE fecha = '2023-12-21' and nombre_producto = 'Rowatinex'

/* ### CONSULTAS QUE VAN A IR EN EL PROGRAMA" */

/* Consulta para ver el listado de zonas que mas compran, se la puede hacer para que funcione
por ciudades cuando se la haga desde la interfaz grafica */

SELECT
    ciudad,
    direccion,
    COUNT(*) AS total_ventas

FROM (
    SELECT
        cliente.ciudad,
        cliente.direccion,
        venta.telefono
    FROM cliente
    INNER JOIN venta
        ON cliente.id_telefono = venta.telefono
) AS sub
GROUP BY
    ciudad,
    direccion
ORDER BY
    total_ventas DESC
LIMIT
    1;


/* Consulta zona de las ciudades compran mas, esta es la que por ahora va a ir en la interfaz" */
SELECT
    ciudad,
    SUBSTRING(direccion, POSITION(',' IN direccion) + 1) AS zona,
    COUNT(*) AS total_ventas
FROM (
    SELECT
        cliente.ciudad,
        cliente.direccion,
        venta.telefono
    FROM cliente
    INNER JOIN venta
        ON cliente.id_telefono = venta.telefono
) AS sub
GROUP BY
    ciudad,
    zona
ORDER BY
    total_ventas DESC
LIMIT
    10;


/* Listar las ventas de un departamento por mes y por año*/
/* Revisar */
SELECT cliente.departamento, MONTH(fecha) AS mes, YEAR(fecha) AS anio, COUNT(*) AS cantidad
FROM venta
JOIN cliente
ON venta.telefono = cliente.id_telefono
GROUP BY cliente.departamento, MONTH(fecha), YEAR(fecha)
ORDER BY cliente.departamento, mes, anio;

/* Listar las ventas de un producto con un rango de fechas */
SELECT *
FROM venta
WHERE nombre_producto = 'producto-1'
AND fecha BETWEEN '2023-01-01' AND '2023-01-31';

/* Comparar meses */

/* Listar las ventas de un cliente ordenadas por fecha cantidad de productos vendidos" */
SELECT *
FROM venta
WHERE telefono = '1234567890'
ORDER BY fecha DESC, cantidad_producto DESC;

/* Listar las ventas de un departamento por mes */
SELECT
    cliente.departamento,
    EXTRACT(MONTH FROM fecha) AS mes,
    COUNT(*) AS cantidad
FROM venta
JOIN cliente
ON venta.telefono = cliente.id_telefono
GROUP BY cliente.departamento, EXTRACT(MONTH FROM fecha)
ORDER BY cliente.departamento, mes;

/* Listar las ventas de un producto mas vendidos */
/*Por mes*/
SELECT nombre_producto, COUNT(*) AS cantidad
FROM venta
GROUP BY nombre_producto
ORDER BY cantidad DESC
LIMIT 10;

/* Listar las ventas de un cliente ordenadas por fecha*/
SELECT *
FROM venta
WHERE telefono = '1234567890'
ORDER BY fecha DESC;

/* Listar todas las ventas de un departamento */
/* Por mes*/
SELECT *
FROM venta
JOIN cliente
ON venta.telefono = cliente.id_telefono
WHERE cliente.departamento = 'Antioquia';

/* Listar todas las ventas de un producto */
SELECT *
FROM venta
WHERE nombre_producto = 'producto-1';






