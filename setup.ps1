# PDF & Excel Search Tool Setup Script
# Run this script to install dependencies and test the application

# Install required packages
Write-Host "Installing required Python packages..." -ForegroundColor Green
pip install -r requirements.txt

# Check if installation was successful
Write-Host "`nChecking installation..." -ForegroundColor Green
python -c "import pandas, pdfplumber, openpyxl; print('All dependencies installed successfully!')"

# Run the application
Write-Host "`nStarting the PDF & Excel Search Tool..." -ForegroundColor Green
python file_search_app.py
