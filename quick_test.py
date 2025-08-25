"""
Quick Test Script for Ultra-Fast PDF Loading
This script demonstrates the new ultra-fast PDF loading capability
"""

import time
from file_search_app import FileSearchApp

def test_ultra_fast_loading():
    """Test the ultra-fast loading functionality."""
    print("🚀 Testing Ultra-Fast PDF Loading")
    print("=" * 40)
    
    # Note: This will create the GUI but you can test loading performance
    app = FileSearchApp()
    
    print("✅ Application created successfully!")
    print("\n📋 How to test:")
    print("1. Click 'Load File' and select a large PDF")
    print("2. Notice instant loading (should be < 5 seconds even for huge files)")
    print("3. Try searching - first search extracts text on-demand")
    print("4. Subsequent searches of same pages are very fast")
    print("\n🎯 Key Benefits:")
    print("• PDF files load instantly regardless of size")
    print("• Memory usage is minimal until you search")
    print("• Cancel button works during search operations")
    print("• Progress bar shows real-time search progress")
    
    # Start the application
    app.run()

if __name__ == "__main__":
    test_ultra_fast_loading()
