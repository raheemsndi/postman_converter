import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

class PostmanConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Postman Collection Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.collection_path = tk.StringVar(value="d:/printify_postman_collection.json")
        self.output_path = tk.StringVar()
        self.format_var = tk.StringVar(value="md")  # Default to Markdown
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Postman Collection Converter", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Collection file selection
        collection_frame = tk.LabelFrame(main_frame, text="Postman Collection File", padx=10, pady=10)
        collection_frame.pack(fill=tk.X, pady=(0, 15))
        
        collection_entry_frame = tk.Frame(collection_frame)
        collection_entry_frame.pack(fill=tk.X)
        
        tk.Entry(collection_entry_frame, textvariable=self.collection_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(collection_entry_frame, text="Browse", command=self.browse_collection).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Output directory selection
        output_frame = tk.LabelFrame(main_frame, text="Output Directory", padx=10, pady=10)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_entry_frame = tk.Frame(output_frame)
        output_entry_frame.pack(fill=tk.X)
        
        tk.Entry(output_entry_frame, textvariable=self.output_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(output_entry_frame, text="Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Format selection
        format_frame = tk.LabelFrame(main_frame, text="Output Format", padx=10, pady=10)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        format_container = tk.Frame(format_frame)
        format_container.pack()
        
        tk.Radiobutton(format_container, text="Plain Text (.txt)", variable=self.format_var, value="txt").pack(anchor=tk.W)
        tk.Radiobutton(format_container, text="JSON (.json)", variable=self.format_var, value="json").pack(anchor=tk.W)
        tk.Radiobutton(format_container, text="Markdown (.md)", variable=self.format_var, value="md").pack(anchor=tk.W)
        
        # Convert button
        convert_btn = tk.Button(main_frame, text="Convert Collection", 
                               command=self.convert, bg="#4CAF50", fg="white",
                               font=("Arial", 12, "bold"), height=2)
        convert_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # Log area
        log_frame = tk.LabelFrame(main_frame, text="Process Log", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=12)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_collection(self):
        filename = filedialog.askopenfilename(
            initialdir="d:/",
            title="Select Postman Collection",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.collection_path.set(filename)
            self.status_var.set(f"Selected collection: {os.path.basename(filename)}")
            
    def browse_output(self):
        directory = filedialog.askdirectory(initialdir="d:/", title="Select Output Directory")
        if directory:
            self.output_path.set(directory)
            self.status_var.set(f"Selected output directory: {os.path.basename(directory)}")
            
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()
        
    def sanitize_name(self, name):
        """Remove invalid characters for folder/file names"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
        
    def save_request_txt(self, item, folder_path, name):
        """Save request details to a TXT file"""
        if 'request' not in item:
            return
            
        request = item['request']
        filename = f"{name}.txt"
        filepath = os.path.join(folder_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"API Endpoint: {name}\n")
                f.write("=" * 50 + "\n")
                f.write(f"Method: {request.get('method', 'N/A')}\n")
                f.write(f"URL: {request.get('url', {}).get('raw', 'N/A')}\n\n")
                
                description = request.get('description', '').strip()
                if description:
                    f.write("Description:\n")
                    f.write(description + "\n\n")
                    
                # Headers
                headers = request.get('header', [])
                if headers:
                    f.write("Headers:\n")
                    for header in headers:
                        key = header.get('key', '')
                        value = header.get('value', '')
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
                    
                # Body (if present)
                body = request.get('body')
                if body:
                    f.write("Body:\n")
                    if body.get('mode') == 'raw':
                        f.write(body.get('raw', '') + "\n")
                    f.write("\n")
                    
            self.log(f"Saved TXT: {name}")
        except Exception as e:
            self.log(f"Error saving TXT {name}: {str(e)}")
            
    def save_request_json(self, item, folder_path, name):
        """Save request details to a JSON file"""
        filename = f"{name}.json"
        filepath = os.path.join(folder_path, filename)
        
        try:
            # Pretty print the entire item
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(item, f, indent=2, ensure_ascii=False)
            self.log(f"Saved JSON: {name}")
        except Exception as e:
            self.log(f"Error saving JSON {name}: {str(e)}")
            
    def save_request_md(self, item, folder_path, name):
        """Save request details to a Markdown file"""
        if 'request' not in item:
            return
            
        request = item['request']
        filename = f"{name}.md"
        filepath = os.path.join(folder_path, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {name}\n\n")
                f.write(f"**Method:** `{request.get('method', 'N/A')}`  \n")
                f.write(f"**URL:** `{request.get('url', {}).get('raw', 'N/A')}`\n\n")
                
                description = request.get('description', '').strip()
                if description:
                    f.write(f"## Description\n{description}\n\n")
                    
                # Headers
                headers = request.get('header', [])
                if headers:
                    f.write("## Headers\n")
                    f.write("| Key | Value |\n|-----|-------|\n")
                    for header in headers:
                        key = header.get('key', '')
                        value = header.get('value', '')
                        f.write(f"| {key} | {value} |\n")
                    f.write("\n")
                    
                # Body (if present)
                body = request.get('body')
                if body:
                    f.write("## Body\n")
                    if body.get('mode') == 'raw':
                        raw_body = body.get('raw', '')
                        f.write("```json\n")
                        f.write(raw_body + "\n")
                        f.write("```\n")
                    f.write("\n")
                    
            self.log(f"Saved MD: {name}")
        except Exception as e:
            self.log(f"Error saving MD {name}: {str(e)}")
            
    def process_item(self, item, current_path, format_type):
        """Process a collection item (folder or request)"""
        name = self.sanitize_name(item.get('name', 'unnamed'))
        
        if 'item' in item:
            # This is a folder
            folder_path = os.path.join(current_path, name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                self.log(f"Created folder: {name}")
                
            # Process children
            for child in item['item']:
                self.process_item(child, folder_path, format_type)
        else:
            # This is a request
            # Save in the specified format only
            if format_type == 'txt':
                self.save_request_txt(item, current_path, name)
            elif format_type == 'json':
                self.save_request_json(item, current_path, name)
            elif format_type == 'md':
                self.save_request_md(item, current_path, name)
                
    def convert(self):
        """Main conversion function"""
        self.log_area.delete(1.0, tk.END)
        
        collection_file = self.collection_path.get().strip()
        output_dir = self.output_path.get().strip()
        format_type = self.format_var.get()
        
        # Validation
        if not collection_file:
            messagebox.showerror("Error", "Please select a Postman collection file.")
            return
            
        if not os.path.exists(collection_file):
            messagebox.showerror("Error", f"Collection file not found:\n{collection_file}")
            return
            
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
            
        try:
            self.status_var.set("Converting...")
            self.progress.start()
            self.root.update_idletasks()
            
            self.log("Starting conversion...")
            self.log(f"Collection: {collection_file}")
            self.log(f"Output: {output_dir}")
            self.log(f"Format: {format_type.upper()}")
            self.log("-" * 50)
            
            # Load collection
            with open(collection_file, 'r', encoding='utf-8') as f:
                collection = json.load(f)
                
            collection_name = collection.get('info', {}).get('name', 'PostmanCollection')
            self.log(f"Loaded collection: {collection_name}")
            
            # Create main output directory
            main_output_dir = os.path.join(output_dir, self.sanitize_name(collection_name))
            os.makedirs(main_output_dir, exist_ok=True)
            self.log(f"Created main directory: {os.path.basename(main_output_dir)}")
            
            # Process items
            if 'item' in collection:
                for item in collection['item']:
                    self.process_item(item, main_output_dir, format_type)
                    
            self.log("-" * 50)
            self.log("Conversion completed successfully!")
            self.status_var.set("Conversion completed!")
            messagebox.showinfo("Success", "Collection converted successfully!")
            
        except json.JSONDecodeError as e:
            error = f"Invalid JSON in collection file: {str(e)}"
            self.log(error)
            messagebox.showerror("Error", error)
        except Exception as e:
            error = f"Conversion failed: {str(e)}"
            self.log(error)
            messagebox.showerror("Error", error)
        finally:
            self.progress.stop()
            self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = PostmanConverterGUI(root)
    root.mainloop()