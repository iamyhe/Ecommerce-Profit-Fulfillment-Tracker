# ============================================================
#  Data Quality Report -- Superstore Sales Dataset
# ============================================================
# This script loads 'train.csv' and produces a concise
# quality overview: shape, data types, missing values,
# duplicate rows, and a structural preview.
# ============================================================

import pandas as pd

# -- 1. Load the dataset --------------------------------------
df = pd.read_csv("train.csv")
print("[OK] Dataset loaded successfully.\n")

# -- 2. Shape of the dataset ----------------------------------
rows, cols = df.shape
print("=" * 50)
print("  Dataset Shape")
print("=" * 50)
print(f"  Rows    : {rows:,}")
print(f"  Columns : {cols}")
print()

# -- 3. Data types of each column ------------------------------
print("=" * 50)
print("  Column Data Types")
print("=" * 50)
print(df.dtypes.to_string())
print()

# -- 4. Missing values per column ------------------------------
missing = df.isnull().sum()
total_missing = missing.sum()

print("=" * 50)
print("  Missing Values Per Column")
print("=" * 50)
print(missing.to_string())
print(f"\n  >> Total missing values across all columns: {total_missing}")
print()

# -- 5. Duplicate rows ----------------------------------------
dup_count = df.duplicated().sum()

print("=" * 50)
print("  Duplicate Rows")
print("=" * 50)
print(f"  Number of duplicate rows: {dup_count}")
print()

# -- 6. First 5 rows (structural preview) ---------------------
print("=" * 50)
print("  First 5 Rows")
print("=" * 50)
print(df.head().to_string())
