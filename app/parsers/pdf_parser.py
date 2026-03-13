from app.parsers.text_extractor import extract_text_from_pdf
from app.parsers.image_extractor import extract_images_from_pdf


def parse_pdf(pdf_path: str):
    """
    Parse PDF and return extracted text and images.
    """

    text = extract_text_from_pdf(pdf_path)

    images = extract_images_from_pdf(pdf_path)

    return {
        "text": text,
        "images": images
    }