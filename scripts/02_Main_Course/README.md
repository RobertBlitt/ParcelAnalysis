# Main Course - Core Processing

Core data processing recipes

## Notebooks in this course:

- `02a_Soil_HAR_Classification.ipynb`
- `02b_Slope_Analysis.ipynb`
- `02c_Distance_Calculations.ipynb`
- `02d_Regulatory_Overlays.ipynb`

## Purpose
These are your "main dishes" - the core processing steps that transform raw data into analysis-ready layers. Each notebook is a complete "recipe" that can be run independently or swapped with alternative approaches.

## Key Features
- **Modular Design**: Each notebook is self-contained
- **Swappable Ingredients**: Easy to substitute different data sources
- **HAR 11-62 Compliant**: All processing follows Hawaii wastewater regulations
- **Matrix-Ready Outputs**: Results are formatted for technology compatibility analysis

## Current Recipes

### 02a_Soil_HAR_Classification.ipynb
- **Input**: HIstate_nrcs_join2 (NRCS soil data)
- **Output**: HAR 11-62 classified soil layer with Matrix compatibility
- **Key Functions**: 
  - Slope classification (<8%, 8-12%, >12%)
  - Ksat to percolation rate conversion
  - Technology compatibility assessment (Septic, ATU, Seepage Pit)

### Future Recipes (To be developed)
- **02b_Slope_Analysis**: DEM-derived slope calculations
- **02c_Distance_Calculations**: Proximity to wells, water bodies, etc.
- **02d_Regulatory_Overlays**: SMA, flood zones, zoning classifications

## Usage Pattern
```python
# Use default data source
%run 02a_Soil_HAR_Classification.ipynb

# Or swap ingredients first
soil_layer = "Alternative_Soil_Data"
%run 02a_Soil_HAR_Classification.ipynb
```

## Dependencies
- Kitchen Utils (99a_Common_Functions.py, 99b_HAR_11_62_Standards.py)
- Source data layers in your map
- TMK Foundation (from Appetizers)
