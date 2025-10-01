# Master Data Acquisition Plan - Matrix Technology Selection
# Hawaii Cesspool Analysis Project - Professional ArcGIS Pro Workflow

## **🎯 PROFESSIONAL ARCGIS PRO APPROACH**

This plan uses **standard GIS professional practices** with custom ArcGIS Pro tools for seamless workflow integration.

**Key HAR 11-62 Requirements Addressed:**
- **Site evaluation factors** (Section 11-62-31.2): Soil, slope, groundwater, flooding, area
- **Spacing requirements** (Section 11-62-32): Wells, shoreline, surface water, buildings  
- **Projection standardization**: NAD 83 HARN UTM Zone 4N (EPSG:26904) - HCPT compatible

---

## **📐 PROJECTION STANDARD: NAD 83 HARN UTM ZONE 4N (EPSG:26904)**

**✅ HCPT COMPATIBLE**: Matches existing HCPT projection exactly
**✅ AUTOMATED**: Custom ArcGIS Pro tool handles all reprojection
**✅ PROFESSIONAL**: Standard GIS workflow integration

---

## **🛠️ ARCGIS PRO TOOLBOX: "HAWAII MATRIX TOOLS"**

**Location**: `HawaiiMatrixTools.pyt` in your project root folder

### **Tool 1: "Check & Fix Projections" ⭐ PRIMARY TOOL**
- **One-click projection checking** for all downloaded data
- **Automatic reprojection** to HCPT standard
- **Progress tracking** in ArcGIS Messages window
- **Optional**: Add processed data directly to your map
- **Optional**: Create backups of original files

### **Tool 2: "Generate Data Inventory Report"**
- **Comprehensive data catalog** with projection info
- **Feature counts and extents** for all shapefiles  
- **Summary by projection status** (ready vs needs fix)
- **Exports to text file** for documentation

### **Tool 3: "Add All Data to Map"**
- **Organized layer management** by data type/county
- **Group layers** for clean map organization
- **Bulk data loading** for analysis setup

---

## **📊 REQUIRED DATA LAYERS (HAR 11-62 COMPLIANCE)**

### **📍 PRIORITY 1: REGULATORY COMPLIANCE DATA**

**1. Water Wells Database (CWRM) 🚨**
- **Source**: https://dlnr.hawaii.gov/cwrm/
- **HAR 11-62**: Section 11-62-32 setbacks (1000 ft)
- **Folder**: `data/gis_downloads/wells/`

**2. Digital Elevation Model (USGS) 🚨**
- **Source**: https://apps.nationalmap.gov/downloader/
- **HAR 11-62**: Section 11-62-31.2(b) slope evaluation
- **Folder**: `data/gis_downloads/elevation/`

**3. Soil Survey Data (NRCS) 🚨**
- **Source**: https://websoilsurvey.sc.egov.usda.gov/
- **HAR 11-62**: Section 11-62-31.2(e) percolation requirements
- **Folder**: `data/gis_downloads/soils/`

**4. Shoreline Boundaries 🚨**
- **Source**: https://geoportal.hawaii.gov/
- **HAR 11-62**: Section 11-62-32 coastal setbacks (50 ft)
- **Folder**: `data/gis_downloads/shoreline/`

**5. Groundwater Depth Data 🚨**
- **Source**: CWRM/USGS groundwater models
- **HAR 11-62**: Section 11-62-31.2(d) seasonal high water table
- **Folder**: `data/gis_downloads/groundwater/`

**6. Surface Water Bodies 🚨**
- **Source**: USGS National Hydrography Dataset
- **HAR 11-62**: Section 11-62-32 water body setbacks (50 ft)
- **Folder**: `data/gis_downloads/surface_water/`

**7. Flood Zones (FEMA) 🚨**
- **Source**: FEMA Flood Insurance Rate Maps
- **HAR 11-62**: Section 11-62-31.2(b) flooding hazard evaluation
- **Folder**: `data/gis_downloads/flood_zones/`

### **📍 PRIORITY 2: COUNTY PARCEL DATA**

**8-10. Tax Map Keys, Building Footprints, Zoning by County**
- **Sources**: County GIS portals (Hawaii, Maui, Honolulu, Kauai)
- **HAR 11-62**: Section 11-62-31.1 lot size requirements (10,000 sq ft)
- **Folders**: 
  - `data/gis_downloads/parcels/[county]/`
  - `data/gis_downloads/building_footprints/[county]/`
  - `data/gis_downloads/zoning/[county]/`

### **📍 PRIORITY 3: INFRASTRUCTURE CONTEXT**

**11-13. Sewer Systems, Special Management Areas, DOH Priority Areas**
- **Sources**: County Public Works, Hawaii State GIS, DOH
- **Purpose**: HCPT overlay integration, regulatory constraints
- **Folders**:
  - `data/gis_downloads/sewer_systems/[county]/`
  - `data/gis_downloads/special_management_areas/[county]/`
  - `data/gis_downloads/doh_priority_areas/`

---

## **🚀 PROFESSIONAL WORKFLOW**

### **📋 SIMPLE 4-STEP PROCESS:**

**STEP 1: Download GIS Data**
- Download to appropriate `gis_downloads` folders
- Any projection format (tool will standardize)

**STEP 2: Open ArcGIS Pro**
- Open your `ParcelAnalysis.aprx` project
- Navigate to **Catalog Pane**

**STEP 3: Run "Check & Fix Projections" Tool**
- Expand **Toolboxes** → **HawaiiMatrixTools.pyt**
- Double-click **"Check & Fix Projections"**
- **Tool automatically**:
  - Scans all your `gis_downloads` folders
  - Shows which files are ready vs need fixing
  - Reprojects any files to HCPT standard
  - Creates backups of originals
  - Adds processed data to your map

**STEP 4: Review Results**
- Check **Geoprocessing** → **Messages** for detailed log
- All data now ready for Matrix analysis
- Consistent HCPT-compatible projection

### **📊 WHAT YOU'LL SEE IN MESSAGES WINDOW:**
```
============================================================
HAWAII MATRIX PROJECT - PROJECTION CHECKER
Target: NAD 83 HARN UTM Zone 4N (EPSG:26904)
============================================================
Found 5 shapefile(s) to check

Checking: zoning\maui_county\cty_zoning_mau.shp
  ✓ Already correct - Ready for Matrix analysis

Checking: parcels\hawaii_county\tmk_parcels.shp
  ⚠ Wrong projection: WGS_1984 (EPSG:4326)
  → Reprojecting to NAD 83 HARN UTM Zone 4N...
  → Backup created: tmk_parcels_original.shp
  ✓ Reprojected successfully - Ready for Matrix analysis

============================================================
SUMMARY:
✓ Already ready for analysis: 1 files
🔧 Fixed and now ready: 4 files
All correctly projected data is ready for Matrix analysis!
============================================================
```

---

## **📁 CLEAN FOLDER STRUCTURE**

```
ParcelAnalysis/
├── data/
│   └── gis_downloads/           # All downloaded GIS data
│       ├── wells/
│       ├── elevation/
│       ├── soils/
│       ├── shoreline/
│       ├── groundwater/
│       ├── surface_water/
│       ├── flood_zones/
│       ├── doh_priority_areas/
│       ├── parcels/
│       │   ├── hawaii_county/
│       │   ├── maui_county/
│       │   ├── honolulu_county/
│       │   └── kauai_county/
│       ├── building_footprints/
│       │   └── [same county structure]
│       ├── zoning/
│       │   └── [same county structure]
│       ├── sewer_systems/
│       │   └── [same county structure]
│       └── special_management_areas/
│           └── [same county structure]
├── outputs/                     # Reports and analysis results
├── HawaiiMatrixTools.pyt       # Custom ArcGIS Pro toolbox ⭐
└── ParcelAnalysis.aprx         # Main ArcGIS Pro project
```

---

## **🎯 MATRIX DECISION LOGIC (UNCHANGED)**

The Matrix binary analysis remains the same, but now uses **standardized, HCPT-compatible data**:

**Parcel Eligibility** → **Setback Compliance** → **Site Evaluation** → **Technology Suitability**

All distance calculations now precise using UTM coordinates.

---

## **📞 CONTACT INFORMATION**

### **State Agencies**
- **CWRM**: (808) 587-0214 (Wells, Groundwater)
- **DOH Wastewater Branch**: (808) 586-4400, wastewater@doh.hawaii.gov
- **Hawaii State GIS**: https://geoportal.hawaii.gov/

### **County GIS Contacts**
- **Hawaii County**: Planning Dept GIS Division
- **Maui County**: GIS Division  
- **Honolulu County**: Department of Planning and Permitting GIS
- **Kauai County**: Planning Department GIS

### **Federal Agencies**
- **USGS**: Elevation Data, Water Resources
- **NRCS**: Soil Survey Data
- **FEMA**: Flood Insurance Rate Maps

---

**🎯 TOTAL: 13 Data Layers**
- **7 HAR 11-62 Required** (Priority 1)
- **3 Parcel-Level** (Priority 2) 
- **3 Infrastructure Context** (Priority 3)

**✅ PROFESSIONAL WORKFLOW**: One-click ArcGIS Pro tools
**✅ HCPT COMPATIBLE**: Standardized NAD 83 HARN UTM Zone 4N projection
**✅ FULLY AUTOMATED**: No manual reprojection needed

**📐 The HawaiiMatrixTools.pyt toolbox handles ALL projection standardization automatically within your professional ArcGIS Pro workflow.**
