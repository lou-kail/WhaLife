import pandas as pd
import os

TAXON_CONFIG = {
    "HUMPBACK_WHALE": 137092,
    "BLUE_WHALE": 137090,
    "ORCA": 137102,
    "DOLPHIN": 137094,
    "NARWHAL": 383467
}

# TODO: Update config creation

os.makedirs("data/csv", exist_ok=True)

df = pd.read_csv('data/txt/occurrence.txt', sep='\t')

df.to_csv('data/csv/occurrence.csv', index=False, encoding='utf-8')