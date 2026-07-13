import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, IMG_DIR

dataset = pd.read_parquet(FORMATTED_DATASET)

filtered = dataset[dataset["#ingredients"] < 50]
filtered["#ingredients"].plot(kind="hist", bins=50, edgecolor="black")

plt.xlim(0, 50)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title("ingredients distribution")
plt.xlabel("number of ingredients")
plt.ylabel("frequency")
plt.savefig(IMG_DIR / "ingredients_distribution.png", dpi=300)