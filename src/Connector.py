import psycopg2

class Connect:
    
    def insert_data(self, id_telefono, nombre, departamento, ciudad, direccion, nombre_producto, cantidad_producto, fecha):
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'database',
                database = 'BaysiDataBase'
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
                cursor.execute(
                    f"INSERT INTO venta (telefono, nombre_producto, cantidad_producto, fecha) VALUES ({id_telefono}, '{nombre_producto}', '{cantidad_producto}', '{fecha}')"
                )
                connection.commit()
            
                return
            else:
                cursor.execute(
                    f"INSERT INTO cliente (id_telefono, nombre, ciudad, departamento, direccion) VALUES ({id_telefono}, '{nombre}', '{ciudad}', '{departamento}', '{direccion}');"
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
                password = 'database',
                database = 'BaysiDataBase'
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

    def get_id_date(self, id_fecha):
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'database',
                database = 'BaysiDataBase'
            )
        except Exception as ex:
            print(ex)
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                    f"SELECT COUNT(*) FROM charge_date WHERE id_fecha = {id_fecha}"
                )
            resultado = cursor.fetchone()[0]
            connection.commit()
        
        except Exception as ex:
            print(ex)
        
        if resultado: 
            return True 
        else: 
            return False 
    
    def insert_date(self, id_date, date):
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'database',
                database = 'BaysiDataBase'
            )
        except Exception as ex:
            print(ex)
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                    f"INSERT INTO charge_date (id_fecha, fecha) VALUES ({id_date}, '{date}')"
                )
            connection.commit()
        
        except Exception as ex:
            print(ex)
            connection.close()

    def get_date():
        try:
            connection = psycopg2.connect(
                host = 'localhost',
                user = 'postgres',
                password = 'database',
                database = 'BaysiDataBase'
            )
        except Exception as ex:
            print(ex)
        
        try:
            cursor = connection.cursor()
            cursor.execute(
                    "SELECT fecha FROM charge_date ORDER BY fecha DESC LIMIT 1;"
                )
            
            result = cursor.fetchone()[0]
            connection.commit()
        
        except Exception as ex:
            print(ex)
            connection.close()
        
        return result
    
    
    

    