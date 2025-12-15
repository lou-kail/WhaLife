import pandas as pd
import os

os.makedirs("data/csv", exist_ok=True)

df = pd.read_csv('data/txt/occurrence.txt', sep='\t')

df.to_csv('data/csv/occurrence.csv', index=False, encoding='utf-8')