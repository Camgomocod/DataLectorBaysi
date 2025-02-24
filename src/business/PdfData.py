"""
PdfData.py

Contains the PdfData class which implements the logic to extract and process sales data 
from shipping guide PDFs generated for Mercado Libre sellers.
It is designed to handle guides from Servientrega, Envia, and Inter Rapidisimo by detecting
specific patterns in the PDF's text.
"""
import os
import PyPDF2
import re
from services.DataProcessor import append_main_data, append_venta_data

class PdfData:
    def __init__(self) -> None:
        """
        Initializes PdfData with default settings including the path to files and 
        the list of pattern substrings to remove from product names.
        """
        self.path = "D:\\General Files\\Projects\\DataLectorBaysi\\"
        # Guide folder sample: D:\General Files\Documents\Baysi\Guias
        self.patrones = [" z- Unidad", " - g", " - mL", " - Kg", " - L"]

    def sumar(self):
        """Example method that returns a constant value."""
        return 5

    def get_next_to_upper(self, text, pattern):
        """
        Searches for a pattern in the given text and returns the concatenation of match groups 2 and 3.
        
        Parameters:
          text    : The string to search within.
          pattern : The regex pattern to apply.
        """
        match = re.search(pattern, text)
        if match:
            return match.group(2) + match.group(3)
        return None

    def eliminar_patron(self, nombre_producto):
        """
        Removes defined pattern substrings from the product name.
        
        Parameters:
          nombre_producto : The original product name.
        """
        for patron in self.patrones:
            nombre_producto = nombre_producto.replace(patron, "")
        nombre_producto = nombre_producto[: nombre_producto.rfind(" a ")]
        return nombre_producto

    def get_previous_to_upper(self, text, pattern):
        """
        Searches for a pattern and returns the concatenation of match groups 1 and 2.
        
        Parameters:
          text    : The string to search within.
          pattern : The regex pattern to apply.
        """
        match = re.search(pattern, text)
        if match:
            return match.group(1) + match.group(2)
        return None

    def lectorPdfs(self):
        """
        Iterates through PDF files in the documents folder, processes each file,
        and removes it afterwards.
        """
        path = "D:\\General Files\\Projects\\DataLectorBaysi\\"
        os.chdir(f"{path}\\documents")
        archivos_pdf = [f for f in os.listdir(f"{path}\\documents") if f.endswith(".pdf")]
        for archivo_pdf in archivos_pdf:
            self.read_pdf(archivo_pdf)
            os.remove(archivo_pdf)

    def procesar_nombre_comprador(self, linea):
        """
        Processes the buyer's name from a text line by applying various regex patterns.
        
        Parameters:
          linea : The input line extracted from the PDF text.
        """
        linea = linea.replace(".", "")
        if re.search(r"(.*?)\s([A-Z])([A-Z].*)$", linea):
            nombre_comprador = self.get_previous_to_upper(linea, r"(.*?)([A-Z])([A-Z].*)$")
        elif re.search(r"(.*?)([a-z])([ÁÉÍÓÚ].*)$", linea):
            nombre_comprador = self.get_previous_to_upper(linea, r"(.*?)([a-z])([ÁÉÍÓÚ].*)$")
        else:
            nombre_comprador = self.get_previous_to_upper(linea, r"(.*?)([a-z])([A-Z])")
        return nombre_comprador

    def get_nombre_comprador(self, lineas):
        """
        Extracts the buyer's name from the PDF text lines.
        
        Parameters:
          lineas : A list of lines extracted from the PDF.
        """
        try:
            linea = lineas[4]
            nombre_comprador = linea
            if nombre_comprador:
                nombre_comprador = self.procesar_nombre_comprador(linea)
            if nombre_comprador is None:
                linea = lineas[5]
                nombre_comprador = self.procesar_nombre_comprador(linea)
        except Exception as ex:
            print(ex)
        return nombre_comprador

    def procesar_nombre_producto(self, linea):
        """
        Processes the product name from a line using regex matching.
        
        Parameters:
          linea : The input line from which the product name is to be extracted.
        """
        linea = linea.replace(".", "")
        if re.search(r"(.*?)\s([A-Z])([A-Z].*)$", linea):
            nombre_producto = self.get_next_to_upper(linea, r"([A-Z])([A-Z].*)(.*?)$")
        elif re.search(r"(.*?)([a-z])([ÁÉÍÓÚ].*)$", linea):
            nombre_producto = self.get_next_to_upper(linea, r"([a-z])([ÁÉÍÓÚ].*)(.*?)$")
        else:
            nombre_producto = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
        return nombre_producto

    def get_nombre_productos(self, lineas):
        """
        Extracts and processes the product name from the list of PDF text lines.
        
        Parameters:
          lineas : A list of lines from the PDF.
        """
        try:
            linea = lineas[4]
            nombre_producto = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
            if nombre_producto:
                nombre_producto = self.procesar_nombre_producto(linea)
            if nombre_producto is None:
                linea = lineas[5]
                nombre_producto = self.procesar_nombre_producto(linea)
            nombre_producto = nombre_producto.replace("'", "")
            nombre_producto = self.eliminar_patron(nombre_producto)
        except Exception as ex:
            print(ex)
        return nombre_producto

    def procesar_productos(self, size, lineas, id_telefono, cantidad_producto, fecha):
        """
        Processes additional product sales in guides with multiple sales entries.
        
        Parameters:
          size             : Starting index to scan the lines.
          lineas           : All PDF text lines.
          id_telefono      : Unique identifier for the seller.
          cantidad_producto: Quantity sold.
          fecha            : Date of sale.
        """
        for i in range(size, len(lineas)):
            cantidad = re.findall("Cantidad: (.*)", lineas[i])
            if cantidad != []:
                nombre_producto = lineas[i - 1].replace("'", "")
                nombre_productoF = self.eliminar_patron(nombre_producto)
                append_venta_data(id_telefono, nombre_productoF, cantidad_producto, fecha)

    def get_nombre_producto_otros(self, lineas, id_telefono, cantidad_producto, fecha):
        """
        Determines if there are additional products in the guide and processes them.
        
        Parameters:
          lineas           : A list of PDF text lines.
          id_telefono      : Seller's phone identifier.
          cantidad_producto: Quantity of product sold.
          fecha            : Sale date.
        """
        try:
            linea = lineas[4]
            nombre_productoX = self.get_next_to_upper(linea, r"([a-z])([A-Z])(.*)")
            if nombre_productoX:
                self.procesar_productos(7, lineas, id_telefono, cantidad_producto, fecha)
            if nombre_productoX is None:
                linea = lineas[5]
                nombre_productoX = self.get_next_to_upper(linea, r"([a-z])([A-Z])w(.*)")
                if nombre_productoX:
                    self.procesar_productos(8, lineas, id_telefono, cantidad_producto, fecha)
        except Exception as ex:
            print(ex)

    def get_fecha(self, text):
        """
        Extracts the sale date from the PDF text based on the courier model detected.
        
        Parameters:
          text : The full text extracted from a PDF.
        """
        titulo = re.findall(r"(Envia|SERVIENTREGA|DEPRISA)", text)[0]
        if titulo in ("Envia", "SERVIENTREGA", "DEPRISA"):
            if titulo == "Envia":
                fecha = re.findall(r"Fecha: (.*)F", text)[0]
            elif titulo == "SERVIENTREGA":
                fecha = re.findall(r"Fecha: (.*?)Fecha Prog. Entrega:", text)[0]
            elif titulo == "DEPRISA":
                fecha = re.findall(r"Fecha:(.*)", text)[0]
            else:
                raise ValueError("Titulo del archivo no reconocido")
        return fecha

    def get_telefono(self, text):
        """
        Extracts and converts the phone number from the PDF text.
        
        Parameters:
          text : The full text extracted from a PDF.
        """
        telefono = (re.findall(r"Telefono:  (.*)", text)[0],)
        telefono_string = "".join(telefono)
        telefono_string = telefono_string.replace(">", "")
        int_telefono = int(telefono_string)
        return int_telefono

    def read_pdf(self, archivo_pdf):
        """
        Reads a PDF file, extracts text from specific pages, processes the data,
        and writes the data into CSV files.
        
        Parameters:
          archivo_pdf : The filename of the PDF to process.
        """
        pdf = PyPDF2.PdfReader(archivo_pdf)
        page = pdf.pages[0]
        text = page.extract_text()
        page2 = pdf.pages[1]
        text2 = page2.extract_text()
        lineas = text2.split("\n")
        nombre_comprador = self.get_nombre_comprador(lineas)
        ciudad_comprador = re.findall(r"Ciudad de destino: (.*)", text)[0]
        ciudad, departamento = ciudad_comprador.split(",")
        ciudad = ciudad.replace(" ", "")
        departamento = departamento.replace(" ", "")
        fecha = self.get_fecha(text)
        cantidad = re.findall(r"Cantidad: (.*)", text2)[0]
        telefono = self.get_telefono(text)
        direccion = re.findall(r"Domicilio: (.*)", text)[0]
        nombre_producto = self.get_nombre_productos(lineas)
        append_main_data(telefono, nombre_comprador, departamento, ciudad, direccion, nombre_producto, cantidad, fecha)
        self.get_nombre_producto_otros(lineas, telefono, cantidad, fecha)
