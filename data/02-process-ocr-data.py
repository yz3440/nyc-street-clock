import polars as pl
import os
from dataclasses import dataclass


@dataclass
class OcrData:
    id: int
    panorama_id: str
    text: str
    ocr_yaw: float
    ocr_pitch: float
    ocr_width: float
    ocr_height: float
    lat: float
    lng: float
    heading: float
    pitch: float
    roll: float


# Read the CSV file using polars
df = pl.read_csv("ocr_data.csv")

# find all unique text
unique_texts = df["text"].unique()

print(len(unique_texts))

SEPARATE_FILES_DIR = "../digits"
os.makedirs(
    SEPARATE_FILES_DIR, exist_ok=True
)  # create the directory if it doesn't exist

# group things by unique text and export a json
for text in unique_texts:
    if len(text) > 4:
        continue

    # text needs to be 0000 to 2500
    if int(text) > 2500:
        continue

    # if there is non numeric characters, skip
    if not text.isdigit():
        continue

    df_text = df.filter(pl.col("text") == text)
    # make all the float64 column to 2 decimal places
    float_cols = [
        col
        for col, dtype in zip(df_text.columns, df_text.dtypes)
        if dtype == pl.Float64
    ]
    df_text = df_text.with_columns(
        [pl.col(col).cast(pl.Float32).round(2) for col in float_cols]
    )
    # write a csv
    df_text.write_csv(f"{SEPARATE_FILES_DIR}/{text}.csv")
