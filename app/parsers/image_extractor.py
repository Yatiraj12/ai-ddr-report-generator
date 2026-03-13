import fitz
import os


OUTPUT_FOLDER = "data/extracted_images"


def extract_images_from_pdf(pdf_path: str):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    doc = fitz.open(pdf_path)

    extracted_images = []

    for page_index in range(len(doc)):

        page = doc.load_page(page_index)

        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):

            xref = img[0]
            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_name = f"page{page_index+1}_img{img_index+1}.{image_ext}"

            image_path = os.path.join(OUTPUT_FOLDER, image_name)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            extracted_images.append(image_path)

    doc.close()

    return extracted_images