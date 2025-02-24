"""
DataProcessor.py

This module provides functions to append processed sales data into CSV files.
It writes two CSV files:
  - main.csv: Contains the main sales data extracted from shipping guides.
  - ventas.csv: Contains additional sales data from guides with multiple sales.
"""
import os
import csv

BASE_PATH = os.path.join(os.path.dirname(__file__), "../data")
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

MAIN_CSV = os.path.join(BASE_PATH, "main.csv")
VENTA_CSV = os.path.join(BASE_PATH, "ventas.csv")

def append_main_data(telefono, nombre_comprador, departamento, ciudad, direccion, nombre_producto, cantidad, fecha):
    """
    Appends a row of main sales data to main.csv.
    
    Parameters:
      telefono            : Seller's phone number.
      nombre_comprador    : Buyer's name.
      departamento        : Buyer's department.
      ciudad              : Buyer's city.
      direccion           : Delivery address.
      nombre_producto     : Product name.
      cantidad            : Quantity sold.
      fecha               : Date of sale.
    """
    new_row = [telefono, nombre_comprador, departamento, ciudad, direccion, nombre_producto, cantidad, fecha]
    file_exists = os.path.exists(MAIN_CSV)
    with open(MAIN_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["telefono", "nombre_comprador", "departamento", "ciudad", "direccion", "nombre_producto", "cantidad", "fecha"])
        writer.writerow(new_row)

def append_venta_data(id_telefono, nombre_producto, cantidad_producto, fecha):
    """
    Appends a row of additional sale data to ventas.csv.
    
    Parameters:
      id_telefono         : Seller's phone identifier.
      nombre_producto     : Product name.
      cantidad_producto   : Quantity of product sold.
      fecha               : Date of sale.
    """
    new_row = [id_telefono, nombre_producto, cantidad_producto, fecha]
    file_exists = os.path.exists(VENTA_CSV)
    with open(VENTA_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["id_telefono", "nombre_producto", "cantidad_producto", "fecha"])
        writer.writerow(new_row)
