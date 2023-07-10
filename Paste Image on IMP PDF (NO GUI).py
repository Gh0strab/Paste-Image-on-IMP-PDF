import os
import sys
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

    print("Image added to", pdf_path)

# Specify the folder paths
pdf_folder = input(r"Please input the PDF folder path: ")
image_folder = input(r"Please input the Image folder path: ")
output_folder = input(r"Please input the Output folder path: ")

# Specify the target image size (width, height)
target_size = (200, 200)  # Adjust as needed

# Main script
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf") and pdf_file.startswith("IMP"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        image_name = input("Enter the name of the image file for {}: ".format(pdf_file[:-4]))
        if not image_name:
            break
        image_path = os.path.join(image_folder, image_name + ".jpg")  # assuming the image is in jpg format
        add_image_to_pdf(pdf_path, image_path, target_size)
