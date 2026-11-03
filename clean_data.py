"""
Clean the "Apartments in Almaty" dataset.

Reads almaty_apartments_with_id.csv, removes duplicates and impossible values,
adds price per m2 and a construction-period column, and saves
almaty_apartments_clean.csv.

Source: Kaggle, "Apartments in Almaty" by Altemir Omar (MIT licence).
"""

import pandas as pd

RAW_FILE = "almaty_apartments_with_id.csv"
CLEAN_FILE = "almaty_apartments_clean.csv"

# Plausible ranges (prices are assumed to be in tenge, the source does not say)
MIN_AREA, MAX_AREA = 12, 300                      # m2: drops tiny rooms and houses
MAX_FLOOR = 40                                    # no building in Almaty is taller
MIN_PRICE_M2, MAX_PRICE_M2 = 150_000, 2_500_000   # price per m2

df = pd.read_csv(RAW_FILE)
log = [("Rows in the raw file", len(df))]

# 1. Duplicates: identical listings (all columns except Id)
df = df.drop_duplicates(subset=df.columns.drop("Id"))
log.append(("After removing duplicates", len(df)))

# 2. Price per m2
df["price_per_m2"] = (df["price"] / df["area"]).round(0)

# 3. Obvious errors and outliers
df = df[df["area"].between(MIN_AREA, MAX_AREA)]
log.append((f"Area between {MIN_AREA} and {MAX_AREA} m2", len(df)))

df = df[df["floor"] <= MAX_FLOOR]
log.append((f"Floor not above {MAX_FLOOR}", len(df)))

df = df[df["price_per_m2"].between(MIN_PRICE_M2, MAX_PRICE_M2)]
log.append((f"Price per m2 between {MIN_PRICE_M2:,} and {MAX_PRICE_M2:,}", len(df)))

# 4. Data types and new columns
for col in ["number_of_rooms", "floor", "year_of_construction"]:
    df[col] = df[col].astype(int)

df["build_period"] = pd.cut(
    df["year_of_construction"],
    bins=[1900, 1969, 1989, 2004, 2014, 2030],
    labels=["Before 1970", "1970-1989", "1990-2004", "2005-2014", "2015 or later"],
)

df.to_csv(CLEAN_FILE, index=False)

print("Cleaning steps:")
prev = None
for name, n in log:
    removed = "" if prev is None else f"  (removed {prev - n})"
    print(f"  {name}: {n}{removed}")
    prev = n
print(f"\nKept {len(df)} of {log[0][1]} rows ({len(df) / log[0][1]:.1%}). File: {CLEAN_FILE}")
