import pandas as pd
from pathlib import Path

# -------------------------------
# Display configuration (readable in terminals & notebooks)
# -------------------------------
pd.set_option("display.max_rows", 50)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)
pd.set_option("display.max_colwidth", 80)


# -------------------------------
# File loading
# -------------------------------
DATA_PATH = Path("../sample_text_category.csv")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"CSV file not found at: {DATA_PATH.resolve()}")

df = pd.read_csv(
    DATA_PATH,
    encoding="utf-8",
    na_values=["", "NA", "NULL"]
)

print(f"✅ Loaded {len(df):,} rows and {len(df.columns)} columns\n")

# -------------------------------
# Quick data overview
# -------------------------------
print("📌 Column Summary")
print(df.info())

print("\n📌 First 5 rows")
print(df.head())



# -------------------------------
# Basic data quality checks
# -------------------------------
print("\n📌 Missing Values (Top 10)")
missing = df.isna().sum().sort_values(ascending=False)
print(missing.head(10))

# -------------------------------
# Optional: Text/category specific insights
# -------------------------------
if "category" in df.columns:
    print("\n📌 Category Distribution")
    print(df["category"].value_counts())


