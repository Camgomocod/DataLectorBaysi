import psycopg2

class Connect:
    
    def insert_data(self, id_telefono, nombre, departamento, ciudad, direccion, nombre_producto, cantidad_producto, fecha):
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'oracle',
                database = 'Mercado libre'
            )
            
        except Exception as ex:
            print(ex)
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT * FROM cliente WHERE id_telefono = '{id_telefono}';"
            )
        
            cliente = cursor.fetchone()
            
            if cliente: 
                print(f"cliente ya registrado '{id_telefono}'")
                cursor.execute(
                    f"INSERT INTO venta (telefono, nombre_producto, cantidad_producto, fecha) VALUES ({id_telefono}, '{nombre_producto}', '{cantidad_producto}', '{fecha}')"
                )
                connection.commit()
            
                return
            else:
                cursor.execute(
                f"INSERT INTO cliente (id_telefono, nombre, departamento, ciudad, direccion) VALUES ({id_telefono}, '{nombre}', '{departamento}', '{ciudad}', '{direccion}');"
                )
                
                cursor.execute(
                f"INSERT INTO venta (telefono, nombre_producto, cantidad_producto, fecha) VALUES ({id_telefono}, '{nombre_producto}', '{cantidad_producto}', '{fecha}')"
                )
                
                connection.commit()
            
            
            connection.commit()
            
        except Exception as ex:
            print(ex)
            
    def insert_data_venta(self, id_telefono, nombre_producto, cantidad_producto, fecha):
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'oracle',
                database = 'Mercado libre'
            )
        except Exception as ex:
            print(ex)
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                    f"INSERT INTO venta (telefono, nombre_producto, cantidad_producto, fecha) VALUES ({id_telefono}, '{nombre_producto}', '{cantidad_producto}', '{fecha}')"
                )
            connection.commit()
        
        except Exception as ex:
            print(ex)
    
    
    

    