from tkinter import * 
import tkinter as tk
from tkinter import filedialog
from Pdf import PdfData
from tkcalendar import *
import os 
import shutil
import re
import datetime
import hashlib

class interface:
  def __init__(self) -> None:
  
    # Ventana principal 
    self.window = tk.Tk()
    self.window.geometry("350x250")
    self.window.config(bg="#222831")
    self.window.title("BAYSI")

    self.origin_folder = tk.StringVar()
    self.destiny_folder = tk.StringVar()

    etiqueta_nombre_origen = tk.Label(self.window, text="Nombre carpeta origen:")
    etiqueta_nombre_origen.pack()

    campo_texto_nombre_origen = tk.Entry(self.window, textvariable=self.origin_folder)
    campo_texto_nombre_origen.pack()

    # Interaction Button Frame (Group buttons visually)
    self.button_frame = tk.Frame(self.window, bg="#2C333D", bd=1, relief=tk.RAISED)
    self.button_frame.pack(fill=tk.X, pady=20, expand=True)
    # Declaración del apartado del calendario 

    self.button_open_root = tk.Button(self.button_frame, text="Carpeta Guías", command=self.open_root_directory, padx=15)
    self.button_open_root.grid(row=0, column=0, pady=10, padx=5)
    self.button_charge_pdf = tk.Button(self.button_frame, text="Cargar PDF", command=self.charge_pdf, padx=15)
    self.button_charge_pdf.grid(row=0, column=1, pady=10, padx=5)
    self.button_exit = tk.Button(self.button_frame, text="Salir", command=self.window.destroy, padx=15)
    self.button_exit.grid(row=0, column=2, pady=10, padx=5)
    
  
  def charge_pdf(self): 
    pdfData = PdfData()
    pdfData.lectorPdfs()

  def generate_unique_id(self, folder_name):
    date_match = re.search(r"(\d{2})-(\d{2})-(\d{4})", folder_name)

    if date_match:
      day = date_match.group(1)
      month = date_match.group(2)
      year = date_match.group(3)

      date_obj = datetime.datetime(int(year), int(month), int(day))
      print(date_obj)
      unique_id = hashlib.sha1(date_obj.strftime("%Y%m%d").encode("utf-8")).hexdigest()
      
      return unique_id
    else:
      raise ValueError("Invalid folder name: " + folder_name)

  def copy_pdfs(self):
    folder_path = "D:\\General Files\\Projects\\DataLectorBaysi\\documents"
    if origin_path:
      for file_name, file_type ,children_files in os.walk(origin_path):
        # Ignorar la carpeta actual 
        if file_name == ".":
          continue

        for file in children_files:
          full_path = os.path.join(file_name, file)
          # Copiar el archivo a la carpeta de destino 
          os.makedirs(os.path.dirname(folder_path), exist_ok=True)
          shutil.copy(full_path, folder_path)
  
  def open_root_directory(self):
    global origin_path
    folder_path = "D:\\General Files\\Documents\\Baysi\\Guias"
    origin_path = filedialog.askdirectory(initialdir=folder_path, title="Seleccione la carpeta de origen")
    if origin_path:
      self.origin_folder.set(os.path.basename(origin_path))
      self.copy_pdfs()
  

if __name__ == "__main__":
  interfaceG = interface()
  interfaceG.window.mainloop()
  folder_name = interfaceG.origin_folder.get()
  print(f"El nombre de la carpeta es {folder_name}")
  id = interfaceG.generate_unique_id(folder_name)
  print(id)
  
