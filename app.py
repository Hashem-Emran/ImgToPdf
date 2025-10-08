import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root): 
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()   
        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_button.pack(pady=5)

        self.select_images_listbox = tk.Listbox(self.root, width=50, height=8, selectmode=tk.MULTIPLE)
        self.select_images_listbox.pack(pady=5)

        name_frame = tk.Frame(self.root)
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Output PDF name: ").pack(side=tk.LEFT)
        tk.Entry(name_frame, textvariable=self.output_pdf_name, width=25).pack(side=tk.LEFT)

        convert_button = tk.Button(self.root, text="Convert to PDF", bg="#4CAF50", fg="white", command=self.convert_to_pdf)
        convert_button.pack(pady=10)

        clear_button = tk.Button(self.root, text="Clear List", bg="#f44336", fg="white", command=self.clear_list)
        clear_button.pack(pady=5)

    def select_images(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        files = filedialog.askopenfilenames(title="Select Images", filetypes=filetypes)
        if files:
            for f in files:
                if f not in self.image_paths:
                    self.image_paths.append(f)
                    self.select_images_listbox.insert(tk.END, os.path.basename(f))

    def convert_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please select at least one image.")
            return

        output_name = self.output_pdf_name.get().strip()
        if not output_name:
            messagebox.showwarning("Missing Name", "Please enter a name for the output PDF.")
            return

        if not output_name.lower().endswith(".pdf"):
            output_name += ".pdf"

        # Ask where to save
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=output_name,
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF As"
        )
        if not output_path:
            return

        try:
            pdf_images = []

            # A4 page size in pixels (at 300 DPI)
            a4_width, a4_height = 2480, 3508

            for img_path in self.image_paths:
                img = Image.open(img_path).convert("RGB")

                # Resize to fit A4 while keeping aspect ratio
                img.thumbnail((a4_width, a4_height), Image.Resampling.LANCZOS)

                # Create blank white A4 background
                background = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))

                # Center the image
                x = (a4_width - img.width) // 2
                y = (a4_height - img.height) // 2
                background.paste(img, (x, y))

                pdf_images.append(background)

            # Save to PDF
            pdf_images[0].save(output_path, save_all=True, append_images=pdf_images[1:])
            messagebox.showinfo("Success", f"PDF created successfully:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert images.\n{e}")

    def clear_list(self):
        self.image_paths.clear()
        self.select_images_listbox.delete(0, tk.END)


def main():
    root = tk.Tk()
    root.title("Image to PDF Converter")
    root.geometry("450x500")
    app = ImageToPDFConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
