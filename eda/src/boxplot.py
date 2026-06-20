import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_parquet("../../dataset/formatted.parquet")

filtered = dataset[["#ingredients", "#steps", "directions_len"]]
filtered.plot.box(showfliers=False)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.yscale("log")
plt.savefig("../img/boxplot.png", dpi=300)