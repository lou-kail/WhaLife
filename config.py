import pandas as pd
import os

TAXON_IDS = {
    "HUMPBACK_WHALE": 137092,
    "BLUE_WHALE": 137090,
    "ORCA": 137102,
    "DOLPHIN": 137094,
}

os.makedirs("data/csv", exist_ok=True)

df = pd.read_csv('data/txt/occurrence.txt', sep='\t')

df.to_csv('data/csv/occurrence.csv', index=False, encoding='utf-8')