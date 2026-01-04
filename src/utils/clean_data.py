import pandas as pd

def clean_data(df):
    cols_to_keep = [
        'scientificName', 'vernacularName',
        'decimalLatitude', 'decimalLongitude',
        'eventDate', 'year', 'month',
        'basisOfRecord', 'datasetName',
        'sst', 'sss', 'bathymetry', 'shoredistance',
        'id'
    ]

    df_clean = df[[col for col in cols_to_keep if col in df.columns]].copy()

    def categorize_species(name):
        name = str(name).lower()
        if 'megaptera' in name: return 'Humpback Whale'
        if 'orcinus' in name: return 'Orca'
        if 'delphinus' in name: return 'Dolphin'
        if 'balaenoptera' in name: return 'Blue Whale'
        return 'Other'

    df_clean['category'] = df_clean['scientificName'].apply(categorize_species)

    df_clean['eventDate'] = pd.to_datetime(df_clean['eventDate'], errors='coerce')

    rename_map = {
        'decimalLatitude': 'latitude',
        'decimalLongitude': 'longitude',
        'lat': 'latitude',
        'lng': 'longitude'
    }
    df_clean = df_clean.rename(columns=rename_map)

    if 'location' in df_clean.columns and 'latitude' not in df_clean.columns:
        df_clean[['latitude', 'longitude']] = df_clean['location'].str.split(',', expand=True).astype(float)

    if 'latitude' in df_clean.columns:
        df_clean['latitude'] = pd.to_numeric(df_clean['latitude'], errors='coerce')
    if 'longitude' in df_clean.columns:
        df_clean['longitude'] = pd.to_numeric(df_clean['longitude'], errors='coerce')

    df_clean = df_clean.dropna(subset=['latitude', 'longitude'])

    if 'bathymetry' in df_clean.columns:
        df_clean['bathymetry'] = df_clean['bathymetry'].abs()

    if 'shoredistance' in df_clean.columns:
        df_clean['shoredistance'] = df_clean['shoredistance'].abs()

    return df_clean