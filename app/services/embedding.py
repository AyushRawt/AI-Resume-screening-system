from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def calculate_embedding_similarity(
    candidate_text: str,
    job_description: str,
) -> float:
    if not candidate_text.strip() or not job_description.strip():
        return 0.0

    model = get_embedding_model()

    embeddings = model.encode(
        [candidate_text, job_description],
        normalize_embeddings=True,
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]],
    )[0][0]

    return round(float(similarity * 100), 2)