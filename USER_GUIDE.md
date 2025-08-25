# PDF & Excel Search Tool - User Guide

## 🚀 Quick Start Instructions

### Step 1: Install Python (if not already installed)
1. Download Python 3.9+ from [python.org](https://python.org)
2. **IMPORTANT**: During installation, check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing: `python --version`

### Step 2: Install Dependencies
Choose one of these methods:

**Method A: Use the setup script**
- Double-click `setup.bat` and follow the prompts

**Method B: Manual installation**
- Open Command Prompt in this folder
- Run: `pip install -r requirements.txt`

### Step 3: Run the Application
- Double-click `file_search_app.py` or
- Open Command Prompt and run: `python file_search_app.py`

## 📱 Application Features

### Main Interface Components

1. **File Management Section**
   - Load File button: Opens PDF or Excel files
   - File path display: Shows currently loaded file
   - Clear button: Removes loaded file

2. **Search Options Section**
   - Column selection (Excel only): Choose which columns to search
   - Multi-select toggle: Enable searching multiple columns
   - Search box: Enter your search term
   - Case sensitive option: Toggle case-sensitive search
   - Search button: Execute the search

3. **Results Section**
   - Scrollable results display
   - Clear Results button: Clear current results
   - Export Results button: Save results to text file
   - Results counter: Shows number of matches found

4. **Status Bar**
   - Real-time status updates during operations

## 🔍 How to Search

### PDF Files
1. Click "Load File" and select a PDF
2. Enter search term in the search box
3. Optionally enable "Case sensitive"
4. Click "Search" or press Enter

**Results will show:**
- Page number where text was found
- Context (surrounding text paragraphs)
- Multiple matches per page if applicable

### Excel Files
1. Click "Load File" and select an Excel file (.xlsx or .xls)
2. Choose search columns:
   - **Single column**: Select from dropdown
   - **Multiple columns**: Check "Multi-select columns" and choose from list
3. Enter search term (text or number)
4. Optionally enable "Case sensitive"
5. Click "Search" or press Enter

**Results will show:**
- Row number in original Excel file
- Which columns contained matches (marked with ★)
- All column values for the matched row

## 💡 Search Tips

### PDF Search
- Search terms can be words, phrases, or numbers
- Use case-sensitive search for exact matches
- Results show surrounding context for better understanding

### Excel Search
- Can search for text or numeric values
- Numeric searches work with exact matches
- Text searches work with partial matches
- Select multiple columns to search across different data types

## 📤 Exporting Results

1. After performing a search, click "Export Results"
2. Choose location and filename
3. Results are saved as a text file (.txt)
4. File contains all search results with formatting

## ⚙️ Creating a Standalone Executable

To create a single .exe file that doesn't require Python:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Create the executable:
   ```
   pyinstaller --onefile --windowed file_search_app.py
   ```

3. Find your .exe file in the `dist` folder

## 🔧 Troubleshooting

### Common Issues

**"Python was not found"**
- Install Python from python.org
- Make sure "Add Python to PATH" was checked during installation
- Restart your computer after installation

**"No module named 'pandas'"**
- Run: `pip install pandas openpyxl pdfplumber`
- Make sure you're in the correct folder

**Application won't start**
- Run `python test_dependencies.py` to check installation
- Make sure all required packages are installed

**PDF file won't load**
- Ensure the PDF is not password-protected
- Try a different PDF file to test
- Check that the file is not corrupted

**Excel file won't load**
- Ensure the file is in .xlsx or .xls format
- Close the file in Excel if it's currently open
- Check that the file is not corrupted

**No search results found**
- For Excel: Make sure you've selected at least one column
- Check your search term spelling
- Try case-insensitive search
- For Excel: Try searching in different columns

### Getting Help

If you encounter issues:
1. Run `python test_dependencies.py` to verify installation
2. Check the status bar for error messages
3. Try with the sample Excel file created by the test script

## 📋 File Format Support

### Supported Formats
- **PDF**: .pdf files
- **Excel**: .xlsx (Excel 2007+), .xls (Excel 97-2003)

### Not Supported
- Password-protected PDFs
- CSV files (can be opened in Excel and saved as .xlsx)
- Word documents
- Scanned PDFs without text layer

## 🎯 Performance Notes

- Large PDF files may take a few seconds to load
- Excel files with many columns/rows are handled efficiently
- Search operations are optimized for speed
- Results are displayed progressively

## 🔄 Version Information

This application includes:
- PDF text extraction using pdfplumber
- Excel processing using pandas and openpyxl
- GUI built with tkinter (included with Python)
- Cross-platform compatibility (Windows, Mac, Linux)

Enjoy using your PDF & Excel Search Tool! 🎉
