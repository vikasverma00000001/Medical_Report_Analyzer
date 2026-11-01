
import pytesseract

from PIL import Image

from pdf2image import convert_from_path

# Windows Tesseract Path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler Path
POPPLER_PATH = r"C:\Users\DELL\Downloads\Release-26.07.0-0\poppler-26.07.0\Library\bin"


def extract_text_from_image(image_path):

    image = Image.open(image_path)

    return pytesseract.image_to_string(image)


def extract_text_from_scanned_pdf(pdf_path):

    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    full_text = ""

    for page in pages:

        text = pytesseract.image_to_string(page)

        full_text += text + "\n"

    return full_text