import pandas as pd

df = pd.read_csv('data/tiktok_dataset.csv')

def clean_dataset():
    return df
def df_duration():
    return df[df['video_duration_sec'].notna() & df['claim_status'].isin(['claim', 'opinion'])]
def clean_dropdown_options(series):
    return [{'label': str(s), 'value': s} for s in series.unique() if pd.notna(s)]