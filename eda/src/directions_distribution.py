import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_parquet("../../dataset/formatted.parquet")

filtered = dataset[dataset["directions_len"] < 500]
filtered["directions_len"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 500)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("directions distribution")
plt.xlabel("number of words")
plt.ylabel("frequency")
plt.savefig("../img/directions_distribution.png", dpi=300)