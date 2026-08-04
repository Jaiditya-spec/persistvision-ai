import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

PERIOD_1_PATH = DATA_DIR / "Sample_Data_YTD_Oct_25.xlsx"   # baseline period
PERIOD_2_PATH = DATA_DIR / "Sample_Data_YTD_Jun_26.xlsx"   # current period


def _load_and_clean(path):
    frame = pd.read_excel(path)

    frame.columns = (
        frame.columns
             .str.strip()
             .str.replace(" ", "_")
             .str.replace("/", "_")
    )

    frame["Product_Name"] = frame["Product_Name"].astype(str).str.upper()
    frame["Line_of_business"] = frame["Line_of_business"].astype(str).str.upper()

    return frame


df_period1 = _load_and_clean(PERIOD_1_PATH)   # Oct 25
df_period2 = _load_and_clean(PERIOD_2_PATH)   # Jun 26

# Existing tools (overall/product/lob/duration) keep working unchanged,
# now pointed at the latest period
df = df_period2

print("Datasets loaded successfully")
print("Period 1 (Oct 25):", df_period1.shape)
print("Period 2 (Jun 26):", df_period2.shape)