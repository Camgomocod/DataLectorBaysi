from tkinter import * 
import tkinter as tk
from Pdf import PdfData
from tkcalendar import *
import os 

class interface:
  def __init__(self) -> None:
    self.window = tk.Tk()
    self.window.geometry("400x300")
    self.window.title("Abrir carpeta")

    self.window_frame = tk.Frame(self.window)
    self.window_frame.pack(side=tk.BOTTOM, pady=20)
    
    self.button_open_directory = tk.Button(self.window_frame, text="Abrir carpeta", command=self.open_directory)
    self.button_open_root = tk.Button(self.window_frame, text="Carpeta Guias", command=self.open_root_directory)
    self.button_charge_pdf = tk.Button(self.window_frame, text="CargarPdf", command=self.charge_pdf)
    
    self.button_open_root.grid(row=0, column=0, pady=10, padx=5)
    self.button_open_directory.grid(row=0, column=1, pady=10, padx=5)
    self.button_charge_pdf.grid(row=0, column=2, pady=10, padx=5)
    self.window_frame.grid_columnconfigure(1, weight=1)

    self.selected_date = StringVar()

    self.calendar = Calendar(self.window, selectmode="day", year=2024, month=4, date=24)
    self.calendar.pack(pady=20)

    self.get_date_button = Button(self.window_frame, text="Obtener fecha", command=self.get_selected_date)

    self.selected_date_label = Label(self.window, textvariable=self.selected_date)
    self.selected_date_label.pack(pady=20)

    self.get_date_button.grid(row=0, column=4, pady=10, padx=5)
    
  def get_selected_date(self):
    self.selected_date.set(self.calendar.get_date())  
  # Crear la interfaz gráfica
  def open_directory(self):
    folder_path = "D:\\General Files\\Projects\\DataLectorBaysi\\documents"
    os.startfile(folder_path)

  def charge_pdf(self): 
    pdfData = PdfData()
    pdfData.lectorPdfs()
  
  def open_root_directory(self):
    folder_path = "D:\\General Files\\Documents\\Baysi\\Guias"
    os.startfile(folder_path)


if __name__ == "__main__":
  interfaceG = interface()
  interfaceG.window.mainloop()
  
