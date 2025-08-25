# PDF & Excel Search Desktop Application

A comprehensive Python desktop application that allows you to search through PDF files and Excel spreadsheets with an intuitive GUI.

## Features

### PDF Search Capabilities
- ✅ Load and search through PDF files
- ✅ Extract text from all pages
- ✅ Display page numbers where matches occur
- ✅ Show context (surrounding sentences/paragraphs)
- ✅ Case-sensitive and case-insensitive search options

### Excel Search Capabilities
- ✅ Load Excel files (.xlsx, .xls)
- ✅ Display all column names in dropdown/multi-select
- ✅ Single or multi-column search
- ✅ Search text or numeric values
- ✅ Display complete rows for matches (all columns)
- ✅ Show which specific columns contained the match

### User Interface
- ✅ Clean, intuitive Tkinter GUI
- ✅ File loading with drag-and-drop support
- ✅ Scrollable results display
- ✅ Export results to text files
- ✅ Status bar with real-time feedback
- ✅ Clear results functionality

## Requirements

- Python 3.9+
- Required packages (automatically installed):
  - `pandas` - Excel file processing
  - `openpyxl` - Excel file support
  - `pdfplumber` - PDF text extraction

## Installation & Usage

### Quick Start
1. Run the setup script:
   ```powershell
   .\setup.ps1
   ```

### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python file_search_app.py
   ```

## How to Use

### Loading Files
1. Click "Load File (PDF/Excel)" button
2. Select a PDF or Excel file from your computer
3. The file type will be automatically detected

### Searching PDFs
1. Load a PDF file
2. Enter your search term in the search box
3. Click "Search" or press Enter
4. Results will show:
   - Page number where text was found
   - Context (surrounding text)
   - Total number of matches

### Searching Excel Files
1. Load an Excel file
2. Select columns to search:
   - **Single column**: Use the dropdown
   - **Multiple columns**: Check "Multi-select columns" and choose from the list
3. Enter your search term (text or number)
4. Click "Search" or press Enter
5. Results will show:
   - Row number in the original Excel file
   - Which columns contained matches (★ marked)
   - All column values for matched rows

### Additional Features
- **Case Sensitivity**: Toggle case-sensitive search
- **Export Results**: Save search results to a text file
- **Clear Results**: Clear the current search results
- **File Management**: Clear loaded file and start over

## Supported File Formats
- **PDF**: `.pdf` files
- **Excel**: `.xlsx`, `.xls` files

## Creating an Executable

To create a standalone .exe file using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed file_search_app.py
   ```

3. The executable will be created in the `dist/` folder

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Corrupted files
- Missing search criteria
- File loading errors
- Search operation failures

## Technical Details

### Architecture
- **GUI Framework**: Tkinter (built into Python)
- **PDF Processing**: pdfplumber for reliable text extraction
- **Excel Processing**: pandas + openpyxl for comprehensive Excel support
- **Search Engine**: Regular expressions with case-insensitive options

### Performance
- Efficient memory usage for large files
- Progressive loading indicators
- Responsive UI during search operations

## Troubleshooting

### Common Issues
1. **Import Error**: Install missing dependencies using `pip install -r requirements.txt`
2. **File Won't Load**: Ensure file is not corrupted and is a supported format
3. **No Search Results**: Check column selection for Excel files, verify search term

### Dependencies Not Installing
If you encounter issues installing dependencies:
```bash
python -m pip install --upgrade pip
pip install pandas openpyxl pdfplumber
```

## Future Enhancements

Potential improvements for future versions:
- Support for additional file formats (Word, CSV)
- Advanced search patterns (regex support)
- Search result highlighting
- Batch file processing
- Search history
- Custom export formats (Excel, CSV)

## License

This project is open-source and available for modification and distribution.
