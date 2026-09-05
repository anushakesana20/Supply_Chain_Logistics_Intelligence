import pandas as pd
import sqlite3

# Load cleaned dataset
df = pd.read_csv(
    "data/processed/DataCoSupplyChain_Cleaned.csv",
    encoding="utf-8"
)

# Create SQLite database
connection = sqlite3.connect("supply_chain.db")

# Load CSV into SQL table
df.to_sql(
    "supply_chain",
    connection,
    if_exists="replace",
    index=False
)

print("Data loaded successfully into SQL database!")

# Check number of rows
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM supply_chain")

count = cursor.fetchone()[0]

print("Rows in SQL table:", count)

connection.close()