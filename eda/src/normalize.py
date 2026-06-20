import ast
import pandas as pd

dataset = pd.read_csv("../../dataset/full_dataset.csv")

# filtro le colonne prendendo solo quelle informative
dataset = dataset[["title", "ingredients", "directions", "NER"]]

dataset = dataset.drop_duplicates()
dataset = dataset.dropna()

# normalizzo il testo e converto da str a list
dataset["title"] = dataset["title"].str.strip().str.lower()
dataset["ingredients"] = dataset["ingredients"].str.strip().str.lower().apply(ast.literal_eval)
dataset["directions"] = dataset["directions"].str.strip().str.lower().apply(ast.literal_eval)
dataset["NER"] = dataset["NER"].str.strip().str.lower().apply(ast.literal_eval)

# aggiungo una colonna che contiene il numero di ingredienti
dataset["#ingredients"] = dataset["NER"].apply(len)

# aggiungo una colonna che contiene il numero di step
dataset["#steps"] = dataset["directions"].apply(len)

# aggiungo una colonna che contiene il numero di parole delle istruzioni
dataset["directions_len"] = dataset["directions"].astype(str).apply(lambda x: len(x.split()))

dataset.to_parquet("../../dataset/formatted.parquet")