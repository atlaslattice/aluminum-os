
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

def overlay_text_on_pdf(input_pdf_path, output_pdf_path, text_to_overlay):
    # Convert the first page of the PDF to an image
    images = convert_from_path(input_pdf_path, first_page=1, last_page=1)
    image = images[0]

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Use a default font
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", size=12)
    except IOError:
        font = ImageFont.load_default()

    # Overlay the text
    for item in text_to_overlay:
        draw.text(item["coords"], item["text"], fill="black", font=font)

    # Save the modified image as a new PDF
    image.save(output_pdf_path, "PDF", resolution=100.0)

# Define the text and coordinates for Form 26
form26_text = [
    {"text": "Denver County", "coords": (150, 90)},
    {"text": "1437 Bannock St., Room 256, Denver, CO 80202", "coords": (100, 120)},
    {"text": "Sheldon", "coords": (100, 170)},
    {"text": "John O'Connor & Alex Knuckey", "coords": (100, 220)},
    {"text": "25S00165", "coords": (450, 170)},
    {"text": "8081.48", "coords": (500, 325)},
    {"text": "371.97", "coords": (500, 350)},
    {"text": "8453.45", "coords": (500, 400)},
    {"text": "Clerk of the Court", "coords": (200, 650)}
]

# Overlay text on Form 26
overlay_text_on_pdf(
    '/home/ubuntu/nova_shred/forms/Form26_Writ_Continuing_Garnishment.pdf',
    '/home/ubuntu/nova_shred/filled_forms/Form26_filled.pdf',
    form26_text
)

print("Form 26 filled successfully!")
