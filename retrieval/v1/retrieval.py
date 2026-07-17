import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
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
index = faiss.read_index(str(INDEX_DIR / "embeddings.index"))

def search_recipes(ingredients, top_k=5):

    results = []
    # sanificazione dell'input
    ingredients = " ".join(ingredient.strip().lower() for ingredient in sorted(ingredients.split(",")))

    # calcolo gli embeddings della query
    embeddings = model.encode(
        ingredients,
        convert_to_numpy=True, # serve perchè FAISS lavora con i numpy array
        normalize_embeddings=True # serve perchè così FAISS può usare il prodotto scalare per la cosine similarity
    )
    embeddings = embeddings.astype(np.float32).reshape(1, -1) # serve perchè FAISS lavora con float32

    # trovo le migliori top_k corrispondenze
    scores, indexes = index.search(embeddings, top_k)

    for score, i in zip(scores[0], indexes[0]):
        
        # salto vettori non presenti
        # (nel caso in cui si riesca a trovare meno di top_k corrispondenze)
        if i == -1:
            continue

        recipe = dataset.iloc[i]

        results.append({
            "id": int(i),
            "score": float(score),
            "title": recipe["title"],
            "ingredients": list(recipe["NER"]),
            "directions": list(recipe["directions"])
        })

    return results