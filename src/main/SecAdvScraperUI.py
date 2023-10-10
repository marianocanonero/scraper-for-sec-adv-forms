import tkinter as tk
from tkinter import filedialog, messagebox
import os
from SecAdvScraper import SecAdvScraper as SAS

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Data Extractor")
        self.resizable(0, 0)
        self.geometry("531x113")      
        self.create_widgets()

    def create_widgets(self):

        # Create label for URL
        url_label = tk.Label(self, text="Enter URL:")
        url_label.grid(row=0, column=0, columnspan=4, sticky='w')

        # Create text box for URL
        self.url_textbox = tk.Entry(self, width=88)
        self.url_textbox.grid(row=1, column=0, columnspan=4, sticky='w')

        # Create label for select path button
        path_label = tk.Label(self, text="Save to:")
        path_label.grid(row=4, column=0, columnspan=4, sticky='w')

        # Create button to select path
        self.select_path_button = tk.Button(self, text="Select", command=self.select_path, bg="grey70")
        self.select_path_button.grid(row=5, column=0, sticky='w')

        # Create text box for path
        self.path_textbox = tk.Entry(self, width=80)
        self.path_textbox.grid(row=5, column=1, columnspan=3, sticky='w')

        # Create button to extract data
        reset_button = tk.Button(self, text="Reset", command=self.reset, bg="IndianRed1")
        reset_button.grid(row=6, column=0, columnspan=2, sticky='nesw')

        # Create button to extract data
        extract_button = tk.Button(self, text="Extract Data", command=self.extract_data, bg="grey70")
        extract_button.grid(row=6, column=2, columnspan=2, sticky='nesw')

    def reset(self):
        self.url_textbox.config(state="normal", bg="white")
        self.url_textbox.delete(0, tk.END)

    def select_path(self):
        # Show file dialog to select path
        path = filedialog.askdirectory()
        self.path = path
        self.path_textbox.delete(0, tk.END)
        self.path_textbox.insert(0, self.path)

    def validate_inputs(self):

        self.output_path = self.path_textbox.get().strip()
        self.url = self.url_textbox.get().strip()

        # Check if URL and path are selected
        if not self.output_path:
            tk.messagebox.showwarning("Warning", "Please select a path to save the file.")
            return
        if not self.url:
            tk.messagebox.showwarning("Warning", "Please enter a URL.")
            return

    def extract_data(self):

        try:
            self.validate_inputs()
            scraper = SAS(self.url)
            scraper.WriteToExcel(self.output_path)
            fileName = getattr(scraper, 'fileName')
            tk.messagebox.showinfo("Success", "SUCCESS\n\nFile: " + fileName + "\nSaved at: " + self.output_path)

        except:
            tk.messagebox.showerror("Error", "ERROR\n\nValidate inputs")
        

# Run the app
app = App()
app.mainloop()
