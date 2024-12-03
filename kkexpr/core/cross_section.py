import pandas as pd
import numpy as np

def cs_rank(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate cross-sectional rank."""
    return df.rank(axis=1, pct=True)

def cs_zscore(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate cross-sectional z-score."""
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    return df.sub(mean, axis=0).div(std, axis=0)

def cs_demean(df: pd.DataFrame) -> pd.DataFrame:
    """Demean cross-section."""
    return df.sub(df.mean(axis=1), axis=0) 