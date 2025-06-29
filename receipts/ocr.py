import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from dateutil import parser

# OPTIONAL: Set tesseract path manually if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from pdf2image import convert_from_path

POPPLER_PATH = r"C:\Users\USER\Documents\poppler\poppler-24.08.0\Library\bin"  # Replace this

def load_images_from_file(path):
    if path.lower().endswith('.pdf'):
        pages = convert_from_path(path, poppler_path=POPPLER_PATH)
        return pages  # list of PIL Images
    else:
        return [clean_image(path)]  # single image in a list

def clean_image(image_path):
    """
    Preprocess the image for better OCR accuracy:
    - Convert to grayscale
    - Sharpen
    - Binarize (threshold)
    """
    image = Image.open(image_path)
    image = image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)
    image = image.point(lambda x: 0 if x < 140 else 255)  # Simple binarization
    return image


def extract_total_from_lines(lines):
    """
    Search for lines that mention total, amount, or balance,
    and extract the number next to those keywords.
    """
    for line in lines:
        if re.search(r'\b(total|amount|balance|paid)\b', line, re.IGNORECASE):
            prices = re.findall(r"\d+\.\d{2}", line)
            if prices:
                return float(prices[-1])  # Take last number in line
    return None


def extract_all_prices(text):
    """Fallback: extract all prices from the entire text."""
    return [float(p) for p in re.findall(r"\d+\.\d{2}", text)]


def extract_receipt_data(image_path, return_text=False):
    images = load_images_from_file(image_path)
    all_text = []

    for img in images:
        all_text.append(pytesseract.image_to_string(img))

    text = "\n".join(all_text)
    lines = text.split('\n')

    vendor = lines[0].strip() if lines and lines[0].strip() else "Unknown"
    total = extract_total_from_lines(lines)
    if total is None:
        prices = extract_all_prices(text)
        total = max(prices) if prices else None

    try:
        date = parser.parse(text, fuzzy=True).date()
    except:
        date = None

    data = {
        "vendor": vendor,
        "total": total,
        "date": date,
    }

    return (data, text) if return_text else data


