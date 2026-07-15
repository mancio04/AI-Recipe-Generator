from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET_DIR = PROJECT_ROOT / "dataset"
INDEX_DIR = PROJECT_ROOT / "idx"

FORMATTED_DATASET = DATASET_DIR / "dataset.parquet"
FULL_DATASET = DATASET_DIR / "full_dataset.csv"

IMG_EDA_DIR = PROJECT_ROOT / "eda" / "img"
IMG_EVALUATION_DIR = PROJECT_ROOT / "evaluation" / "img"