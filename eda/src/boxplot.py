import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))
from config import FORMATTED_DATASET, IMG_EDA_DIR

dataset = pd.read_parquet(FORMATTED_DATASET)

filtered = dataset[["#ingredients", "#steps", "directions_len"]]
filtered.plot.box(showfliers=False)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.yscale("log")
plt.savefig(IMG_EDA_DIR / "boxplot.png", dpi=300)