import pdfplumber
import docx
import os

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
    # Load spaCy model only when this function is called
    import spacy
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
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
