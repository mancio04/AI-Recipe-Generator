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

# converto in lista di stringhe perchè SBERT lavora con le stringhe
texts = [" ".join(ingredients) for ingredients in dataset["NER"]]

# creazione degli embeddings (matrice 2 231 142 x 384)
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
faiss.write_index(index, str(INDEX_DIR / "embeddings.index"))
print("FAISS index saved")