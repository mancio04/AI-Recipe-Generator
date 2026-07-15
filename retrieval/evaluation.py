import random
import pandas as pd
from retrieval import search_recipes
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET

N_TEST = 100
PERCENTAGE = 0.6
TOP_K = 5

random.seed(42)
dataset = pd.read_parquet(FORMATTED_DATASET)

# campione casuale
test_set = dataset.sample(n=N_TEST, random_state=42)

correct = 0
tested = 0

for _, recipe in test_set.iterrows():

    ingredients = list(recipe["NER"])

    # salto ricette senza ingredienti
    if len(ingredients) == 0:
        continue

    # prendo il PERCENTAGE% degli ingredienti
    query = random.sample(ingredients, max(1, int(len(ingredients) * PERCENTAGE)))
    query = " ".join(query)

    results = search_recipes(query, TOP_K)

    # controllo se la ricetta originale compare
    found = False
    for result in results:
        if set(result["ingredients"]) == set(ingredients):
            found = True
            break

    tested += 1
    if found:
        correct += 1

recall = (correct / tested) * 100

print(f"Recall@{TOP_K}: {recall:.3f}%")
print(f"Recipes found: {correct}/{N_TEST}")