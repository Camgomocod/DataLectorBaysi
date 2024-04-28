from tkinter import * 
import tkinter as tk
from tkinter import filedialog
from Pdf import PdfData
from Connector import Connect
from tkcalendar import *
import os 
import shutil
import re
import datetime
import hashlib
import time

class interface:
  def __init__(self) -> None:
    self.folder_path = "D:\\General Files\\Projects\\DataLectorBaysi\\documents"
    self.move_folder_path = None 
    self.queryF = False
    self.cn = Connect
    self.date = None
    self.date_show = self.cn.get_date()
    self.id_date = None
    self.warning = None
    # Ventana principal 
    self.window = tk.Tk()
    self.window.geometry("320x180")
    self.window.config(bg="#154854")
    self.window.title("BAYSI")

    self.origin_folder = tk.StringVar()
    self.destiny_folder = tk.StringVar()

    # Interaction Button Frame (Group buttons visually)
    self.button_frame = tk.Frame(self.window, bg="#2FAC73", bd=1, relief=tk.RAISED)
    self.button_frame.pack(fill=tk.X, pady=20, expand=True)
    
    # Apartado de actualización de datos
    self.label_date = tk.Label(self.button_frame, text="Ultima actualización : ")
    self.label_date.grid(row=0, column=0, pady=10, padx=10)
    self.label_date_show = tk.Label(self.button_frame, text=self.date_show)
    self.label_date_show.grid(row=0, column=1, pady=5)

    # Apartado de botones de interacción 
    self.button_open_root = tk.Button(self.button_frame, text="Carpeta Guías", command=self.open_root_directory, padx=15)
    self.button_open_root.grid(row=1, column=0, pady=10, padx=5)
    self.button_charge_pdf = tk.Button(self.button_frame, text="Cargar PDF",  state=DISABLED,command= self.charge_pdf,  padx=15)
    self.button_charge_pdf.grid(row=1, column=1, pady=10, padx=5)
    self.button_exit = tk.Button(self.button_frame, text="Salir", command=self.window.destroy, padx=15)
    self.button_exit.grid(row=1, column=2, pady=10, padx=5)

    # Label Frame
    self.label_frame = tk.Frame(self.window, bg="#2FAC73", bd=1, relief=tk.RAISED)
    self.label_frame.pack(fill=tk.X, expand=True)

    # Create a sample label in the label_frame
    self.label_warning = tk.Label(self.label_frame, text=self.warning, bg="#2FAC73")
    self.label_warning.grid(row=0, column=2, padx=10, pady=10)



  def charge_pdf(self): 

    if self.button_charge_pdf["state"] == 'normal':
      pdfData = PdfData()
      pdfData.lectorPdfs()
      self.label_warning.config(text="Datos Procesados!")

    if self.empty_folder(self.folder_path):
      self.cn.insert_date(self, self.id_date, self.date)
    
    self.label_date_show.config(text=self.cn.get_date())
    self.button_charge_pdf.config(state=DISABLED)

  def empty_folder(self, folder_path):
    for file in os.listdir(folder_path):
      if file.lower().endswith(".pdf"):
        return False
      
    return True
  
  def generate_unique_id(self, folder_name):
    base_str = None
    if folder_name: 
      date_match = re.search(r"(\d{2})-(\d{2})-(\d{4})", folder_name)
      if date_match:
        date_obj = datetime.datetime(int(date_match.group(3)), int(date_match.group(2)), int(date_match.group(1)))
        base_str = date_obj.strftime("%Y-%m-%d")
        self.date = base_str

    if not base_str:
      base_str = str(int(time.time() * 1000))
      
    numeric_id = int(hashlib.sha256(base_str.encode("utf-8")).hexdigest(), 16)
    formatted_id = str(numeric_id)
    self.id_date = formatted_id[:9]

    self.state_folder_charge()

    
  def state_folder_charge(self):
    if self.cn.get_id_date(self, self.id_date):
      self.button_charge_pdf.config(state=DISABLED)
      self.label_warning.config(text="La carpeta seleccionada ya fue procesada")
      return
    
    if self.empty_folder(self.move_folder_path):
      self.button_charge_pdf.config(state=DISABLED)
      self.label_warning.config(text=" ¡LA CARPETA SELECCIONA ESTÁ VACIA!", fg="#FE7955")
    else:
      self.button_charge_pdf.config(state=DISABLED if self.queryF else NORMAL)
      self.label_warning.config(text=" ¡TODO EN ORDEN!", fg="#DAFFF7")

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
      self.move_folder_path = origin_path
      self.origin_folder.set(os.path.basename(origin_path))
      self.copy_pdfs()
  
    self.generate_unique_id(self.origin_folder.get())
  
  def delete_files(self):
    path = 'D:\\General Files\\Projects\\DataLectorBaysi\\documents'
    os.chdir(path)
    pdf_files = [f for f in os.listdir(path) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
      os.remove(pdf_file)
  

if __name__ == "__main__":
  interfaceG = interface()
  cn = Connect
  interfaceG.date_show = cn.get_date()
  interfaceG.window.mainloop()
  interfaceG.delete_files()