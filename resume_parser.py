import os
import re
import pdfplumber
import docx

try:
    import spacy
    from spacy.util import is_package
except Exception:  # pragma: no cover - optional dependency for lightweight deployments
    spacy = None
    is_package = None

nlp = None


class _SimpleDoc:
    def __init__(self, text):
        self.text = text
        self.ents = []

    def __iter__(self):
        return iter([])


def get_nlp():
    global nlp
    if nlp is not None:
        return nlp

    if spacy is None:
        nlp = _SimpleDoc
        return nlp

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        if is_package and is_package("en_core_web_sm"):
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


def extract_phone_numbers(text):
    patterns = [
        r"\+?\d[\d\s\-()]{7,}\d",
        r"\(\d{3}\)\s*\d{3}[\-\s]\d{4}",
    ]
    phones = set()
    for pattern in patterns:
        for match in re.findall(pattern, text):
            normalized = re.sub(r"[^+\d]", "", match)
            if 7 <= len(normalized) <= 16:
                phones.add(normalized)
    return list(phones)


def extract_education(text):
    degrees = [
        "bachelor", "master", "mba", "phd", "b.sc", "m.sc", "b.eng", "m.eng", "associate",
        "certificate", "diploma",
    ]
    education = set()
    for line in text.splitlines():
        normalized = line.lower()
        if any(degree in normalized for degree in degrees):
            education.add(line.strip())
    return list(education)


TECHNICAL_TERMS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "ruby", "php",
    "swift", "kotlin", "scala", "r", "sql", "bash", "react", "angular", "vue",
    "django", "flask", "fastapi", "spring", "node", "express", "tensorflow",
    "pytorch", "keras", "spark", "hadoop", "pandas", "numpy", "scikit-learn",
    "bootstrap", "jquery", "material-ui", "aws", "azure", "gcp", "docker",
    "kubernetes", "terraform", "ansible", "jenkins", "git", "linux", "ci/cd",
    "docker-compose", "helm", "machine learning", "deep learning", "nlp", "data science",
    "analytics", "data analysis", "excel", "nosql", "html", "css", "rest api",
    "graphql", "microservices", "agile", "scrum", "ui/ux", "user interface", "project",
    "developer", "engineer", "scientist", "manager", "lead", "architect",
}


def is_valid_person_name(name):
    name_text = name.strip()
    if not name_text:
        return False

    low = name_text.lower()
    if any(term in low for term in TECHNICAL_TERMS):
        return False
    if re.search(r"\d|[@#%$^&*()_=+\\/|\[\]{}<>]", name_text):
        return False

    tokens = [token for token in re.findall(r"\b[A-Za-z]+\b", name_text)]
    if not tokens:
        return False
    if len(tokens) == 1 and tokens[0].lower() in TECHNICAL_TERMS:
        return False
    if all(token[0].islower() for token in tokens):
        return False

    return True


SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "ruby",
        "php", "swift", "kotlin", "scala", "r", "sql", "bash",
    ],
    "Frameworks & Libraries": [
        "react", "angular", "vue", "django", "flask", "fastapi", "spring", "node",
        "express", "tensorflow", "pytorch", "keras", "spark", "hadoop", "pandas",
        "numpy", "scikit-learn", "bootstrap", "jquery", "material-ui",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
        "jenkins", "git", "linux", "ci/cd", "docker-compose", "helm",
    ],
    "Data & AI": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "data science", "analytics", "data analysis", "nlp",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving", "project management",
        "adaptability", "critical thinking", "time management", "collaboration",
    ],
    "Other": [
        "excel", "nosql", "html", "css", "rest api", "graphql", "microservices",
        "agile", "scrum", "problem-solving", "user interface", "ui/ux",
    ],
}


def _normalize_text_for_skill_matching(text):
    return re.sub(r"[\-_/]+", " ", text.lower())


def extract_skills_from_text(text):
    normalized = _normalize_text_for_skill_matching(text)
    skill_map = {}
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            normalized_skill = _normalize_text_for_skill_matching(skill)
            pattern = r"\b" + re.escape(normalized_skill) + r"\b"
            if re.search(pattern, normalized):
                skill_map.setdefault(category, []).append(skill)

    if skill_map:
        return {category: sorted(set(skills)) for category, skills in skill_map.items()}

    nlp_model = get_nlp()
    doc = nlp_model(normalized)
    fallback_skills = set()
    stop_terms = {"resume", "experience", "skills", "education", "work", "year", "years", "project"}
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} and token.is_alpha:
            term = token.text.lower()
            if len(term) > 2 and term not in stop_terms:
                fallback_skills.add(term)
                if len(fallback_skills) >= 25:
                    break

    return {"Inferred Skills": sorted(fallback_skills)}


def extract_summary(text, max_sentences=3):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if len(sentences) <= max_sentences:
        return sentences

    stop_words = {
        "and", "the", "for", "with", "that", "this", "from", "have", "has",
        "are", "but", "not", "you", "your", "their", "our", "project",
    }
    sentence_scores = []
    for sentence in sentences:
        words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{2,}\b", sentence)]
        score = sum(1 for word in words if word not in stop_words)
        sentence_scores.append((score, sentence))

    top_sentences = [sentence for _, sentence in sorted(sentence_scores, key=lambda x: -x[0])[:max_sentences]]
    top_sentences.sort(key=lambda s: sentences.index(s))
    return top_sentences


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
    doc = nlp_model(text) if callable(nlp_model) else nlp_model
    entities = {
        "email": None,
        "phone": [],
        "name": None,
        "location": [],
        "skills": {},
        "experience": [],
        "education": [],
        "summary": [],
    }

    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            entities["email"] = ent.text
        elif ent.label_ == "PERSON" and not entities["name"] and is_valid_person_name(ent.text):
            entities["name"] = ent.text
        elif ent.label_ in ["GPE", "LOC"]:
            entities["location"].append(ent.text)
        elif ent.label_ in ["ORG", "WORK_OF_ART", "PRODUCT", "NORP"]:
            entities["experience"].append(ent.text)

    entities["phone"] = extract_phone_numbers(text)
    entities["education"] = extract_education(text)
    entities["skills"] = extract_skills_from_text(text)
    entities["summary"] = extract_summary(text)
    entities["location"] = sorted(set(entities["location"]))
    entities["experience"] = sorted(set(entities["experience"]))
    return entities

