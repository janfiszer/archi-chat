import pymupdf

from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

from config import keywords
from src.preprocess import clean_raw_text_from_pdf

def load_context_file(file_path):
    pathlib_filepath = Path(file_path)
    file_extension = pathlib_filepath.suffix

    if file_extension == '.txt':
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
    elif file_extension == '.pdf':
        documents = load_pdf_chapter_as_documents(file_path, f"data/{pathlib_filepath.stem}.txt")
    else:
        raise ValueError(f"Unsupported file extension {file_extension}")

    return documents


def load_pdf_chapter_as_documents(filepath, txt_file_output=None, clean_pdf_text=True):
    """
    Loads the whole text from the pdf, cleans it and (optionally) saves it as txt_file_output.
    :param filepath: file path to the pdf
    :param txt_file_output: file path to the output txt file
    :param clean_pdf_text: a flag to clean the text before saving it as txt_file_output
    :return: Documents instances (one for each chapter) based on config.keywords.CHAPTER_SEP
    """
    with pymupdf.open(filepath) as pdf:
        text = "".join([page.get_text() for page in pdf.pages()])

    if clean_pdf_text:
        text = clean_raw_text_from_pdf(text)

    if txt_file_output:
        with open(txt_file_output, "w", encoding='utf-8') as txt_file:
            txt_file.write(text)

    chapter_split = text.split(keywords.CHAPTER_SEP)
    chapter_docs = [Document(keywords.CHAPTER_SEP + chapter_text) for chapter_text in chapter_split]

    return chapter_docs
