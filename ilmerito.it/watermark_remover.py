import cv2
import fitz
import numpy as np
from pdf2image import convert_from_path
import os
from PIL import Image, ImageDraw

# Convert PDF to images
def pdf_to_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, img in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        img.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

# Remove watermark using OpenCV
def remove_watermark(image_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define watermark color range (tolerance around (193,193,193) in RGB)
    lower_bound = np.array([0, 0, 160])   # Light gray lower bound
    upper_bound = np.array([180, 60, 250]) # Light gray upper bound

    # Create a mask for watermark
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply inpainting to remove watermark
    result = cv2.inpaint(img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

    # Save the cleaned image
    cleaned_path = image_path.replace(".png", "_cleaned.png")
    cv2.imwrite(cleaned_path, result)
    return cleaned_path

# Convert images back to PDF
def images_to_pdf(image_paths, output_pdf):
    images = [Image.open(img).convert("RGB") for img in image_paths]
    images[0].save(output_pdf, save_all=True, append_images=images[1:])

# Main function
def process_pdf(input_pdf, output_pdf, temp_folder="temp_images"):
    os.makedirs(temp_folder, exist_ok=True)

    # Convert PDF to images
    image_paths = pdf_to_images(input_pdf, temp_folder)

    # Remove watermark from each image
    cleaned_paths = [remove_watermark(img) for img in image_paths]

    # Convert back to PDF
    images_to_pdf(cleaned_paths, output_pdf)

    print(f"Watermark removed! Saved as {output_pdf}")

# Run the script
input_pdf = "ilmerito.it.pdf"  # Replace with your PDF path
output_pdf = "cleaned_document.pdf"
final_pdf = "final.pdf"
process_pdf(input_pdf, output_pdf)
doc = fitz.open(output_pdf)
images = []
for page_num in range(len(doc)):
    # Convert page to image
    pix = doc[page_num].get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Draw a white rectangle at (0,0) to (400,100)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 580, 170], fill=(255, 255, 255))
    
    images.append(img)

# Save modified images back to a new PDF
images[0].save(final_pdf, save_all=True, append_images=images[1:])
print(f"Modified PDF saved as {final_pdf}")


