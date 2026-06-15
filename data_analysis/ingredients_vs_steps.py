import os
import ast
import pandas as pd
import matplotlib.pyplot as plt

if os.path.exists("../dataset/formatted.parquet"):
    dataset = pd.read_parquet("../dataset/formatted.parquet")
else:
    dataset = pd.read_csv("../dataset/full_dataset.csv")
    # filtro le colonne prendendo solo quelle informative
    dataset = dataset[["title", "ingredients", "directions", "NER"]]

    # aggiungo una colonna che contiene il numero di ingredienti
    dataset["#ingredients"] = dataset["NER"].apply(ast.literal_eval).apply(len)
    
    # aggiungo una colonna che contiene il numero di step
    dataset["#steps"] = dataset["directions"].apply(ast.literal_eval).apply(len)

    dataset.to_parquet("../dataset/formatted.parquet")

filtered = dataset[(dataset["#ingredients"] < 50) & (dataset["#steps"] < 50)]
filtered.plot.hexbin(x="#ingredients", y="#steps", gridsize=30, cmap="viridis")

plt.xlim(0, 50)
plt.ylim(0, 50)
plt.title("ingredients vs steps")
plt.xlabel("number of ingredients")
plt.ylabel("number of steps")
plt.savefig("../images/ingredients_vs_steps.png", dpi=300)