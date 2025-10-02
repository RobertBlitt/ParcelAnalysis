# Data Acquisition Checklist - Phase 1

**Hawaii Cesspool Technology Suitability Matrix**  
**Target**: Complete Priority 1 datasets by end of Week 2  
**Status**: [ ] Not Started | [ ] In Progress | [ ] Complete

---

## Overview

This checklist guides systematic acquisition of all foundation datasets needed for the Master Parcel Attribute Table (MPAT). Each dataset must be documented in `data/04_docs/download_logs/` before moving to processing.

**Critical Rule**: Never edit files in `data/00_raw/` - this folder should be set to READ-ONLY.

---

## Priority 1: Foundation Layers (Week 1)

### 1. Parcels (Tax Map Key Boundaries)

**Importance**: ⭐⭐⭐⭐⭐ (Absolutely critical - base layer for all analysis)

#### Hawaii County
- [ ] Downloaded from: https://geoportal.hawaii.gov/
- [ ] Search for: "Hawaii County Parcels" or "TMK"
- [ ] Save to: `data/00_raw/parcels/Hawaii_TMK_[date].zip`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_parcels_hawaii.md`
- [ ] Verify fields include: TMK, OWNER, PITTCODE, TAXACRES, geometry
- [ ] Note native CRS in download log

#### Maui County
- [ ] Downloaded from: https://geoportal.hawaii.gov/
- [ ] Search for: "Maui County Parcels" or "TMK"
- [ ] Save to: `data/00_raw/parcels/Maui_TMK_[date].zip`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_parcels_maui.md`
- [ ] Verify fields include: TMK, OWNER, PITTCODE, TAXACRES
- [ ] Note: Includes Maui, Molokai, Lanai

#### Kauai County
- [ ] Downloaded from: https://kauai-open-data-kauaigis.hub.arcgis.com/
- [ ] Search for: "Parcels" or "TMK"
- [ ] Save to: `data/00_raw/parcels/Kauai_TMK_[date].zip`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_parcels_kauai.md`
- [ ] Verify fields include: TMK, PARID, PITTCODE, TAXACRES

#### Honolulu (City & County)
- [ ] Downloaded from: https://geoportal.hawaii.gov/ or Honolulu GIS portal
- [ ] Search for: "Honolulu Parcels" or "Oahu TMK"
- [ ] Save to: `data/00_raw/parcels/Honolulu_TMK_[date].zip`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_parcels_honolulu.md`
- [ ] Verify fields include: TMK, OWNER, land use codes

**Quality Checks**:
- [ ] All files downloaded without corruption (check file sizes)
- [ ] TMK field exists in all datasets
- [ ] Geometries are valid polygons
- [ ] Coverage extends to entire county
- [ ] Native CRS documented for each county

---

### 2. Cesspools (DOH Inventory)

**Importance**: ⭐⭐⭐⭐⭐ (Critical - defines study parcels)

#### Option A: Direct from DOH
- [ ] Contact: DOH Wastewater Branch
  - Phone: (808) 586-4294
  - Email: doh.wastewater@doh.hawaii.gov
- [ ] Request: Latest cesspool inventory (point locations + TMK table)
- [ ] Preferred format: Geodatabase or Shapefile with coordinates
- [ ] Save to: `data/00_raw/cesspools/DOH_Cesspool_Inventory_[date].gdb`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_cesspools_doh.md`

#### Option B: HCPT Database (If Available)
- [ ] Check existing HCPT project files
- [ ] Location: [Check with PI - may already have access]
- [ ] Copy to: `data/00_raw/cesspools/HCPT_Cesspools_[date].gdb`
- [ ] Document source and version

**Required Fields**:
- [ ] TMK (9-digit)
- [ ] Coordinates (latitude/longitude or X/Y)
- [ ] County
- [ ] Island
- [ ] Installation date (if available)
- [ ] Status (active/inactive)

**Quality Checks**:
- [ ] Record count matches expected (~88,000 statewide)
- [ ] TMKs are valid and match parcel layer format
- [ ] Coordinates fall within Hawaii boundaries
- [ ] No duplicate records (check TMK uniqueness)

---

### 3. Wells (Municipal and Domestic)

**Importance**: ⭐⭐⭐⭐⭐ (Critical - HAR 11-62 setback requirements)

#### Municipal Wells (1000 ft setback)
- [ ] Source 1: DOH Safe Drinking Water Branch
  - Contact: (808) 586-4258
  - Request: Public water system source locations
- [ ] Source 2: County water departments
  - May have more current data
- [ ] Save to: `data/00_raw/wells_municipal/Municipal_Wells_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_wells_municipal.md`

#### Domestic Wells (100 ft setback)
- [ ] Source: USGS National Water Information System
  - URL: https://waterdata.usgs.gov/nwis
  - Select: Hawaii, Groundwater, Site Type: Well
- [ ] Alternate: DOH well completion reports database
- [ ] Save to: `data/00_raw/wells_domestic/Domestic_Wells_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_wells_domestic.md`

**Required Fields**:
- [ ] Well ID
- [ ] Coordinates
- [ ] Well type (municipal/domestic)
- [ ] Status (active/inactive)
- [ ] Depth (if available)

**Quality Checks**:
- [ ] Wells are within Hawaii boundaries
- [ ] Coordinates are accurate (not placeholder values)
- [ ] Municipal and domestic wells clearly distinguished
- [ ] No obvious duplicates

---

### 4. Soils (NRCS SSURGO)

**Importance**: ⭐⭐⭐⭐⭐ (Critical - drives infiltration classification)

#### Download Instructions
- [ ] Source: USDA NRCS Web Soil Survey
  - URL: https://websoilsurvey.nrcs.usda.gov/
- [ ] Area of Interest: Draw around each island separately
- [ ] Download: Spatial and tabular data (SSURGO format)
- [ ] Save to: `data/00_raw/soils/SSURGO_Hawaii_[date].gdb`
- [ ] For each island: Hawaii, Maui, Molokai, Lanai, Oahu, Kauai

**Critical Fields to Verify**:
- [ ] MUKEY (Map Unit Key)
- [ ] Hydrologic Soil Group (HSG) - A, B, C, D
- [ ] Drainage Class
- [ ] Soil Texture
- [ ] Ksat (saturated hydraulic conductivity) - if available
- [ ] Depth to restrictive layer
- [ ] Depth to water table

**Tables to Download**:
- [ ] Component table (soil series information)
- [ ] Horizon table (depth and properties)
- [ ] Map unit aggregated attributes

**Quality Checks**:
- [ ] Coverage complete for all islands
- [ ] HSG field populated for >80% of records
- [ ] Drainage class field populated
- [ ] Join to spatial layer successful

---

## Priority 2: Physical Characteristics (Week 1-2)

### 5. Digital Elevation Model (DEM)

**Importance**: ⭐⭐⭐⭐ (High - needed for slope calculation)

#### Download Instructions
- [ ] Source: USGS National Map
  - URL: https://apps.nationalmap.gov/downloader/
- [ ] Product: 1/3 arc-second DEM (~10m resolution)
- [ ] Coverage: All Hawaiian Islands
- [ ] Format: GeoTIFF preferred
- [ ] Save to: `data/00_raw/slope/Hawaii_DEM_10m_[date].tif`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_dem_usgs.md`

**Alternative Source**:
- [ ] Hawaii State GIS portal may have pre-processed DEMs
- [ ] Check for island-specific higher resolution DEMs

**Quality Checks**:
- [ ] CRS is geographic or UTM (document which)
- [ ] No data voids in study areas
- [ ] Elevation values reasonable (0 to ~4200m for Big Island)
- [ ] File size appropriate (~1-5 GB total)

---

### 6. Building Footprints

**Importance**: ⭐⭐⭐⭐ (High - needed for buildable area calculation)

**Status Check**:
- [✓] Hawaii County - COMPLETE (already extracted)
- [✓] Kauai County - COMPLETE (already extracted)
- [ ] Maui County - NEEDED
- [ ] Honolulu - NEEDED

#### Microsoft/USGS Building Footprints
- [ ] Source: https://github.com/microsoft/USBuildingFootprints
- [ ] Hawaii download: https://usbuildingdata.blob.core.windows.net/usbuildings-v2/Hawaii.geojson.zip
- [ ] Save to: `data/00_raw/building_footprints/USA_Buildings_Hawaii_[date].zip`
- [ ] Extract subsets for each county
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_buildings_microsoft.md`

**For Maui and Honolulu**:
- [ ] Use same extraction method as Hawaii/Kauai counties
- [ ] Select by location using county parcels
- [ ] Export to: `data/00_raw/building_footprints/[County]_Buildings_Raw.shp`

**Quality Checks**:
- [ ] Buildings fall within expected county boundaries
- [ ] Footprint sizes reasonable (not just points)
- [ ] Coverage appears complete for developed areas

---

### 7. Groundwater Depth

**Importance**: ⭐⭐⭐⭐ (High - 3 ft separation requirement)

#### Data Sources (in order of preference)
- [ ] **Option A**: WRRC internal data
  - Contact: [Your PI or water resources faculty]
  - Depth to water table models or measurements
  - Save to: `data/00_raw/groundwater/WRRC_GW_Depth_[date].tif`

- [ ] **Option B**: Commission on Water Resource Management (CWRM)
  - URL: https://dlnr.hawaii.gov/cwrm/
  - Request: Groundwater level data
  - May need to interpolate from monitoring wells

- [ ] **Option C**: USGS Groundwater Information
  - URL: https://waterdata.usgs.gov/hi/nwis/gw
  - Download water level measurements
  - Will require spatial interpolation

**Quality Checks**:
- [ ] Data coverage adequate for study areas
- [ ] Units clearly documented (feet below ground surface)
- [ ] Temporal currency noted (seasonal variation important)
- [ ] Confidence/uncertainty documented

**If Data Gaps Exist**:
- [ ] Document extent of coverage
- [ ] Identify areas needing interpolation
- [ ] Flag parcels with unknown GW depth for lower confidence

---

## Priority 3: Regulatory Overlays (Week 2)

### 8. Shoreline

**Importance**: ⭐⭐⭐ (Medium-High - 50 ft setback requirement)

- [ ] Source: Hawaii State GIS
  - URL: https://geoportal.hawaii.gov/
  - Search for: "Shoreline" or "Coastal Zone"
- [ ] Save to: `data/00_raw/shoreline/Hawaii_Shoreline_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_shoreline.md`

**Quality Checks**:
- [ ] Complete coverage for all islands
- [ ] Shoreline follows expected coastline
- [ ] CRS documented

---

### 9. Special Management Areas (SMA)

**Importance**: ⭐⭐⭐ (Medium - permitting consideration)

#### County-Specific Downloads
- [ ] Hawaii County SMA
- [ ] Maui County SMA
- [ ] Kauai County SMA
- [ ] Honolulu SMA

**Source**: Individual county planning departments or State GIS
- [ ] Save to: `data/00_raw/sma/[County]_SMA_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_sma.md`

---

### 10. Flood Zones

**Importance**: ⭐⭐ (Medium - planning overlay, not HAR requirement)

- [ ] Source: FEMA National Flood Hazard Layer (NFHL)
  - URL: https://msc.fema.gov/portal/advanceSearch
  - Search by: Hawaii counties
- [ ] Download format: Geodatabase preferred
- [ ] Save to: `data/00_raw/flood/FEMA_NFHL_Hawaii_[date].gdb`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_flood_fema.md`

**Required Fields**:
- [ ] FLD_ZONE (flood zone designation)
- [ ] ZONE_SUBTY (subtype)
- [ ] SFHA_TF (Special Flood Hazard Area flag)

---

### 11. Zoning

**Importance**: ⭐⭐⭐ (Medium - may constrain technology placement)

#### County-Specific Downloads
- [ ] Hawaii County zoning
- [ ] Maui County zoning
- [ ] Kauai County zoning
- [ ] Honolulu zoning

**Source**: Individual county planning departments
- [ ] Save to: `data/00_raw/zoning/[County]_Zoning_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_zoning.md`

**Required Fields**:
- [ ] Zoning code/classification
- [ ] Zoning description
- [ ] Residential vs. non-residential flag

---

### 12. Surface Water

**Importance**: ⭐⭐ (Low-Medium - optional setback consideration)

- [ ] Source: USGS National Hydrography Dataset (NHD)
  - URL: https://www.usgs.gov/national-hydrography/access-national-hydrography-products
- [ ] Download: NHD Hawaii (Flowlines and Water bodies)
- [ ] Save to: `data/00_raw/surface_water/NHD_Hawaii_[date].gdb`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_surface_water_usgs.md`

**Components**:
- [ ] NHDFlowline (streams and rivers)
- [ ] NHDWaterbody (lakes and ponds)
- [ ] NHDArea (additional water features)

---

## Priority 4: Optional Overlays (As Available)

### 13. Tsunami Evacuation Zones

**Importance**: ⭐ (Low - planning context only)

- [ ] Source: State/County Civil Defense
- [ ] Save to: `data/00_raw/tsunami/Hawaii_Tsunami_Zones_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_tsunami.md`

---

### 14. Critical Habitat

**Importance**: ⭐ (Low - planning context only)

- [ ] Source: USFWS Critical Habitat Portal
  - URL: https://ecos.fws.gov/ecp/report/table/critical-habitat.html
- [ ] Filter for: Hawaii
- [ ] Save to: `data/00_raw/habitat/USFWS_Critical_Habitat_HI_[date].shp`
- [ ] Document in: `data/04_docs/download_logs/[YYYYMMDD]_habitat.md`

---

## Documentation Requirements

### For EVERY Dataset Downloaded:

Create a log file: `data/04_docs/download_logs/YYYYMMDD_[dataset_name].md`

**Include**:
1. Dataset name and purpose
2. Source agency and URL
3. Download date and who downloaded it
4. Dataset version or date
5. Contact information
6. File format and size
7. Native CRS/projection
8. Record count
9. License and usage restrictions
10. Known limitations or issues
11. Relevant fields/attributes
12. Processing needed (reprojection, clipping, etc.)

**Template available**: `data/04_docs/download_logs/[DATE]_TEMPLATE.md`

---

## Progress Tracking

### Week 1 Summary
**Target**: Priority 1 datasets (parcels, cesspools, wells, soils)

Downloaded: _____ / 4 critical datasets  
Documented: _____ / 4 logs completed  
Quality checked: _____ / 4 passed QC

### Week 2 Summary
**Target**: Priority 2-3 datasets (DEM, buildings, GW, overlays)

Downloaded: _____ / 8 additional datasets  
Documented: _____ / 8 logs completed  
Quality checked: _____ / 8 passed QC

### Overall Phase 1 Status

Total datasets acquired: _____ / 14  
Total documentation complete: _____ / 14  
Ready for standardization: [ ] YES [ ] NO

**Blockers/Issues**:
- 
- 
- 

**Notes**:
- 
- 
- 

---

## Next Phase

When Phase 1 is complete:
1. Set `data/00_raw/` to READ-ONLY in Windows
2. Run initial QC checks on all datasets
3. Begin Phase 2: Data Standardization (ROADMAP Week 3)
4. Create `configs/paths.yaml` from template

---

**Document Version**: 1.0  
**Last Updated**: October 2, 2025  
**Owner**: [Your Name]  
**Review Date**: End of Week 2
