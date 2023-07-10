import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
sys.path.insert(0, '.\vendor')
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

# Function to add image to PDF
def add_image_to_pdf(pdf_path, image_path, target_size):
    # Open PDF and create output writer
    pdf = PdfReader(pdf_path)
    output = PdfWriter()

    # Load image and resize
    image = Image.open(image_path)
    image.thumbnail(target_size)

    # Get dimensions of the first page
    first_page = pdf.pages[0]
    page_width = first_page.mediabox.upper_right[0]
    page_height = first_page.mediabox.upper_right[1]

    # Calculate the position to paste the image
    image_width, image_height = image.size
    x = page_width - image_width
    y = 0

    # Create a new PDF page with the image
    image_page = canvas.Canvas("temp.pdf", pagesize=(image_width, image_height))
    image_page.drawImage(image_path, 0, 0, width=image_width, height=image_height)
    image_page.save()

    # Merge the image page with the first page
    merged_page = PdfReader("temp.pdf").pages[0]
    first_page.merge_page(merged_page)
    output.add_page(first_page)

    # Add the remaining pages
    for page in pdf.pages[1:]:
        output.add_page(page)

    # Save the modified PDF
    output_path = os.path.join(output_folder, os.path.basename(pdf_path))
    with open(output_path, 'wb') as f:
        output.write(f)

    messagebox.showinfo("Image Added", "Image added to {}".format(pdf_path))

def select_pdf_folder():
    global pdf_folder
    pdf_folder = filedialog.askdirectory()
    pdf_folder_entry.delete(0, tk.END)
    pdf_folder_entry.insert(0, pdf_folder)

def select_image_folder():
    global image_folder
    image_folder = filedialog.askdirectory()
    image_folder_entry.delete(0, tk.END)
    image_folder_entry.insert(0, image_folder)

def select_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, output_folder)

def ask_for_image(pdf_file):
    image_choice = messagebox.askquestion("Image Selection", "Would you like to select an image file for {}?".format(pdf_file[:-4]))
    if image_choice == 'yes':
        image_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        return image_file
    else:
        image_name = image_name = simpledialog.askstring("Image Name", "Enter the name of the image file for {}:".format(pdf_file[:-4]))
        if image_name:
            image_path = os.path.join(image_folder, image_name + ".jpg")  # assuming the image is in jpg format
            return image_path

def add_images_to_pdfs():
    global output_folder
    pdf_folder = pdf_folder_entry.get()
    image_folder = image_folder_entry.get()
    output_folder = output_folder_entry.get()

    # Specify the target image size (width, height)
    target_size = (200, 200)  # Adjust as needed

    # Main script
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith(".pdf") and pdf_file.startswith("IMP"):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            image_path = ask_for_image(pdf_file)
            if image_path:
                add_image_to_pdf(pdf_path, image_path, target_size)

# Create the GUI window
window = tk.Tk()
window.title("Add Images to PDFs")

# Create and position the widgets
pdf_folder_label = tk.Label(window, text="PDF Folder:")
pdf_folder_label.grid(row=0, column=0, sticky=tk.W)
pdf_folder_entry = tk.Entry(window, width=50)
pdf_folder_entry.grid(row=0, column=1)
pdf_folder_button = tk.Button(window, text="Select Folder", command=select_pdf_folder)
pdf_folder_button.grid(row=0, column=2)

image_folder_label = tk.Label(window, text="Image Folder:")
image_folder_label.grid(row=1, column=0, sticky=tk.W)
image_folder_entry = tk.Entry(window, width=50)
image_folder_entry.grid(row=1, column=1)
image_folder_button = tk.Button(window, text="Select Folder", command=select_image_folder)
image_folder_button.grid(row=1, column=2)

output_folder_label = tk.Label(window, text="Output Folder:")
output_folder_label.grid(row=2, column=0, sticky=tk.W)
output_folder_entry = tk.Entry(window, width=50)
output_folder_entry.grid(row=2, column=1)
output_folder_button = tk.Button(window, text="Select Folder", command=select_output_folder)
output_folder_button.grid(row=2, column=2)

add_images_button = tk.Button(window, text="Add Images to PDFs", command=add_images_to_pdfs)
add_images_button.grid(row=3, column=1, pady=10)

# Start the GUI event loop
window.mainloop()
