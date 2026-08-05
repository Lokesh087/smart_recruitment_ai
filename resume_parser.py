import os
import pdfplumber
import docx
import spacy
from spacy.util import is_package

nlp = None


def get_nlp():
    global nlp
    if nlp is not None:
        return nlp

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        if is_package("en_core_web_sm"):
            print(
                "Warning: spaCy model 'en_core_web_sm' failed to load; using blank 'en' model."
            )
            nlp = spacy.blank("en")
        else:
            try:
                from spacy.cli import download

                download("en_core_web_sm")
                nlp = spacy.load("en_core_web_sm")
            except Exception:
                nlp = spacy.blank("en")
                print(
                    "Warning: spaCy model 'en_core_web_sm' not available; using blank 'en' model."
                )
    return nlp


def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_resume_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".doc", ".docx"]:
        return extract_text_from_docx(file_path)
    return ""


def parse_resume(text):
    nlp_model = get_nlp()
    doc = nlp_model(text)
    entities = {
        "email": None,
        "name": None,
        "skills": [],
        "experience": [],
    }

    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            entities["email"] = ent.text
        elif ent.label_ == "PERSON" and not entities["name"]:
            entities["name"] = ent.text
        elif ent.label_ in ["ORG", "WORK_OF_ART"]:
            entities["experience"].append(ent.text)

    tokens = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    entities["skills"] = list(set(tokens))
    return entities

