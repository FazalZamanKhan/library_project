@echo off
echo Installing PDF and Excel Search Tool Dependencies
echo ================================================

echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install pandas>=1.3.0
pip install openpyxl>=3.0.0
pip install pdfplumber>=0.6.0

echo.
echo Testing installation...
python test_dependencies.py

echo.
echo Setup complete! You can now run the application:
echo python file_search_app.py
pause
