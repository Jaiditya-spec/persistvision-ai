import pandas as pd
from pathlib import Path

# Get project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to Excel file
DATA_PATH = BASE_DIR / "data" / "Sample_Data.xlsx"

# Load data
df = pd.read_excel(DATA_PATH)

# Clean column names
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_")
)

# Convert text columns to uppercase
df["Product_Name"] = df["Product_Name"].astype(str).str.upper()
df["Line_of_business"] = df["Line_of_business"].astype(str).str.upper()

# Display dataset information (for testing)
print("Dataset Loaded Successfully")
print(df.head())