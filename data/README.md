# Data Guide - ParcelAnalysis Project

**University of Hawaii Water Resources Research Center**  
**Project**: Hawaii Cesspool Technology Suitability Matrix  
**Purpose**: Planning-level technology feasibility assessment  
**Scope**: Statewide parcel analysis for onsite wastewater system replacement

---

## Overview

This directory contains all geospatial and tabular data for the cesspool replacement technology suitability analysis. Data are organized by processing state to maintain clear provenance and facilitate reproducible analysis.

**Key Principle**: Raw data are read-only; all transformations occur in interim, final products live in processed.

---

## Directory Structure and Usage

### `00_raw/` - Source Data (READ-ONLY)

**Purpose**: Original downloads exactly as received from source agencies  
**Status**: Immutable - DO NOT EDIT  
**Protection**: Set folder to read-only in Windows  
**Versioning**: Keep download date and URL in `04_docs/provenance_notes/`

#### Subdirectories:

| Folder | Contents | Typical Source | MPAT Fields Generated |
|--------|----------|----------------|----------------------|
| `parcels/` | County TMK parcel boundaries | County GIS portals | tmk, geometry, lot_size |
| `cesspools/` | DOH cesspool inventory | HI DOH | has_cesspool, cesspool_id |
| `slope/` | DEM-derived slope rasters | USGS/State GIS | slope_avg, pct_area_lt12, pct_area_lt20 |
| `soils/` | SSURGO soil polygons | USDA NRCS | soil_infil_class, hsg, drainage_class |
| `groundwater/` | Depth to water table | WRRC/CWRM | min_gw_depth, gw_shallow_flag |
| `wells_domestic/` | Domestic well points | DOH/USGS | dist_dom_well_m |
| `wells_municipal/` | Public supply wells | County/DOH | dist_mun_well_m |
| `shoreline/` | State shoreline | State GIS | dist_shoreline_m |
| `surface_water/` | Streams and water bodies | USGS NHD | dist_stream_m |
| `zoning/` | County zoning districts | County Planning | zone_class |
| `sma/` | Special Management Areas | County Planning | sma_flag |
| `flood/` | FEMA flood zones | FEMA NFHL | flood_zone |
| `tsunami/` | Evacuation zones | State/County | tsunami_flag |
| `habitat/` | Critical habitat | USFWS | habitat_flag |

**Data Acquisition Protocol:**
1. Download data from authoritative source
2. Save with original filename in appropriate raw subfolder
3. Record metadata in `04_docs/download_logs/YYYYMMDD_[dataset].md`:
   - Source URL
   - Download date
   - Dataset version/date
   - Contact information
   - License information
   - Known limitations

### `01_interim/` - Working Data (SCRATCH)

**Purpose**: Temporary workspace for data transformations  
**Status**: Mutable - safe to delete and regenerate  
**Typical Contents**:
- Reprojected layers (standardizing to UTM Zone 4, NAD 83)
- Clipped layers (county or island subsets)
- Cleaned attribute tables
- Join intermediates
- Processing logs

**Organization Tips:**
- Use descriptive names: `maui_parcels_reprojected_20251002.shp`
- Keep processing logs: `_processing_logs/[scriptname]_YYYYMMDD.txt`
- Delete once data moves to processed
- Use version dates to track iterations

### `02_processed/` - Analysis-Ready Data (FINAL)

**Purpose**: Clean, standardized, QC'd datasets ready for analysis  
**Status**: Semi-permanent - these are your deliverables  
**Key Products**:
- **Master_Parcel_Attribute_Table** (MPAT) - THE central product
- Classified soil layers with permeability
- Buildable area polygons (parcels minus buildings minus setbacks)
- Wells with regulatory buffer zones
- Matrix results (technology suitability per parcel)

**File Naming Convention:**
```
[dataset_name]_[county]_[version_date].[ext]

Examples:
MPAT_Maui_20251002.gdb
classified_soils_statewide_20251002.shp
matrix_results_Hawaii_20251002.csv
```

### `03_external/` - Small Reference Data (LIGHTWEIGHT)

**Purpose**: Lookup tables, regulatory thresholds, small reference datasets  
**Examples**:
- HAR 11-62 regulatory thresholds (CSV)
- Technology specifications lookup
- PITT code to land use crosswalk

### `04_docs/` - Data Documentation (TRACKED IN GIT)

**Purpose**: Provenance, metadata, data dictionaries  
**Subdirectories:**
- `data_dictionaries/` - Field definitions
- `licenses/` - Data use licenses
- `download_logs/` - Acquisition records
- `provenance_notes/` - Data lineage

---

## Master Parcel Attribute Table (MPAT) - Key Fields

See `04_docs/data_dictionaries/MPAT_Field_Dictionary.md` for complete definitions.

**Core**: tmk, island, county, coordinates  
**Physical**: lot_size, building_footprints, available_area, slope  
**Soils**: infiltration_class, hsg, drainage_class  
**Setbacks**: dist_wells, dist_shoreline, gw_depth  
**Regulatory**: sma_flag, flood_zone, zoning  
**Building**: bedrooms, dwelling_units, estimated_gpd

---

## Standard CRS

**UTM Zone 4, NAD 83 (HARN)** | EPSG: 26904

Defined in `../configs/paths.yaml`

---

## Workflow Summary

1. **Acquisition** → 00_raw (with documentation)
2. **Standardization** → 01_interim (reproject/clean)
3. **Calculation** → 01_interim (attributes)
4. **Assembly** → 02_processed (MPAT)
5. **Matrix** → 02_processed/matrix_results

---

## Disclaimers

**Planning-level analysis only**  
Site-specific verification required  
NOT a regulatory determination

---

**Version**: 1.0 | **Date**: October 2, 2025  
**Contact**: UH WRRC
