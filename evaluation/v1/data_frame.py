import random
import pandas as pd
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, INDEX_DIR
from retrieval.v1.retrieval import search_recipes

N_TEST = 100
TOP_KS = [1, 3, 5, 10]
PERCENTAGES = [0.3, 0.5, 0.7, 0.9]

random.seed(42)

# carico dataset
print("Loading dataset...")
dataset = pd.read_parquet(FORMATTED_DATASET)
print(f"{len(dataset)} recipes loaded")

# campione casuale
test_set = dataset.sample(n=N_TEST, random_state=42)

rows = []

for percentage in PERCENTAGES:

    print(f"\nPercentage: {int(percentage*100)}%")
    for top_k in TOP_KS:

        correct = 0
        tested = 0

        for index, recipe in test_set.iterrows():

            ingredients = list(recipe["NER"])

            # salto ricette senza ingredienti
            if len(ingredients) == 0:
                continue

            # prendo il percentage% degli ingredienti
            query = random.sample(ingredients, max(1, int(len(ingredients) * percentage)))
            query = " ".join(query)

            results = search_recipes(query, top_k)

            # controllo se la ricetta originale compare
            for result in results:
                if result["id"] == index:
                    correct += 1

            tested += 1

        recall = (correct / tested) * 100

        print(f"Recall@{top_k}: {int(recall)}")
        print(f"Recipes found: {correct}/{tested}")
        rows.append({
            "percentage": percentage,
            "top_k": top_k,
            "recall": recall
        })

data_frame = pd.DataFrame(rows)
data_frame.to_csv(str(INDEX_DIR / "evaluation.csv"), index=False)