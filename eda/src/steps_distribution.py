import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_parquet("../../dataset/formatted.parquet")

filtered = dataset[dataset["#steps"] < 50]
filtered["#steps"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 50)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("steps distribution")
plt.xlabel("number of steps")
plt.ylabel("frequency")
plt.savefig("../img/steps_distribution.png", dpi=300)