# MPAT Development Scripts

This folder contains scripts and notebooks for building the Master Parcel Attribute Table (MPAT) for the Hawaii Cesspool Infrastructure Feasibility Overlay project.

## Purpose

The MPAT is the foundation data table that will contain all spatial and regulatory characteristics needed to run parcels through The Matrix technology suitability analysis. Each record is keyed to TMK (Tax Map Key) and includes:

- Physical site characteristics (slope, lot size, soil percolation)
- Distance to regulatory features (wells, shoreline, surface water)  
- Regulatory overlays (Special Management Areas, flood zones)
- Building characteristics (bedrooms, estimated wastewater flow)

## Files in This Folder

### Scripts
- **01_MPAT_Wells_Join.py** - Joins municipal and domestic wells distance data
- **02_MPAT_Slope_Analysis.py** *(coming next)* - Adds slope analysis from DEM
- **03_MPAT_Soil_Data.py** *(planned)* - Adds NRCS soil percolation data
- **04_MPAT_Regulatory_Overlays.py** *(planned)* - Adds SMA and flood zones
- **05_MPAT_Building_Data.py** *(planned)* - Adds bedroom counts and wastewater calculations
- **06_MPAT_Final_Assembly.py** *(planned)* - Final quality checks and export

### Documentation
- **MPAT_Development_Notebook.ipynb** - Jupyter notebook documenting the entire process

## Usage

### Step 1: Wells Distance Data (READY TO RUN)

**In ArcGIS Python Window:**
```python
exec(open(r'C:/Users/rober/OneDrive/Documents/GIS_Projects/ParcelAnalysis/scripts/mpat_development/01_MPAT_Wells_Join.py').read())
```

**Expected Output:** Creates `MPAT_Wells_Joined` table in geodatabase

### Documentation

**Open Jupyter Notebook:**
```bash
jupyter notebook MPAT_Development_Notebook.ipynb
```

Run all cells to document progress and assess data quality.

## Development Approach

- **Incremental builds**: Each script adds data to the growing MPAT table
- **Quality checks**: Built-in validation and error reporting
- **Documentation**: Full process documented in Jupyter notebook
- **Reproducible**: Scripts can be re-run with updated data

## Integration with Matrix Analysis

The completed MPAT will feed directly into The Matrix technology suitability analysis, providing all necessary site characteristics to determine which wastewater treatment technologies are feasible for each parcel.

## Current Status

✅ **Step 1:** Wells distance data join - SCRIPT READY  
⏳ **Step 2:** Slope analysis - IN DEVELOPMENT  
⏳ **Steps 3-6:** Additional data layers - PLANNED  

---

*Part of the Hawaii Cesspool Prioritization Tool (HCPT) Infrastructure Feasibility Overlay project*
