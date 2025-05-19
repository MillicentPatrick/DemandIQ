import pandas as pd

def clean_data(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna(subset=["Date", "Units Sold"])
    return df
