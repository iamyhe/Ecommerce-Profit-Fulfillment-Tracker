# ============================================================
#  Data Cleaning Script -- Superstore Sales Dataset
# ============================================================
# Cleans 'train.csv' based on the Data Quality Report findings:
#   - 11 missing values in Postal Code
#   - Date columns stored as strings
#   - Row ID not needed for analysis
# Outputs: 'cleaned_superstore.csv'
# ============================================================

import pandas as pd

# -- 1. Load the dataset --------------------------------------
df = pd.read_csv("train.csv")
print(f"[OK] Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns.\n")

# -- 2. Convert date columns to datetime ----------------------
# The dates are in DD/MM/YYYY format based on the raw data
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d/%m/%Y")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%d/%m/%Y")
print("[OK] 'Order Date' and 'Ship Date' converted to datetime.")

# -- 3. Handle Postal Code ------------------------------------
# Fill the 11 missing values with 'Unknown', then convert the
# entire column to string so the trailing ".0" decimals are removed.
df["Postal Code"] = df["Postal Code"].fillna("Unknown")
df["Postal Code"] = df["Postal Code"].apply(
    lambda x: str(int(x)) if isinstance(x, float) else str(x)
)
print("[OK] 'Postal Code' missing values filled with 'Unknown' and converted to string.")

# -- 4. Feature Engineering: Shipping Time ---------------------
# Calculate the number of days between shipping and ordering
df["Shipping_Time_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
print("[OK] New column 'Shipping_Time_Days' created.")

# -- 5. Drop unnecessary columns -------------------------------
df.drop(columns=["Row ID"], inplace=True)
print("[OK] 'Row ID' column dropped.")

# -- 6. Save the cleaned dataset -------------------------------
output_file = "cleaned_superstore.csv"
df.to_csv(output_file, index=False)
print(f"\n[OK] Cleaned dataset saved to '{output_file}'.\n")

# -- 7. Verify the result -------------------------------------
print("=" * 55)
print("  Cleaned DataFrame Info")
print("=" * 55)
df.info()
