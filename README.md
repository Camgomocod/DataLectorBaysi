# DataLectorBaysi

DataLectorBaysi is a PDF processing application that extracts sales data from shipping guides generated for Mercado Libre sellers. These guides contain the necessary information for product shipments and are issued by major courier companies like Servientrega, Envia, and Inter Rapidisimo. The application is designed to detect and process the specific patterns present in each type of guide.

## Project Structure

```
/mnt/c/Users/Usuario/Projects/DataLectorBaysi/
├── data/
│   ├── main.csv         # Main sales data extracted from PDF guides
│   └── ventas.csv       # Additional sales data from multi-sale guides
├── src/
│   ├── business/
│   │   └── PdfData.py   # PDF extraction and processing logic (detects patterns for Servientrega, Envia, and Inter Rapidisimo)
│   ├── services/
│   │   └── DataProcessor.py  # Functions to write processed data into CSV files
│   ├── ui/
│   │   └── Interface.py  # PyQt5-based user interface implementation
│   └── main.py           # Application entry point
```

## Features

- **PDF Processing:** Reads and processes shipping guide PDFs from Mercado Libre, extracting key sales data.
- **Pattern Detection:** Specifically designed to handle and detect patterns from Servientrega, Envia, and Inter Rapidisimo guide models.
- **CSV Storage:** Exports the extracted data into CSV files (main.csv and ventas.csv) for review and further analysis.
- **Modern UI:** Features an improved and modern user interface built with PyQt5.
- **Clean Architecture:** Clearly separates business logic, service layer, and UI for ease of maintenance and extensibility.

## How to Run

1. Ensure you have Python 3.x installed.
2. Install the required packages:
   ```bash
   pip install PyQt5 PyPDF2 tkcalendar
   ```
3. Navigate to the project source directory:
   ```bash
   cd /mnt/c/Users/Usuario/Projects/DataLectorBaysi/src
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage Instructions

- **Select Guide Folder:** Click the "Carpeta Guías" button to choose the folder containing your Mercado Libre shipping guides.
- **Load PDFs:** Once the folder is selected, click "Cargar PDF" to process the guides and extract the sales data.
- **Open CSV Folder:** Use the "Abrir CSV" button to open the folder where the CSV files are stored.
- **Exit:** Click the "Salir" button to close the application.

## Customization

- Modify file paths in the code if your folder structure differs.
- Update the stylesheet in `Interface.py` to further enhance the GUI appearance.
- Extend or adjust the data extraction logic in `PdfData.py` as your guide formats or requirements evolve.

## License

This is an open-source project available for modification and distribution.
