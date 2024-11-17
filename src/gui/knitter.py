import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import yaml
from utils.path_finder import PathFinder
import queue
from threading import Thread

class RmdKnitter:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("R Markdown Knitter")
        self.root.geometry("800x800")
        
        # Variables to store paths
        self.working_dir = ""
        self.rmd_file = ""
        
        # Load configuration
        self.load_config()
        
        # Add console queue
        self.console_queue = queue.Queue()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text="R Markdown Knitter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Working Directory Selection
        dir_frame = ctk.CTkFrame(self.main_frame)
        dir_frame.pack(fill="x", padx=20, pady=10)
        
        self.dir_label = ctk.CTkLabel(
            dir_frame, 
            text="No working directory selected",
            font=ctk.CTkFont(size=12)
        )
        self.dir_label.pack(side="left", padx=10)
        
        dir_button = ctk.CTkButton(
            dir_frame,
            text="Browse Directory",
            command=self.select_directory,
            width=150
        )
        dir_button.pack(side="right", padx=10)
        
        # Rmd File Selection
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        self.file_label = ctk.CTkLabel(
            file_frame, 
            text="No .Rmd file selected",
            font=ctk.CTkFont(size=12)
        )
        self.file_label.pack(side="left", padx=10)
        
        file_button = ctk.CTkButton(
            file_frame,
            text="Select Rmd File",
            command=self.select_file,
            width=150
        )
        file_button.pack(side="right", padx=10)
        
        # Settings Button
        settings_button = ctk.CTkButton(
            self.main_frame,
            text="Settings",
            command=self.show_settings,
            width=150
        )
        settings_button.pack(pady=10)
        
        # Knit Button
        knit_button = ctk.CTkButton(
            self.main_frame,
            text="Knit to HTML",
            command=self.knit_document,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        knit_button.pack(pady=20)
        
        # Add console output area
        self.console_widget = ctk.CTkTextbox(
            self.main_frame,
            wrap='word',
            height=400,
            font=('Courier', 14)
        )
        self.console_widget.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Start console update loop
        self.root.after(100, self.update_console)

    def update_console(self):
        """Update console widget with queued output"""
        try:
            while True:
                text = self.console_queue.get_nowait()
                self.console_widget.insert('end', text)
                self.console_widget.see('end')
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.update_console)

    def load_config(self):
        """Load configuration or create with detected paths"""
        try:
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            pandoc_path = PathFinder.find_rstudio_pandoc()
            rscript_path = PathFinder.find_rscript()
            
            if not pandoc_path or not rscript_path:
                messagebox.showwarning(
                    "Configuration Required",
                    "Could not automatically detect R or Pandoc paths.\n"
                    "Please set them manually in the settings."
                )
            
            self.config = {
                'paths': {
                    'rstudio_pandoc': pandoc_path,
                    'rscript': rscript_path
                }
            }
            with open('config.yaml', 'w') as f:
                yaml.dump(self.config, f)

    def show_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("800x400")  # Increased width for browse buttons
        settings_window.transient(self.root)  # Makes window stay on top of main window
        settings_window.grab_set()  # Makes the window modal
        
        # Pandoc Path
        pandoc_label = ctk.CTkLabel(
            settings_window,
            text="Pandoc Path (Used for converting R Markdown to HTML)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        pandoc_label.pack(anchor="w", padx=20, pady=(20,5))
        
        pandoc_frame = ctk.CTkFrame(settings_window)
        pandoc_frame.pack(fill="x", padx=20, pady=(0,10))
        
        pandoc_entry = ctk.CTkEntry(
            pandoc_frame, 
            width=600,
            placeholder_text=self.config['paths']['rstudio_pandoc']
        )
        pandoc_entry.pack(side="left", padx=10, pady=5)
        
        def browse_pandoc():
            path = filedialog.askdirectory()
            if path:
                pandoc_entry.delete(0, 'end')
                pandoc_entry.insert(0, path)
        
        pandoc_browse = ctk.CTkButton(
            pandoc_frame,
            text="Browse",
            width=100,
            command=browse_pandoc
        )
        pandoc_browse.pack(side="right", padx=10)
        
        # RScript Path
        rscript_label = ctk.CTkLabel(
            settings_window,
            text="RScript Path (R executable for running R Markdown)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        rscript_label.pack(anchor="w", padx=20, pady=(20,5))
        
        rscript_frame = ctk.CTkFrame(settings_window)
        rscript_frame.pack(fill="x", padx=20, pady=(0,10))
        
        rscript_entry = ctk.CTkEntry(
            rscript_frame, 
            width=600,
            placeholder_text=self.config['paths']['rscript']
        )
        rscript_entry.pack(side="left", padx=10, pady=5)
        
        def browse_rscript():
            path = filedialog.askopenfilename(
                filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
            )
            if path:
                rscript_entry.delete(0, 'end')
                rscript_entry.insert(0, path)
        
        rscript_browse = ctk.CTkButton(
            rscript_frame,
            text="Browse",
            width=100,
            command=browse_rscript
        )
        rscript_browse.pack(side="right", padx=10)
        
        def save_settings():
            self.config['paths']['rstudio_pandoc'] = pandoc_entry.get()
            self.config['paths']['rscript'] = rscript_entry.get()
            with open('config.yaml', 'w') as f:
                yaml.dump(self.config, f)
            settings_window.destroy()
        
        save_button = ctk.CTkButton(
            settings_window,
            text="Save",
            command=save_settings,
            width=200
        )
        save_button.pack(pady=20)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.working_dir = directory
            self.dir_label.configure(text=f"Directory: {directory}")

    def select_file(self):
        file = filedialog.askopenfilename(filetypes=[("R Markdown Files", "*.Rmd")])
        if file:
            self.rmd_file = file
            self.file_label.configure(text=f"File: {os.path.basename(file)}")

    def knit_document(self):
        if not self.working_dir or not self.rmd_file:
            messagebox.showerror("Error", "Please select both working directory and Rmd file")
            return
            
        try:
            env = os.environ.copy()
            env['RSTUDIO_PANDOC'] = self.config['paths']['rstudio_pandoc']
            
            rscript_path = self.config['paths']['rscript']
            rmd_file = os.path.basename(self.rmd_file)
            
            command = [
                rscript_path,
                "-e",
                f"rmarkdown::render('{rmd_file}', output_format='html_document')"
            ]
            
            def run_knit():
                process = subprocess.Popen(
                    command,
                    cwd=self.working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.console_queue.put(output)
                
                return_code = process.poll()
                
                if return_code == 0:
                    self.console_queue.put("\nDocument knitted successfully!\n")
                else:
                    error = process.stderr.read()
                    self.console_queue.put(f"\nError during knitting:\n{error}\n")
            
            # Run knitting in separate thread
            Thread(target=run_knit, daemon=True).start()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")