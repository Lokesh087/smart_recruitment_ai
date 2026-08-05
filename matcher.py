from sentence_transformers import SentenceTransformer, util

model = None


def get_match_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def calculate_match_score(resume_text, job_description):
    model = get_match_model()
    embeddings = model.encode([resume_text, job_description])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity[0][0]) * 100, 2)  # Return as percentage


