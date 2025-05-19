import pandas as pd
import numpy as np

def detect_anomalies(df, threshold=3):
    df = df.copy()
    mean = df["Units Sold"].mean()
    std = df["Units Sold"].std()
    df["z_score"] = (df["Units Sold"] - mean) / std
    df["anomaly"] = df["z_score"].abs() > threshold
    return df
