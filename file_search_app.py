"""
PDF and Excel Search Desktop Application
========================================

A comprehensive desktop application built with Python and Tkinter that allows users to:
1. Load and search through PDF files
2. Load and search through Excel files with column-specific searching
3. Display results in a user-friendly interface

Author: GitHub Copilot
Date: August 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import pdfplumber
import os
import re
from typing import List, Dict, Any, Optional, Tuple


class FileSearchApp:
    """Main application class for the PDF and Excel search tool."""
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("PDF & Excel Search Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Application state
        self.loaded_file_path: Optional[str] = None
        self.loaded_file_type: Optional[str] = None  # 'pdf' or 'excel'
        self.excel_data: Optional[pd.DataFrame] = None
        self.pdf_text_data: List[Dict[str, Any]] = []  # Store text by page
        self.pdf_file_path: Optional[str] = None  # For lazy loading
        self.cancel_loading = False  # Flag for canceling long operations
        
        # Setup the GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # File loading section
        self.setup_file_section(main_frame)
        
        # Search section
        self.setup_search_section(main_frame)
        
        # Results section
        self.setup_results_section(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
    def setup_file_section(self, parent):
        """Setup the file loading section."""
        # File loading frame
        file_frame = ttk.LabelFrame(parent, text="File Management", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Load file button
        self.load_btn = ttk.Button(file_frame, text="Load File (PDF/Excel)", 
                                  command=self.load_file, width=20)
        self.load_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        # File path label
        self.file_label = ttk.Label(file_frame, text="No file loaded", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Clear file button
        self.clear_file_btn = ttk.Button(file_frame, text="Clear", 
                                        command=self.clear_file, state=tk.DISABLED)
        self.clear_file_btn.grid(row=0, column=2, padx=(10, 0), pady=5)
        
    def setup_search_section(self, parent):
        """Setup the search controls section."""
        # Search frame
        search_frame = ttk.LabelFrame(parent, text="Search Options", padding="5")
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)
        
        # Column selection (for Excel files only)
        ttk.Label(search_frame, text="Columns:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Frame for column selection widgets
        column_frame = ttk.Frame(search_frame)
        column_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        column_frame.columnconfigure(0, weight=1)
        
        # Column selection combobox (for single selection)
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(column_frame, textvariable=self.column_var, 
                                        state="readonly", width=30)
        self.column_combo.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Multi-select listbox for columns (initially hidden)
        self.column_listbox_frame = ttk.Frame(column_frame)
        self.column_listbox = tk.Listbox(self.column_listbox_frame, height=4, 
                                        selectmode=tk.MULTIPLE, exportselection=False)
        column_scrollbar = ttk.Scrollbar(self.column_listbox_frame, orient=tk.VERTICAL,
                                        command=self.column_listbox.yview)
        self.column_listbox.configure(yscrollcommand=column_scrollbar.set)
        
        self.column_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        column_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.column_listbox_frame.columnconfigure(0, weight=1)
        
        # Toggle for multi-select
        self.multi_select_var = tk.BooleanVar()
        self.multi_select_cb = ttk.Checkbutton(column_frame, text="Multi-select columns",
                                              variable=self.multi_select_var,
                                              command=self.toggle_column_selection)
        self.multi_select_cb.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Search query
        ttk.Label(search_frame, text="Search:").grid(row=1, column=0, sticky=tk.W, pady=(10, 2))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 2))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Search options frame
        options_frame = ttk.Frame(search_frame)
        options_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))
        
        # Case sensitive option
        self.case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Case sensitive", 
                       variable=self.case_sensitive_var).grid(row=0, column=0, sticky=tk.W)
        
        # Search method info
        ttk.Label(options_frame, text="Using Ultra-Fast Search", 
                 foreground="green").grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Search button
        self.search_btn = ttk.Button(search_frame, text="Search", 
                                    command=self.perform_search, state=tk.DISABLED)
        self.search_btn.grid(row=3, column=1, sticky=tk.E, padx=(10, 0), pady=(10, 0))
        
        # Initially hide column selection widgets
        self.hide_column_widgets()
        
    def setup_results_section(self, parent):
        """Setup the results display section."""
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Search Results", padding="5")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results display (using scrolled text for flexibility)
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                     height=20, state=tk.DISABLED)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results control frame
        control_frame = ttk.Frame(results_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Clear results button
        self.clear_results_btn = ttk.Button(control_frame, text="Clear Results", 
                                           command=self.clear_results)
        self.clear_results_btn.grid(row=0, column=0, sticky=tk.W)
        
        # Export results button
        self.export_btn = ttk.Button(control_frame, text="Export Results", 
                                    command=self.export_results, state=tk.DISABLED)
        self.export_btn.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Results count label
        self.results_count_label = ttk.Label(control_frame, text="")
        self.results_count_label.grid(row=0, column=2, sticky=tk.E, padx=(20, 0))
        control_frame.columnconfigure(2, weight=1)
        
    def setup_status_bar(self, parent):
        """Setup the status bar with progress bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        # Status text
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Load a PDF or Excel file to begin")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar (initially hidden)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           maximum=100, length=200)
        
        # Cancel button (initially hidden)
        self.cancel_btn = ttk.Button(status_frame, text="Cancel", 
                                    command=self.cancel_operation, state=tk.DISABLED)
        
    def show_progress(self):
        """Show progress bar and cancel button."""
        self.progress_bar.grid(row=0, column=1, padx=(10, 5), sticky=tk.E)
        self.cancel_btn.grid(row=0, column=2, sticky=tk.E)
        self.cancel_btn.config(state=tk.NORMAL)
        self.cancel_loading = False
        
    def hide_progress(self):
        """Hide progress bar and cancel button."""
        self.progress_bar.grid_remove()
        self.cancel_btn.grid_remove()
        self.cancel_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        
    def cancel_operation(self):
        """Cancel the current loading operation."""
        self.cancel_loading = True
        self.status_var.set("Canceling...")
        self.cancel_btn.config(state=tk.DISABLED)
        
    def load_file(self):
        """Load a PDF or Excel file."""
        file_path = filedialog.askopenfilename(
            title="Select PDF or Excel file",
            filetypes=[
                ("All supported", "*.pdf;*.xlsx;*.xls"),
                ("PDF files", "*.pdf"),
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        # Show progress for loading
        self.show_progress()
        self.status_var.set("Loading file...")
        self.root.update()
        
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                self.load_pdf_file(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                self.load_excel_file(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format. Please select a PDF or Excel file.")
                return
                
            if not self.cancel_loading:  # Only update if not canceled
                self.loaded_file_path = file_path
                self.file_label.config(text=os.path.basename(file_path), foreground="black")
                self.clear_file_btn.config(state=tk.NORMAL)
                self.search_btn.config(state=tk.NORMAL)
                self.clear_results()
            else:
                # Reset if canceled
                self.clear_file()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.status_var.set("Error loading file")
        finally:
            self.hide_progress()
            
    def load_pdf_file(self, file_path: str):
        """Ultra-fast PDF loading - just stores file reference."""
        self.loaded_file_type = 'pdf'
        self.pdf_text_data = []
        self.pdf_file_path = file_path
        
        try:
            # Only open PDF to get page count - no text extraction
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                
            # Store only minimal page references - no text extraction at all
            for page_num in range(1, total_pages + 1):
                self.pdf_text_data.append({
                    'page': page_num,
                    'loaded': False  # Text will be loaded only when searching this page
                })
                
            self.hide_column_widgets()
            self.status_var.set(f"PDF loaded instantly - {total_pages} pages ready for search")
            
        except Exception as e:
            raise Exception(f"Failed to load PDF: {str(e)}")
        
    def load_excel_file(self, file_path: str):
        """Load and process an Excel file."""
        self.loaded_file_type = 'excel'
        self.excel_data = pd.read_excel(file_path)
        
        # Populate column selection widgets
        columns = list(self.excel_data.columns)
        self.column_combo['values'] = columns
        
        # Clear and populate listbox
        self.column_listbox.delete(0, tk.END)
        for col in columns:
            self.column_listbox.insert(tk.END, col)
            
        self.show_column_widgets()
        self.status_var.set(f"Excel loaded - {len(self.excel_data)} rows, {len(columns)} columns")
        
    def clear_file(self):
        """Clear the loaded file and reset the interface."""
        self.loaded_file_path = None
        self.loaded_file_type = None
        self.excel_data = None
        self.pdf_text_data = []
        self.pdf_file_path = None
        
        self.file_label.config(text="No file loaded", foreground="gray")
        self.clear_file_btn.config(state=tk.DISABLED)
        self.search_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        
        self.hide_column_widgets()
        self.clear_results()
        self.status_var.set("Ready - Load a PDF or Excel file to begin")
        
    def toggle_column_selection(self):
        """Toggle between single and multi-column selection."""
        if self.multi_select_var.get():
            self.column_combo.grid_remove()
            self.column_listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        else:
            self.column_listbox_frame.grid_remove()
            self.column_combo.grid(row=0, column=0, sticky=(tk.W, tk.E))
            
    def show_column_widgets(self):
        """Show column selection widgets for Excel files."""
        self.column_combo.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.multi_select_cb.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
    def hide_column_widgets(self):
        """Hide column selection widgets for PDF files."""
        self.column_combo.grid_remove()
        self.multi_select_cb.grid_remove()
        self.column_listbox_frame.grid_remove()
        
    def get_selected_columns(self) -> List[str]:
        """Get the selected columns for Excel search."""
        if not self.multi_select_var.get():
            # Single selection
            selected = self.column_var.get()
            return [selected] if selected else []
        else:
            # Multi-selection
            selected_indices = self.column_listbox.curselection()
            return [self.column_listbox.get(i) for i in selected_indices]
            
    def perform_search(self):
        """Perform search based on the loaded file type."""
        if not self.loaded_file_path:
            messagebox.showwarning("Warning", "Please load a file first.")
            return
            
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query.")
            return
            
        # Show progress for search
        self.show_progress()
        self.cancel_loading = False
        self.status_var.set("Searching...")
        self.root.update()
        
        try:
            if self.loaded_file_type == 'pdf':
                results = self.search_pdf(query)
            elif self.loaded_file_type == 'excel':
                results = self.search_excel(query)
            else:
                return
                
            if not self.cancel_loading:
                self.display_results(results, query)
            else:
                self.status_var.set("Search canceled")
                
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
            self.status_var.set("Search error")
        finally:
            self.hide_progress()
            
    def search_pdf_ultra_fast(self, query: str) -> List[Dict[str, Any]]:
        """Ultra-fast PDF search - loads and searches pages on-demand."""
        results = []
        case_sensitive = self.case_sensitive_var.get()
        total_pages = len(self.pdf_text_data)
        
        # Prepare search pattern
        if case_sensitive:
            search_lower = None
        else:
            search_lower = query.lower()
        
        self.status_var.set("Starting search...")
        self.root.update()
        
        try:
            with pdfplumber.open(self.pdf_file_path) as pdf:
                for i, page_data in enumerate(self.pdf_text_data):
                    if self.cancel_loading:
                        break
                    
                    page_num = page_data['page']
                    
                    # Update progress every 10 pages
                    if i % 10 == 0:
                        progress = (i / total_pages) * 100
                        self.progress_var.set(progress)
                        self.status_var.set(f"Searching page {page_num}/{total_pages}...")
                        self.root.update()
                    
                    try:
                        # Extract text from this page only
                        page = pdf.pages[page_num - 1]
                        
                        # Super fast text extraction with minimal processing
                        text = page.extract_text(layout=False, x_tolerance=3, y_tolerance=3)
                        
                        if not text:
                            continue
                        
                        # Quick check if query exists before detailed processing
                        if case_sensitive:
                            if query not in text:
                                continue
                        else:
                            if search_lower not in text.lower():
                                continue
                        
                        # Found a match - now get better context
                        lines = text.split('\n')
                        
                        # Find all lines containing the search term
                        matching_lines = []
                        for line_idx, line in enumerate(lines):
                            line_check = line if case_sensitive else line.lower()
                            query_check = query if case_sensitive else search_lower
                            
                            if query_check in line_check:
                                # Get context around matching line
                                start_idx = max(0, line_idx - 1)
                                end_idx = min(len(lines), line_idx + 2)
                                context_lines = lines[start_idx:end_idx]
                                context = '\n'.join(context_lines).strip()
                                
                                if context and context not in [r['context'] for r in matching_lines]:
                                    matching_lines.append({
                                        'context': context,
                                        'line_number': line_idx + 1
                                    })
                        
                        # Add all unique contexts from this page
                        for match_info in matching_lines:
                            results.append({
                                'page': page_num,
                                'context': match_info['context'],
                                'line_number': match_info['line_number']
                            })
                    
                    except Exception as e:
                        # Skip problematic pages
                        print(f"Warning: Could not search page {page_num}: {e}")
                        continue
                        
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")
        
        return results

    def search_pdf(self, query: str) -> List[Dict[str, Any]]:
        """Search through PDF content - uses ultra-fast method."""
        # Always use ultra-fast search for instant loading
        return self.search_pdf_ultra_fast(query)
        
    def search_excel(self, query: str) -> List[Dict[str, Any]]:
        """Search through Excel content."""
        selected_columns = self.get_selected_columns()
        
        if not selected_columns:
            messagebox.showwarning("Warning", "Please select at least one column to search.")
            return []
            
        results = []
        case_sensitive = self.case_sensitive_var.get()
        
        # Convert query to appropriate type for numeric searches
        numeric_query = None
        try:
            numeric_query = float(query)
        except ValueError:
            pass
            
        for idx, row in self.excel_data.iterrows():
            match_found = False
            matched_columns = []
            
            for column in selected_columns:
                cell_value = row[column]
                
                # Skip NaN/None values
                if pd.isna(cell_value):
                    continue
                    
                # Convert to string for text search
                cell_str = str(cell_value)
                
                # Perform search
                if case_sensitive:
                    text_match = query in cell_str
                else:
                    text_match = query.lower() in cell_str.lower()
                    
                # Also check for numeric exact match
                numeric_match = False
                if numeric_query is not None and isinstance(cell_value, (int, float)):
                    numeric_match = abs(cell_value - numeric_query) < 1e-10
                    
                if text_match or numeric_match:
                    match_found = True
                    matched_columns.append(column)
                    
            if match_found:
                # Convert row to dictionary and include metadata
                row_dict = row.to_dict()
                results.append({
                    'row_index': idx + 2,  # +2 because Excel is 1-indexed and has header
                    'matched_columns': matched_columns,
                    'data': row_dict
                })
                
        return results
        
    def display_results(self, results: List[Dict[str, Any]], query: str):
        """Display search results in the results text widget."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if not results:
            self.results_text.insert(tk.END, "No matches found.")
            self.results_count_label.config(text="")
            self.export_btn.config(state=tk.DISABLED)
            self.status_var.set("Search completed - No results")
            self.results_text.config(state=tk.DISABLED)
            return
            
        # Display results based on file type
        if self.loaded_file_type == 'pdf':
            self.display_pdf_results(results, query)
        elif self.loaded_file_type == 'excel':
            self.display_excel_results(results, query)
            
        self.results_count_label.config(text=f"{len(results)} result(s) found")
        self.export_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Search completed - {len(results)} results found")
        self.results_text.config(state=tk.DISABLED)
        
    def display_pdf_results(self, results: List[Dict[str, Any]], query: str):
        """Display PDF search results."""
        self.results_text.insert(tk.END, f"PDF Search Results for: '{query}'\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, result in enumerate(results, 1):
            self.results_text.insert(tk.END, f"Result #{i} - Page {result['page']}:\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")
            self.results_text.insert(tk.END, result['context'])
            self.results_text.insert(tk.END, "\n\n")
            
    def display_excel_results(self, results: List[Dict[str, Any]], query: str):
        """Display Excel search results."""
        self.results_text.insert(tk.END, f"Excel Search Results for: '{query}'\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Get all column names for display
        all_columns = list(self.excel_data.columns)
        
        for i, result in enumerate(results, 1):
            self.results_text.insert(tk.END, f"Result #{i} - Row {result['row_index']}:\n")
            self.results_text.insert(tk.END, f"Matched columns: {', '.join(result['matched_columns'])}\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")
            
            # Display all columns of the matched row
            for col in all_columns:
                value = result['data'][col]
                # Highlight matched columns
                if col in result['matched_columns']:
                    self.results_text.insert(tk.END, f"★ {col}: {value}\n")
                else:
                    self.results_text.insert(tk.END, f"  {col}: {value}\n")
                    
            self.results_text.insert(tk.END, "\n")
            
    def clear_results(self):
        """Clear the results display."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.results_count_label.config(text="")
        self.export_btn.config(state=tk.DISABLED)
        
    def export_results(self):
        """Export search results to a file."""
        if not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("Warning", "No results to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")
                
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main function to run the application."""
    try:
        # Check for required dependencies
        import pandas as pd
        import pdfplumber
    except ImportError as e:
        error_msg = f"""
Missing required dependency: {e}

Please install the required packages:
pip install pandas openpyxl pdfplumber

Then run the application again.
"""
        print(error_msg)
        # Try to show GUI error if tkinter is available
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Missing Dependencies", error_msg)
        except:
            pass
        return
        
    # Create and run the application
    app = FileSearchApp()
    app.run()


if __name__ == "__main__":
    main()
