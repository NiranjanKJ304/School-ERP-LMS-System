import pandas as pd
import os
from pathlib import Path

def init_directories():
    directories = [
        'data/students',
        'data/teachers',
        'data/marks',
        'data/assignments',
        'data/submissions',
        'data/materials',
        'data/users'
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def save_dataframe(df, filepath, excel=True):
    df.to_csv(filepath + '.csv', index=False)
    if excel:
        df.to_excel(filepath + '.xlsx', index=False)

def load_dataframe(filepath):
    csv_path = filepath + '.csv'
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()