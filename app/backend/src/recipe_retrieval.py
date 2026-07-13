import glob
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, INDEX_DIR

TOP_K = 5

dataset = pd.read_parquet(FORMATTED_DATASET) 

model = SentenceTransformer("all-MiniLM-L6-v2")

# pre-carichiamo i percorsi delle shard per velocizzare le richieste future
shards = sorted(glob.glob(str(INDEX_DIR / "shard_*.index")))

def cerca_ricette(ingredients_input):
    
    # calcolo gli embeddings della query passata come argomento
    embeddings = model.encode(
        ingredients_input,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    embeddings = embeddings.astype(np.float32).reshape(1, -1)
    
    results = []
    
    for shard in shards:
        
        # carico indice FAISS
        index = faiss.read_index(shard)

        # carico id globali dello shard
        x = shard.split("_")[-1].split(".")[0]
        global_indexes = np.load(INDEX_DIR / f"shard_{x}.npy")

        # trovo le migliori TOP_K corrispondenze locali
        scores, local_indexes = index.search(embeddings, TOP_K)
        
        for score, local_index in zip(scores[0], local_indexes[0]):

            if local_index == -1:
                continue

            global_index = global_indexes[local_index]
            recipe = dataset.iloc[global_index]

            results.append({
                "id": int(global_index),
                "score": float(score),
                "title": recipe["title"],
                "ingredients": recipe["NER"].tolist(),
                "directions": recipe["directions"].tolist()
            })

    # ordino in base allo score così da prendere le migliori TOP_K globali
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # restituisco solo le prime TOP_K
    return results[:TOP_K]