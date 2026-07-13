import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, IMG_DIR

dataset = pd.read_parquet(FORMATTED_DATASET)

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
plt.savefig(IMG_DIR / "ingredients_vs_steps.png", dpi=300)