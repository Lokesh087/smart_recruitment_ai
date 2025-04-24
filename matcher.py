from sentence_transformers import util

# Global cache for the model
_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def calculate_match_score(resume_text, job_description):
    model = get_model()
    embeddings = model.encode([resume_text, job_description])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity[0][0]) * 100, 2)  # Return as percentage

