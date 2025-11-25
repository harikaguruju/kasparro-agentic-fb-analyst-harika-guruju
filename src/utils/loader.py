import os
import pandas as pd

def load_csv(path):
    """
    Load CSV from `path` and parse date column.
    Raises FileNotFoundError if file doesn't exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    # read CSV and ensure 'date' column parsed as datetime (if present)
    df = pd.read_csv(path, parse_dates=["date"], infer_datetime_format=True)
    return df
