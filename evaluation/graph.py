import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import INDEX_DIR, IMG_EVALUATION_DIR

dataset = pd.read_csv(str(INDEX_DIR / "evaluation.csv"))

for top_k in sorted(dataset["top_k"].unique()):
    filtered = dataset[dataset["top_k"] == top_k]
    plt.plot(filtered["percentage"] * 100, filtered["recall"], marker="o", label=f"Recall@{top_k}")

plt.ylim(0, 0.8)
plt.xticks([30, 50, 70, 90])
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("retrieval evaluation")
plt.xlabel("percentage of ingredients")
plt.ylabel("recall")
plt.grid(True)
plt.legend()
plt.savefig(IMG_EVALUATION_DIR / "evaluation.png", dpi=300)