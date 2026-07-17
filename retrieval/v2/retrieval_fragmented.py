import gc
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from embeddings_fragmented import N_SHARDS
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

def search_recipes(ingredients, top_k=5):
    
    # sanificazione dell'input
    ingredients = " ".join(ingredient.strip().lower() for ingredient in sorted(ingredients.split(",")))

    # calcolo gli embeddings della query
    embeddings = model.encode(
        ingredients,
        convert_to_numpy=True, # serve perchè FAISS lavora con i numpy array
        normalize_embeddings=True # serve perchè così FAISS può usare il prodotto scalare per la cosine similarity
    )
    embeddings = embeddings.astype(np.float32).reshape(1, -1) # serve perchè FAISS lavora con float32
    
    results = []
    
    for shard in range(N_SHARDS):
        
        # carico indice FAISS
        index = faiss.read_index(str(INDEX_DIR / f"shard_{shard}.index"))

        # carico id globali dello shard
        x = shard.split("_")[-1].split(".")[0]
        global_indexes = np.load(str(INDEX_DIR / f"shard_{x}.npy"))

        # trovo le migliori top_k corrispondenze locali
        scores, local_indexes = index.search(embeddings, top_k)
        
        for score, local_index in zip(scores[0], local_indexes[0]):

            # salto vettori non presenti
            # (nel caso in cui si riesca a trovare meno di top_k corrispondenze)
            if local_index == -1:
                continue

            # ogni shard_*.index indicizza i propri embeddings da 0 a 223 113
            # se troviamo una ricetta nello shard_1 per esempio:
            # - index.search restituisce l'indice (quello di shard_1.index) della ricetta trovata, che può andare da 0 a 223 113
            # - nello shard_1 però avevamo calcolato gli embeddings delle ricette con indice (quello del dataset) da 223 114 a 446 227
            #
            # -> serve una mappatura da indice locale a indice globale
            global_index = global_indexes[local_index]
            recipe = dataset.iloc[global_index]

            results.append({
                "id": int(global_index),
                "score": float(score),
                "title": recipe["title"],
                "ingredients": list(recipe["NER"]),
                "directions": list(recipe["directions"])
            })
        
        del index
        del global_indexes
        gc.collect()

    # ordino in base allo score così da prendere le migliori top_k globali
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # restituisco solo le prime top_k
    return results[:top_k]