"""
Test script for PDF & Excel Search Tool
This script verifies that all dependencies are properly installed
"""

def test_dependencies():
    """Test if all required dependencies are available."""
    print("Testing PDF & Excel Search Tool dependencies...")
    print("=" * 50)
    
    # Test pandas
    try:
        import pandas as pd
        print("✅ pandas:", pd.__version__)
    except ImportError as e:
        print("❌ pandas: Not installed")
        return False
    
    # Test openpyxl
    try:
        import openpyxl
        print("✅ openpyxl:", openpyxl.__version__)
    except ImportError as e:
        print("❌ openpyxl: Not installed")
        return False
    
    # Test pdfplumber
    try:
        import pdfplumber
        print("✅ pdfplumber:", pdfplumber.__version__)
    except ImportError as e:
        print("❌ pdfplumber: Not installed")
        return False
    
    # Test tkinter (should be built-in)
    try:
        import tkinter as tk
        print("✅ tkinter: Available")
    except ImportError as e:
        print("❌ tkinter: Not available")
        return False
    
    print("\n🎉 All dependencies are properly installed!")
    print("You can now run the application with: python file_search_app.py")
    return True

def create_sample_excel():
    """Create a sample Excel file for testing."""
    try:
        import pandas as pd
        
        # Sample data
        data = {
            'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
            'Age': [30, 25, 35, 28, 42],
            'Department': ['IT', 'HR', 'Finance', 'IT', 'Marketing'],
            'Salary': [75000, 65000, 80000, 70000, 90000],
            'Email': ['john@company.com', 'jane@company.com', 'bob@company.com', 'alice@company.com', 'charlie@company.com']
        }
        
        df = pd.DataFrame(data)
        df.to_excel('sample_data.xlsx', index=False)
        print("\n📊 Created sample Excel file: sample_data.xlsx")
        print("You can use this file to test the Excel search functionality.")
        
    except Exception as e:
        print(f"\n❌ Could not create sample Excel file: {e}")

if __name__ == "__main__":
    if test_dependencies():
        create_sample_excel()
    else:
        print("\n❌ Some dependencies are missing. Please run:")
        print("pip install -r requirements.txt")
