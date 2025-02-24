"""
main.py

Entry point for the DataLectorBaysi application.
Initializes the PyQt5 application and launches the main UI window.
"""

from ui.Interface import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    window.delete_files()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
