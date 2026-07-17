import gc
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

N_SHARDS = 10

# carico dataset
print("Loading dataset...")
dataset = pd.read_parquet(FORMATTED_DATASET)
print(f"{len(dataset)} recipes loaded")

# carico modello SBERT (Sentence BERT)
print("\nLoading Sentence-BERT...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SBERT loaded")

# elaboro il dataset a blocchi di 1/10 della dimensione totale (223 114 ricette alla volta)
shard_size = (len(dataset) + N_SHARDS - 1) // N_SHARDS

for shard in range(N_SHARDS):

    start = shard * shard_size
    end = min(start + shard_size, len(dataset))
    print(f"\nShard: {shard+1}/{N_SHARDS}")
    print(f"Recipes: {start} - {end-1}")

    dataset_shard = dataset.iloc[start:end]

    # salvo gli indici che sto prendendo in esame
    global_indexes = dataset_shard.index.to_numpy()
    np.save(str(INDEX_DIR / f"shard_{shard}.npy"), global_indexes)

    # converto in lista di stringhe perchè SBERT lavora con le stringhe
    texts = [" ".join(sorted(ingredients)) for ingredients in dataset_shard["NER"]]

    # creazione degli embeddings (matrice 223 114 x 384)
    print("\nCreating embeddings...")
    embeddings = model.encode(
        texts,
        batch_size=128, # elaboro 128 ricette alla volta per limitare la memoria
        show_progress_bar=True,
        convert_to_numpy=True, # serve perchè FAISS lavora con i numpy array
        normalize_embeddings=True # serve perchè così FAISS può usare il prodotto scalare per la cosine similarity
    )
    embeddings = embeddings.astype(np.float32) # serve perchè FAISS lavora con float32
    print("Embeddings created")

    # creazione indice FAISS (indice vettoriale)
    print("\nSaving FAISS index...")
    index = faiss.IndexFlatIP(model.get_embedding_dimension())
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_DIR / f"shard_{shard}.index"))
    print("FAISS index saved")

    del texts
    del embeddings
    del dataset_shard
    gc.collect()