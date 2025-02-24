"""
Interface.py

Provides the PyQt5-based GUI for the DataLectorBaysi application.
This module defines the MainWindow class which manages user interactions such as:
 - Selecting the folder containing PDF guides.
 - Processing the PDFs.
 - Opening the CSV folder.
 - Exiting the application.
"""
import sys
import os
import datetime
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
)
from PyQt5.QtGui import QFont
from business.PdfData import PdfData

class MainWindow(QMainWindow):
    """
    MainWindow class for DataLectorBaysi.

    Sets up the user interface with buttons for selecting guide folders,
    processing PDF files, opening the CSV folder, and exiting the application.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BAYSI")
        self.setFixedSize(400, 250)
        self.setStyleSheet("""
            QMainWindow { background-color: #2e2e2e; }
            QLabel { color: #ffffff; }
            QPushButton {
                background-color: #4a90e2;
                border: none;
                color: #fff;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:disabled { background-color: #7f8c8d; }
            QPushButton:hover { background-color: #357ABD; }
        """)
        self.move_folder_path = None

        # Setup central widget and layout.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        v_layout = QVBoxLayout()
        central_widget.setLayout(v_layout)

        # Update label: shows the last update date.
        self.label_date = QLabel("Última actualización: N/A")
        self.label_date.setFont(QFont("Arial", 10))
        v_layout.addWidget(self.label_date)

        # Message label for status updates.
        self.label_message = QLabel("")
        self.label_message.setFont(QFont("Arial", 10))
        v_layout.addWidget(self.label_message)

        # Create buttons and layout.
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton("Carpeta Guías")
        self.btn_open.clicked.connect(self.open_folder)
        btn_layout.addWidget(self.btn_open)

        self.btn_charge = QPushButton("Cargar PDF")
        self.btn_charge.setEnabled(False)
        self.btn_charge.clicked.connect(self.charge_pdf)
        btn_layout.addWidget(self.btn_charge)
        
        self.btn_csv = QPushButton("Abrir CSV")
        self.btn_csv.clicked.connect(self.open_csv)
        btn_layout.addWidget(self.btn_csv)

        self.btn_exit = QPushButton("Salir")
        self.btn_exit.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_exit)

        v_layout.addLayout(btn_layout)

    def open_folder(self):
        """
        Opens a dialog to select the folder containing PDF guides.
        Copies the PDFs to the destination folder and enables the processing button.
        """
        initial_folder = "D:\\General Files\\Documents\\Baysi\\Guias"
        folder = QFileDialog.getExistingDirectory(self, "Seleccione la carpeta de origen", initial_folder)
        if folder:
            self.move_folder_path = folder
            self.copy_pdfs()
            self.btn_charge.setEnabled(True)
            self.label_message.setText("Carpeta: " + os.path.basename(folder))

    def copy_pdfs(self):
        """
        Copies PDF files from the selected folder to the application's documents folder.
        """
        dest_folder = "D:\\General Files\\Projects\\DataLectorBaysi\\documents"
        if self.move_folder_path:
            for root, _, files in os.walk(self.move_folder_path):
                for name in files:
                    full_path = os.path.join(root, name)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.copy(full_path, dest_folder)

    def charge_pdf(self):
        """
        Processes the PDFs in the destination folder using PdfData.
        Updates the status message and disables the processing button.
        """
        if self.btn_charge.isEnabled():
            pdfData = PdfData()
            pdfData.lectorPdfs()
            self.label_message.setText("Datos Procesados!")
            self.update_date()
            self.btn_charge.setEnabled(False)

    def update_date(self):
        """Updates the label showing the last update date and time."""
        self.label_date.setText("Última actualización: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def open_csv(self):
        """
        Opens the folder containing the CSV file outputs.
        Uses os.startfile to open the directory in the native file explorer.
        """
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        if os.path.exists(csv_path):
            os.startfile(csv_path)
        else:
            self.label_message.setText("No se encontró la carpeta de CSV.")

    def delete_files(self):
        """
        Deletes all PDF files from the destination folder after processing.
        """
        path = "D:\\General Files\\Projects\\DataLectorBaysi\\documents"
        for file in os.listdir(path):
            if file.endswith(".pdf"):
                os.remove(os.path.join(path, file))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    window.delete_files()
    sys.exit(exit_code)
