import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, IMG_EDA_DIR

dataset = pd.read_parquet(FORMATTED_DATASET)

filtered = dataset[dataset["#steps"] < 50]
filtered["#steps"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 50)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("steps distribution")
plt.xlabel("number of steps")
plt.ylabel("frequency")
plt.savefig(IMG_EDA_DIR / "steps_distribution.png", dpi=300)