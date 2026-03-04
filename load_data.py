import pandas as pd
import sqlite3

# Load the CSV
df = pd.read_csv("Sample - Superstore.csv", encoding='windows-1252')

# Preview the data
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# Save to SQLite database
conn = sqlite3.connect("superstore.db")
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()

print("\n✅ Data successfully loaded into superstore.db!")