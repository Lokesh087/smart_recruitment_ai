from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_match_score(resume_text, job_description):
    embeddings = model.encode([resume_text, job_description])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(similarity[0][0]) * 100, 2)  # Return as percentage
