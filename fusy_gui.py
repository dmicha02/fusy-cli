import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from ttkthemes import ThemedTk

class FusyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fusy - PDF Manipulation Tool")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Set styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TNotebook", background="#f0f0f0")
        self.style.configure("TNotebook.Tab", padding=[12, 6], font=("Arial", 10))
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create tabs
        self.merge_tab = ttk.Frame(self.notebook)
        self.split_tab = ttk.Frame(self.notebook)
        self.extract_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.merge_tab, text="Merge PDFs")
        self.notebook.add(self.split_tab, text="Split PDF")
        self.notebook.add(self.extract_tab, text="Extract Pages")
        
        # Initialize tabs
        self.setup_merge_tab()
        self.setup_split_tab()
        self.setup_extract_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_merge_tab(self):
        # File selection frame
        file_frame = ttk.Frame(self.merge_tab)
        file_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Files listbox with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=10)
        self.files_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        buttons_frame = ttk.Frame(file_frame)
        buttons_frame.pack(fill="x", pady=5)
        
        add_button = ttk.Button(buttons_frame, text="Add Files", command=self.add_files)
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = ttk.Button(buttons_frame, text="Remove Selected", command=self.remove_files)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        move_up_button = ttk.Button(buttons_frame, text="Move Up", command=self.move_up)
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(buttons_frame, text="Move Down", command=self.move_down)
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        # Output file selection
        output_frame = ttk.Frame(self.merge_tab)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT, padx=5)
        
        self.merge_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.merge_output_var, width=40)
        output_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        browse_button = ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_output(self.merge_output_var))
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Merge button
        merge_button = ttk.Button(self.merge_tab, text="Merge PDFs", command=self.merge_pdfs)
        merge_button.pack(pady=20)
    
    def setup_split_tab(self):
        # Input file selection
        input_frame = ttk.Frame(self.split_tab)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Input PDF:").pack(side=tk.LEFT, padx=5)
        
        self.split_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.split_input_var, width=40)
        input_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        browse_button = ttk.Button(input_frame, text="Browse...", command=self.browse_input_split)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Page ranges
        page_frame = ttk.Frame(self.split_tab)
        page_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(page_frame, text="Start Page:").pack(side=tk.LEFT, padx=5)
        
        self.start_page_var = tk.StringVar()
        start_page_entry = ttk.Entry(page_frame, textvariable=self.start_page_var, width=5)
        start_page_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(page_frame, text="End Page:").pack(side=tk.LEFT, padx=5)
        
        self.end_page_var = tk.StringVar()
        end_page_entry = ttk.Entry(page_frame, textvariable=self.end_page_var, width=5)
        end_page_entry.pack(side=tk.LEFT, padx=5)
        
        # PDF info
        self.pdf_info_var = tk.StringVar()
        self.pdf_info_var.set("PDF Info: No file selected")
        pdf_info_label = ttk.Label(self.split_tab, textvariable=self.pdf_info_var)
        pdf_info_label.pack(pady=5)
        
        # Output file selection
        output_frame = ttk.Frame(self.split_tab)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File Prefix:").pack(side=tk.LEFT, padx=5)
        
        self.split_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.split_output_var, width=40)
        output_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        browse_button = ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_output_dir(self.split_output_var))
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Split button
        split_button = ttk.Button(self.split_tab, text="Split PDF", command=self.split_pdf)
        split_button.pack(pady=20)
    
    def setup_extract_tab(self):
        # Input file selection
        input_frame = ttk.Frame(self.extract_tab)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Input PDF:").pack(side=tk.LEFT, padx=5)
        
        self.extract_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.extract_input_var, width=40)
        input_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        browse_button = ttk.Button(input_frame, text="Browse...", command=self.browse_input_extract)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Pages to extract
        page_frame = ttk.Frame(self.extract_tab)
        page_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(page_frame, text="Pages to Extract:").pack(side=tk.LEFT, padx=5)
        
        self.pages_var = tk.StringVar()
        pages_entry = ttk.Entry(page_frame, textvariable=self.pages_var, width=30)
        pages_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        ttk.Label(page_frame, text="(e.g., 1,3,5-7)").pack(side=tk.LEFT, padx=5)
        
        # PDF info
        self.extract_pdf_info_var = tk.StringVar()
        self.extract_pdf_info_var.set("PDF Info: No file selected")
        pdf_info_label = ttk.Label(self.extract_tab, textvariable=self.extract_pdf_info_var)
        pdf_info_label.pack(pady=5)
        
        # Output file selection
        output_frame = ttk.Frame(self.extract_tab)
        output_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT, padx=5)
        
        self.extract_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.extract_output_var, width=40)
        output_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        browse_button = ttk.Button(output_frame, text="Browse...", command=lambda: self.browse_output(self.extract_output_var))
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Extract button
        extract_button = ttk.Button(self.extract_tab, text="Extract Pages", command=self.extract_pages)
        extract_button.pack(pady=20)
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        for file in files:
            self.files_listbox.insert(tk.END, file)
    
    def remove_files(self):
        selected = self.files_listbox.curselection()
        for index in selected[::-1]:  # Reverse to avoid index issues
            self.files_listbox.delete(index)
    
    def move_up(self):
        selected = self.files_listbox.curselection()
        if not selected or selected[0] == 0:
            return
        
        for index in selected:
            text = self.files_listbox.get(index)
            self.files_listbox.delete(index)
            self.files_listbox.insert(index - 1, text)
            self.files_listbox.selection_set(index - 1)
    
    def move_down(self):
        selected = self.files_listbox.curselection()
        if not selected or selected[-1] == self.files_listbox.size() - 1:
            return
        
        for index in selected[::-1]:  # Reverse to avoid index issues
            text = self.files_listbox.get(index)
            self.files_listbox.delete(index)
            self.files_listbox.insert(index + 1, text)
            self.files_listbox.selection_set(index + 1)
    
    def browse_input_split(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.split_input_var.set(filename)
            try:
                reader = PdfReader(filename)
                self.pdf_info_var.set(f"PDF Info: {len(reader.pages)} pages")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read PDF file: {e}")
    
    def browse_input_extract(self):
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.extract_input_var.set(filename)
            try:
                reader = PdfReader(filename)
                self.extract_pdf_info_var.set(f"PDF Info: {len(reader.pages)} pages")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read PDF file: {e}")
    
    def browse_output(self, var):
        filename = filedialog.asksaveasfilename(
            title="Save PDF file",
            filetypes=[("PDF files", "*.pdf")],
            defaultextension=".pdf"
        )
        if filename:
            var.set(filename)
    
    def browse_output_dir(self, var):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            filename = filedialog.askstring("File Prefix", "Enter output file prefix:")
            if filename:
                var.set(os.path.join(directory, filename))
    
    def parse_page_ranges(self, page_ranges):
        """Parse a string of page ranges into a list of integers."""
        pages = set()
        ranges = page_ranges.split(',')
        for r in ranges:
            if '-' in r:
                start, end = map(int, r.split('-'))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(r))
        return sorted(pages)
    
    def merge_pdfs(self):
        files = list(self.files_listbox.get(0, tk.END))
        output_file = self.merge_output_var.get()
        
        if not files:
            messagebox.showerror("Error", "No files selected for merging")
            return
        
        if not output_file:
            messagebox.showerror("Error", "No output file specified")
            return
        
        try:
            merger = PdfMerger()
            
            for pdf in files:
                merger.append(pdf)
            
            # Make sure output has .pdf extension
            if not output_file.lower().endswith('.pdf'):
                output_file += '.pdf'
                
            merger.write(output_file)
            merger.close()
            
            self.status_var.set(f"Merged {len(files)} PDFs into {output_file}")
            messagebox.showinfo("Success", f"Successfully merged {len(files)} PDFs into {output_file}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Could not merge PDFs: {str(e)}")
    
    def split_pdf(self):
        input_file = self.split_input_var.get()
        output_prefix = self.split_output_var.get()
        start_page = self.start_page_var.get()
        end_page = self.end_page_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "No input file selected")
            return
        
        if not output_prefix:
            messagebox.showerror("Error", "No output file prefix specified")
            return
        
        try:
            start_page = int(start_page)
            end_page = int(end_page)
        except ValueError:
            messagebox.showerror("Error", "Start and end page must be integers")
            return
        
        try:
            reader = PdfReader(input_file)
            
            if start_page < 1 or end_page > len(reader.pages) or start_page > end_page:
                messagebox.showerror("Error", "Invalid page range")
                return
            
            for page in range(start_page - 1, end_page):
                writer = PdfWriter()
                writer.add_page(reader.pages[page])
                
                page_output = f"{output_prefix}_{page + 1}.pdf"
                with open(page_output, "wb") as f:
                    writer.write(f)
            
            self.status_var.set(f"Split {input_file} from page {start_page} to {end_page}")
            messagebox.showinfo("Success", f"Successfully split {input_file} into individual pages")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Could not split PDF: {str(e)}")
    
    def extract_pages(self):
        input_file = self.extract_input_var.get()
        output_file = self.extract_output_var.get()
        pages_str = self.pages_var.get()
        
        if not input_file:
            messagebox.showerror("Error", "No input file selected")
            return
        
        if not output_file:
            messagebox.showerror("Error", "No output file specified")
            return
        
        if not pages_str:
            messagebox.showerror("Error", "No pages specified")
            return
        
        try:
            pages = self.parse_page_ranges(pages_str)
            
            if not pages:
                messagebox.showerror("Error", "Invalid page specification")
                return
            
            reader = PdfReader(input_file)
            writer = PdfWriter()
            
            for page in pages:
                if page < 1 or page > len(reader.pages):
                    messagebox.showerror("Error", f"Page {page} out of range")
                    return
                writer.add_page(reader.pages[page - 1])
            
            # Make sure output has .pdf extension
            if not output_file.lower().endswith('.pdf'):
                output_file += '.pdf'
                
            with open(output_file, "wb") as f:
                writer.write(f)
            
            self.status_var.set(f"Extracted pages {pages_str} from {input_file}")
            messagebox.showinfo("Success", f"Successfully extracted pages to {output_file}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Could not extract pages: {str(e)}")

if __name__ == "__main__":
    # root = tk.Tk()
    root = ThemedTk(theme="adapta")
    app = FusyGUI(root)
    root.mainloop()