import gc
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

N_SHARDS = 10

print("Loading dataset...")
dataset = pd.read_parquet("../../dataset/formatted.parquet")
print(f"{len(dataset)} recipes loaded")

# carico modello SBERT (Sentence BERT)
print("\nLoading Sentence-BERT...")
model = SentenceTransformer("all-MiniLM-L6-v2")
dimension = model.get_embedding_dimension()
print(f"Embedding dimension: {dimension}")

# elaboro il dataset a blocchi di 1/10 della dimensione totale
shard_size = (len(dataset) + N_SHARDS - 1) // N_SHARDS

for shard in range(N_SHARDS):

    start = shard * shard_size
    end = min(start + shard_size, len(dataset))

    dataset_shard = dataset.iloc[start:end]

    # salvo gli indici che sto prendendo in esame
    indexes = dataset_shard.index.to_numpy()
    np.save(f"../idx/shard_{shard}.npy", indexes)

    # converto in lista di stringhe perchè SBERT lavora con le stringhe
    texts = [" ".join(ingredients) for ingredients in dataset_shard["NER"]]

    print(f"\nShard: {shard+1}/{N_SHARDS}")
    print(f"Recipes: {start} - {end-1}")

    # creo gli embeddings:
    # - ogni embedding è un vettore di 384 numeri
    # - embeddings è una matrice 223114 x 384
    embeddings = model.encode(
        texts,
        batch_size=128, # elaboro 128 ricette alla volta (sempre per limitare la memoria)
        show_progress_bar=True,
        convert_to_numpy=True, # serve perchè FAISS lavora con i numpy array
        normalize_embeddings=True # serve perchè così FAISS può usare il prodotto scalare per la cosine similarity
    )
    embeddings = embeddings.astype(np.float32) # serve perchè FAISS lavora con float32

    # creazione indice FAISS (indice vettoriale)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, f"../idx/shard_{shard}.index")

    del texts
    del embeddings
    del index
    del dataset_shard
    gc.collect()