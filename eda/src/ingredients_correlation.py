import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

dataset = pd.read_parquet("../../dataset/formatted.parquet")

# seleziono i 20 ingredienti più frequenti
counter = Counter()
for ingredients in dataset["NER"]:
    counter.update(ingredients)

top_20 = [ingredient for ingredient, _ in counter.most_common(20)]

# costruisco una matrice binaria dove:
# - righe -> ricette
# - colonne -> top 20 ingredienti
# se un ingrediente compare nella ricetta -> matrice[r,c] = 1
binary = pd.DataFrame(0, index=dataset.index, columns=top_20)
for i, ingredients in enumerate(dataset["NER"]):
    for ingredient in ingredients:
        if ingredient in top_20:
            binary.loc[i, ingredient] = 1

corr = binary.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, cmap="coolwarm", mask=mask, fmt=".2f", annot_kws={"size": 5})

plt.xticks(fontsize=5, rotation=45)
plt.yticks(fontsize=6)
plt.title("top 20 ingredients correlation")
plt.savefig("../img/ingredients_correlation.png", dpi=300)