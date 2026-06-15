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

filtered = dataset[dataset["#steps"] < 50]
filtered["#steps"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 50)
plt.title("steps distribution")
plt.xlabel("number of steps")
plt.ylabel("frequency")
plt.savefig("../images/steps_distribution.png", dpi=300)