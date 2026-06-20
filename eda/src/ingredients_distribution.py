import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_parquet("../../dataset/formatted.parquet")

filtered = dataset[dataset["#ingredients"] < 50]
filtered["#ingredients"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 50)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("ingredients distribution")
plt.xlabel("number of ingredients")
plt.ylabel("frequency")
plt.savefig("../img/ingredients_distribution.png", dpi=300)