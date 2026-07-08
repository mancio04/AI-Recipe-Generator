import glob
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

TOP_K = 5

dataset = pd.read_parquet("dataset/dataset.parquet") 

model = SentenceTransformer("all-MiniLM-L6-v2")

# Pre-carichiamo i percorsi delle shard per velocizzare le richieste future
shards = sorted(glob.glob("src/idx/shard_*.index"))

def cerca_ricette(ingredients_input):

    # Calcolo gli embeddings della query passata come argomento
    embeddings = model.encode(
        ingredients_input,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    embeddings = embeddings.astype(np.float32).reshape(1, -1)

    results = []
    
    for shard in shards:
        
        # Carico indice FAISS
        index = faiss.read_index(shard)

        # Carico id globali dello shard
        x = shard.split("_")[-1].split(".")[0]
        global_indexes = np.load(f"src/idx/shard_{x}.npy")

        # Trovo le migliori TOP_K corrispondenze locali
        scores, local_indexes = index.search(embeddings, TOP_K)

        for score, local_index in zip(scores[0], local_indexes[0]):

            if local_index == -1:
                continue

            global_index = global_indexes[local_index]
            recipe = dataset.iloc[global_index]

            # conversione da numpy.array a lista per json
            ingredienti_list = recipe["NER"].tolist()

            results.append({
                "score": float(score),
                "title": recipe["title"],
                "ingredients": ingredienti_list,
                "directions": recipe["directions"]
            })

    # Ordino in base allo score così da prendere le migliori TOP_K globali
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Restituisco solo le prime TOP_K
    return results[:TOP_K]