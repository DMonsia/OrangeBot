import io
import re

import config
import fitz
import pandas as pd
import pytesseract
from PIL import Image


def is_page_textual(page, text_threshold=0.0):
    """Verifie si une page contient du texte
    Args:
        page (Any): la page à verifier
        text_threshold (float): la proportion de texte par minimal acceptable.Default 0.3
    Return:
        Un boolean.
    """
    text = page.get_text()
    # Calculez la proportion de texte par rapport
    # à la longueur totale du contenu
    text_length = len(text)
    total_length = page.rect.width * page.rect.height
    text_ratio = text_length / total_length
    return text_ratio >= text_threshold


def clean_text(text: str) -> str:
    text = re.sub("\n +", "\n", text)
    text = re.sub("\n+", "\n", text)
    text = re.sub(" +", " ", text)
    return text.strip()


def ocr_pdf(file_content: bytes):
    documents = []
    pdf_stream = io.BytesIO(file_content)
    pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")  # type: ignore
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        if is_page_textual(
            page
        ):  # Extraction de texte directe si la page contient principalement du texte
            documents.append(clean_text(page.get_text()))
        else:  # Sinon, utilisez Tesseract OCR pour extraire le texte des images
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_data = base_image["image"]
                image = Image.open(io.BytesIO(image_data))
                documents.append(clean_text(pytesseract.image_to_string(image)))
    return documents


def process_pdf_file(file, text_splitter):
    documents: list = []
    metadata: list = []
    docs = ocr_pdf(file.content)
    for num_page, page in enumerate(docs):
        # Découpage du texte en morceaux
        chunks = text_splitter.split_text(page)
        for chunk_idx, chunk in enumerate(chunks):
            documents.append(chunk)
            metadata.append(
                {
                    "doc": file.name.split("/")[-1],
                    "page": str(num_page),
                    "chunk": str(chunk_idx),
                    "source": f"f-{file.name.split('/')[-1]} p-{num_page} c-{chunk_idx}",
                }
            )
    return documents, metadata


def process_csv_file(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file.content, sep=config.CSV_SEP)
    else:
        df = pd.read_excel(file.content)
    df[config.CONTEXT_COLUMN] = df[config.CONTEXT_COLUMN].map(lambda x: clean_text(x))
    df.rename({config.DATA_SOURCE: "source"}, inplace=True, axis=1)
    df = df[config.METADATA_COLUMNS]
    return list(df[config.INDEXED_COLUMNS]), df.to_dict("records")


# Définition d'une fonction asynchrone pour traiter les fichiers téléchargés
def process_uploaded_files(files, text_splitter):
    """Charge des fichiers puis fait un pretraitement"""
    documents: list = []
    metadata: list = []
    for file in files:
        if file.name.endswith(".pdf"):
            docs, meta = process_pdf_file(file, text_splitter)
            documents.extend(docs)
            metadata.extend(meta)
        else:
            docs, meta = process_csv_file(file)
            documents.extend(docs)
            metadata.extend(meta)
    return documents, metadata
