import re
from collections import Counter

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:  # pragma: no cover - optional dependency for lightweight deployments
    SentenceTransformer = None
    util = None

model = None


def get_match_model():
    global model
    if model is None and SentenceTransformer is not None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def _keyword_fallback_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0

    resume_tokens = Counter(re.findall(r"[a-z0-9]+", resume_text.lower()))
    job_tokens = Counter(re.findall(r"[a-z0-9]+", job_description.lower()))

    if not resume_tokens or not job_tokens:
        return 0.0

    overlap = sum(min(resume_tokens[token], job_tokens[token]) for token in set(resume_tokens) & set(job_tokens) if len(token) > 2)
    total = sum(job_tokens.values())
    if total == 0:
        return 0.0

    return round((overlap / total) * 100, 2)


def calculate_match_score(resume_text, job_description):
    if not resume_text or not job_description:
        return 0.0

    try:
        model_instance = get_match_model()
        embeddings = model_instance.encode([resume_text, job_description])
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        return round(float(similarity[0][0]) * 100, 2)
    except Exception:
        return _keyword_fallback_score(resume_text, job_description)


