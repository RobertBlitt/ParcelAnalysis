# Geospatial Analysis Phase

**Academic Framework for Hawaii Cesspool Matrix Analysis**

## Purpose
Execute spatial analytical tools and scripts to calculate site characteristics for Matrix technology assessment. Focus on HAR 11-62 Individual Wastewater System requirements.

## Phase Components

### 02a_Slope_Analysis
- Calculate slope from DEM data
- Classify by HAR 11-62 thresholds (8%, 12%, 15%)
- Add slope class to foundation table

### 02b_Soil_Classification  
- Process NRCS soil data
- Convert saturated hydraulic conductivity (Ksat) to percolation rates
- Classify soil suitability for different IWS technologies

### 02c_Distance_Calculations
- Calculate distances to shoreline (50-foot setback per HAR 11-62)
- Calculate distances to surface water features (50-foot setback)
- Verify existing wells distances (1000-foot setback)

### 02d_Regulatory_Overlays
- Intersect with Special Management Areas (SMA)
- Check flood zone status (FEMA)  
- Add regulatory constraint flags

## HAR 11-62 Compliance Framework
All processing implements Individual Wastewater System regulatory requirements:
- Slope limitations for different technologies
- Setback distance requirements
- Soil percolation rate standards
- Groundwater separation requirements

## Key Processing Principles
- **Modular execution** - Each notebook runs independently
- **Quality validation** - Built-in error checking
- **JOIN_LOG updates** - Track all processing steps
- **Standardized outputs** - Consistent field naming

## Dependencies
- TMK_Foundation_Master from Phase 1
- DEM data (10-meter resolution)
- NRCS soil data (HIstate_nrcs_join2)
- Regulatory overlay shapefiles

## Outputs
- Enhanced foundation table with calculated characteristics
- Individual analysis results for validation
- Quality assessment reports
- Updated JOIN_LOG tracking

## Next Phase
After completion, data flows to **03_Data_Validation** for quality assurance before Matrix processing.
