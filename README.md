# WhaLife
## User Guide
First, clone the repository:
```bash
git clone https://github.com/lou-kail/WhaLife.git
cd whalife
```
It is necessary to install the required libraries before installation:
```bash
pip install -r requirements.txt
```
To run the code simply type the following command at the root of the project:
```bash
python3 main.py
```
## Data
[Data source page](https://obis.org/taxon/1370)

The data comes from the Ocean Biodiversity Information System and gathers data on numerous cetaceans.
We only process data concerning Humpback Whales, blue whales, orcas and dolphins.
It is then possible to analyze the population of a species according to years, their location, the depth at which the animal was detected, the distance from the coasts, the water temperature and the water salinity
## Developer Guide
The project is structured in a modular way:
- main.py: Application entry point. Manages dashboard initialization, data loading and routing.
- config.py: Contains global constants (taxon IDs, descriptive texts).
- src/components/: Contains reusable interface elements (Header, Map, Histogram, 3D Visualizer).
- src/pages/: Contains layouts specific to each analysis page (species.py, depth.py, etc.).
- src/utils/: Contains API retrieval and Pandas cleaning scripts.
- assets/: Contains project resources (CSS, 3D models, images).
## Analysis Report
- Distribution: The dashboard highlights on a map that the different species have very different living environments. For example, dolphins seem to live near American, European and Australian coasts while orcas have a very wide distribution particularly in the Pacific Ocean.
- Temperature: The analysis of sea surface temperatures (SST) shows the distinct thermal preferences between polar and temperate species.
- Depth: The depth graphs make it possible to distinguish coastal species from species that frequent deep waters.
## Copyright
I declare on my honor that the code provided was produced by Lou Kail and Théo Séré, with the exception of the elements below:
- Third-party libraries: The application relies on the open-source libraries Dash, Pandas and Plotly.
- Font: The imported font is Gluten, retrieved from Google Fonts
- 3D models: The .glb files present in the assets/ folder (whales, orcas, dolphins) are illustrative models
- Data: The data comes from OBIS.
- API Snippet: The API connection logic in src/utils/get_data.py is inspired by the official OBIS API documentation.
  
Any line not declared above is deemed to be produced by the author (or authors) of the project. The absence or omission of declaration will be considered plagiarism.
