import tkinter as tk
from tkinter import filedialog
from Pdf import PdfData

""" D:\General Files\Projects\DataLectorBaysi\src """
class interface:
  def __init__(self) -> None:
    self.ventana = tk.Tk()
    self.ventana.title("Abrir carpeta")
    self.ventana.geometry("400x200")
    self.botonSumar = tk.Button(self.ventana, text="Sumar", command=self.suma)
    self.botonSumar.pack(side="bottom", anchor="center", padx=10, pady=10)
    self.resultado = tk.Label(self.ventana, text="Resultado: ")
    self.resultado.pack()
    self.boton = tk.Button(self.ventana, text="Abrir carpeta", command=self.abrir_carpeta)
    self.boton.pack(side="bottom", anchor="center", padx=10, pady=50)

    
  # Crear la interfaz gráfica

  def abrir_carpeta(self):
    """Abre la carpeta especificada en la variable 'ruta_carpeta'."""
    ruta_carpeta = "D:\General Files\Projects\DataLectorBaysi\documents"  # Cambia esta ruta a la que deseas abrir
    filedialog.askdirectory(initialdir=ruta_carpeta)

  def suma(self):
    suma1 = PdfData()
    resultado = suma1.sumar()
    print(resultado)
    self.resultado.config(text=f"Resultado: {resultado}")
  
if __name__ == "__main__":
  interfaceG = interface()
  interfaceG.ventana.mainloop()
  
