import glob
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

TOP_K = 5

print("Loading dataset...")
dataset = pd.read_parquet("../dataset/dataset.parquet")
print(f"{len(dataset)} recipes loaded")

# carico modello SBERT (Sentence BERT)
print("Loading Sentence-BERT...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("SBERT loaded")

# query dell'utente
print("Inserisci gli ingredienti della ricetta:")
ingredients = input()

# calcolo gli embeddings che confronterò con quelli del dataset
embeddings = model.encode(
    ingredients,
    convert_to_numpy=True,
    normalize_embeddings=True
)
embeddings = embeddings.astype(np.float32).reshape(1, -1)

# per trovare le migliori corrispondenze devo confrontare gli embeddings della query con
# quelli del dataset (sono sparsi nei vari shard_*.index)
#
# aver diviso gli embeddings del dataset in più file porta problemi:
# se cerco solo in questi file però otterrò degli indici (che rappresentano il numero di ricetta) locali,
# vale a dire che quell'indice è relativo ad un file shard_x.index e non ad un indice che posso usare nel dataset globale
#
# ho bisogno quindi anche dei file shard_*.npy dove ho salvato gli indici del dataset che avevo preso in esame

results = []
shards = sorted(glob.glob("idx/shard_*.index"))

for shard in shards:

    # carico indice FAISS
    index = faiss.read_index(shard)

    # carico id globali dello shard
    x = shard.split("_")[-1].split(".")[0]
    global_indexes = np.load(f"idx/shard_{x}.npy")

    # trovo le migliori TOP_K corrispondenze locali
    scores, local_indexes = index.search(embeddings, TOP_K)
    for score, local_index in zip(scores[0], local_indexes[0]):

        if local_index == -1:
            continue

        global_index = global_indexes[local_index]
        recipe = dataset.iloc[global_index]

        results.append({
            "score": float(score),
            "title": recipe["title"],
            "ingredients": recipe["ingredients"],
            "NER": recipe["NER"],
            "directions": recipe["directions"]
        })

# ordino in base allo score così da prendere le migliori TOP_K globali
results.sort(
    key=lambda x: x["score"],
    reverse=True
)

# stampo le migliori TOP_K ricette
print(f"\nTop {TOP_K} recipes:\n")
for i, recipe in enumerate(results[:TOP_K]):

    print("-"*80)

    print(f"{i+1}) {recipe['title']}")
    print(f"Similarity: {recipe['score']:.3f}")

    print("\nIngredients:")
    print(recipe["ingredients"])

    print("\nNER:")
    print(recipe["NER"])

    print("\nDirections:")
    print(recipe["directions"])

    print()