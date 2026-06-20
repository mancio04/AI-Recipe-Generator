import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_parquet("../../dataset/formatted.parquet")

filtered = dataset[(dataset["#ingredients"] < 40) & (dataset["#steps"] < 40)]
sample = filtered.sample(n=10000, random_state=42)
sample.plot.scatter(x="#ingredients", y="#steps", alpha=0.2)

plt.xlim(0, 40)
plt.ylim(0, 40)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("ingredients vs steps")
plt.xlabel("number of ingredients")
plt.ylabel("number of steps")
plt.savefig("../img/ingredients_vs_steps.png", dpi=300)