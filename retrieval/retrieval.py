import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, INDEX_DIR

# carico dataset
print("Loading dataset...")
dataset = pd.read_parquet(FORMATTED_DATASET)
print(f"{len(dataset)} recipes loaded")

# carico modello SBERT (Sentence BERT)
print("\nLoading Sentence-BERT...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SBERT loaded")

# carico indice FAISS
index = faiss.read_index(INDEX_DIR / "embeddings.index")

def search_recipes(ingredients, top_k=5):

    results = []

    embeddings = model.encode(
        ingredients,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # trovo le migliori top_k corrispondenze
    scores, indexes = index.search(embeddings, top_k)

    for score, i in zip(scores[0], indexes[0]):
        
        # salto vettori non presenti
        # (nel caso in cui si riesca a trovare meno di top_k corrispondenze)
        if i == -1:
            continue

        recipe = dataset.iloc[i]

        results.append({
            "score": float(score),
            "title": recipe["title"],
            "ingredients": list(recipe["NER"]),
            "directions": list(recipe["directions"])
        })

    return results