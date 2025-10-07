import tkinter as tk
from tkinter import filedialog
import os

class ImageToPFConverter:
    def __init__(self, root):
        self.root = root
        self.image_path = []
        self.output_pdf_name = tk.StringVar()   
        self.select_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.instialize_ui()

