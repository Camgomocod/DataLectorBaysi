import os
import PyPDF2
import re
from Connector import Connect

class Pdf:

    def __init__(self) -> None:
        self.path = "D:\\General Files\\Documents\\Baysi\\Guias\\"
        # D:\General Files\Documents\Baysi\Guias
        self.patrones = [' - Unidad', ' - g', ' - mL', ' - Kg', ' - L']
        self.cn = Connect()
    
    # Detector de patrones derecha
    def get_next_to_upper(self, text, pattern): 
        match = re.search(pattern, text)
        if match:
            return  match.group(2) + match.group(3)  # Devuelve el tercer grupo completo
        return None 
     
    # Eliminar seccion del nombre del producto
    def eliminar_patron(self, nombre_producto):
        for patron in self.patrones:
            nombre_producto = nombre_producto.replace(patron, "")
            
        nombre_producto = nombre_producto[:nombre_producto.rfind(" a ")]

        return nombre_producto
    
    # Detector de patrones izquierda
    def get_previous_to_upper(self, text, pattern):
        match = re.search(pattern, text)
        if match:
            return match.group(1) + match.group(2)
        return None
        
    # Iterador pdfs carpeta
    def lectorPdfs(self):
        os.chdir(f'{self.path}\\upload')
        # Crea una lista de archivos PDF
        archivos_pdf = [f for f in os.listdir(f'{self.path}\\upload') if f.endswith('.pdf')]

        # Procesa cada archivo PDF
        for archivo_pdf in archivos_pdf:
            self.read_pdf(archivo_pdf)
        
    # Procesar el nombre del comprador 
    def procesar_nombre_comprador(self, linea):
        linea = linea.replace(".", "")
        if re.search(r"(.*?)\s([A-Z])([A-Z].*)$", linea):
            nombre_comprador = self.get_previous_to_upper(linea, r"(.*?)([A-Z])([A-Z].*)$")
        elif re.search(r"(.*?)([a-z])([ÁÉÍÓÚ].*)$", linea):
            nombre_comprador= self.get_previous_to_upper(linea, r"(.*?)([a-z])([ÁÉÍÓÚ].*)$")
        else:
            nombre_comprador = self.get_previous_to_upper(linea, r"(.*?)([a-z])([A-Z])")
        
        return nombre_comprador
    
    # Obtener el nombre del comprador
    def get_nombre_comprador(self, lineas):
        try:
            linea = lineas[4]
            nombre_comprador = linea
            if nombre_comprador:
                nombre_comprador = self.procesar_nombre_comprador(linea)
            if nombre_comprador == None:
                linea = lineas[5]
                nombre_comprador = self.procesar_nombre_comprador(linea)

        except Exception as ex:
            print(ex)

        return nombre_comprador
    #Procesar el nombre del producto
    def procesar_nombre_producto(self, linea):
        linea = linea.replace(".", "")

        if re.search(r"(.*?)\s([A-Z])([A-Z].*)$", linea):
            nombre_producto = self.get_next_to_upper(linea, r"([A-Z])([A-Z].*)(.*?)$")
        elif re.search(r"(.*?)([a-z])([ÁÉÍÓÚ].*)$", linea):
            nombre_producto= self.get_next_to_upper(linea, r"([a-z])([ÁÉÍÓÚ].*)(.*?)$")
        else:
            nombre_producto = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
        
        return nombre_producto
    
    # Obtener el nombre del producto
    def get_nombre_productos(self, lineas):
        try:
            linea = lineas[4]
            nombre_producto = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")   

            if nombre_producto:
                nombre_producto = self.procesar_nombre_producto(linea)
                
            if nombre_producto == None:
                linea = lineas[5]
                nombre_producto = self.procesar_nombre_producto(linea)

            nombre_producto = nombre_producto.replace("'", "")
            nombre_producto = self.eliminar_patron(nombre_producto)
                
        except Exception as ex:
            print(ex)
        
        return nombre_producto
    # Obtener el resto de productos, cuando en una guia hay mas de una venta
    def procesar_productos(self, size, lineas, id_telefono, cantidad_producto, fecha):
        for i in range(size, len(lineas)):
            cantidad = re.findall('Cantidad: (.*)',lineas[i])
            if cantidad != []:
                nombre_producto = lineas[i-1]
                nombre_producto = nombre_producto.replace("'", "")
                nombre_productoF = self.eliminar_patron(nombre_producto)                    
                self.cn.insert_data_venta(id_telefono, nombre_productoF, cantidad_producto, fecha)

    # Si hay mas de dos productos en la guia, registro
    def get_nombre_producto_otros(self, lineas, id_telefono, cantidad_producto, fecha):
        try:
            linea = lineas[4]
            nombre_productoX = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
            # Agregar productos cuando hay en la guia mas de dos ventas
            if nombre_productoX:
                self.procesar_productos(7, lineas, id_telefono, cantidad_producto, fecha)
            # Agregar productos cuando hay en la guia mas de dos ventas
            if nombre_productoX == None:
                linea = lineas[5]
                nombre_productoX = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
                if nombre_productoX:
                    self.procesar_productos(8, lineas, id_telefono, cantidad_producto, fecha)
        except Exception as ex:
            print(ex)
    
    # Obtener la fecha de compra
    def get_fecha(self, text):
        # Buscar la fecha:
        titulo = re.findall(r"(Envia|SERVIENTREGA|DEPRISA)", text)[0]
        if titulo in ('Envia', 'SERVIENTREGA', 'DEPRISA'):
            if titulo == 'Envia':
                fecha = re.findall(r'Fecha: (.*)F', text)[0]
            elif titulo == 'SERVIENTREGA':
                fecha = re.findall(r'Fecha: (.*?)Fecha Prog. Entrega:', text)[0]
            elif titulo == 'DEPRISA':
                fecha = re.findall(r'Fecha:(.*)', text)[0]
            else: 
                raise ValueError("Titulo del archivo no recononocido")
        return fecha
    
    def get_telefono(self, text):
        telefono = re.findall(r'Telefono:  (.*)', text)[0],
        telefono_string = "".join(telefono)

        # Elimina el símbolo ">" de la cadena
        telefono_string = telefono_string.replace(">", "")
    
        int_telefono = int(telefono_string)
        
        return int_telefono
    
    # Leer los datos del pdf
    def read_pdf(self, archivo_pdf):
        # Abre el archivo PDF usando PdfReader
        pdf = PyPDF2.PdfReader(archivo_pdf)

        # Obtiene la primera página del documento
        page = pdf.pages[0]
        text = page.extract_text()
        
        page2 = pdf.pages[1]
        text2 = page2.extract_text()
        
        lineas = text2.split('\n')
        # Extrae el texto de la página
        # Nombre del comprador
        nombre_comprador = self.get_nombre_comprador(lineas)
        #Nombre del producto
        
        # Departamento y ciudad del comprador
        ciudad_comprador = re.findall(r'Ciudad de destino: (.*)', text)[0]
        ciudad, departamento = ciudad_comprador.split(",")
        ciudad = ciudad.replace(" ", "")
        departamento = departamento.replace(" ", "")

        # Buscar la fecha:
        fecha = self.get_fecha(text)
            
        # Buscar cantidad del producto:
        cantidad = re.findall(r'Cantidad: (.*)',text2)[0]
        
        # Telefono 
        telefono = self.get_telefono(text)

        # Domicilio
        direccion = re.findall(r'Domicilio: (.*)', text)[0]
        
        # Nombre producto
        nombre_producto = self.get_nombre_productos(lineas)
        
        # Mandar los datos para la base de datos.
        self.cn.insert_data(telefono, nombre_comprador, departamento, ciudad, direccion, nombre_producto, cantidad, fecha)
        
        # Si hay mas de dos ventas en la guia se actualiza
        self.get_nombre_producto_otros(lineas, telefono, cantidad, fecha)

# Main
if __name__ == "__main__":
    pdf = Pdf()
    pdf.lectorPdfs()
    