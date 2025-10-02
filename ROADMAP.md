# ParcelAnalysis Implementation Roadmap

**University of Hawaii Water Resources Research Center**  
**Project**: Hawaii Cesspool Technology Suitability Matrix  
**Status**: Data Organization Phase Complete - Ready for Data Acquisition  
**Last Updated**: October 2, 2025

---

## Project Overview

Development of a parcel-level technology suitability assessment tool for cesspool replacement across Hawaii, feeding into the larger HCPT Infrastructure Feasibility Overlay project. The system evaluates each parcel against HAR 11-62 requirements and produces technology compatibility scores through The Matrix decision framework.

---

## Current Status: Phase 0 Complete ✓

**Folder structure established** with clear data state visibility  
**Documentation framework** in place (README, paths template, .gitignore)  
**GitHub repository** initialized with lightweight tracking  
**Matrix spreadsheet** development ongoing (nearly complete)

**Next Action**: Begin systematic data acquisition

---

## Implementation Phases

### **PHASE 1: Data Acquisition & Organization** (Weeks 1-2)

**Goal**: Populate `data/00_raw/` with all required statewide datasets

#### Priority 1 - Foundation Layers (Week 1)
- [ ] **Parcels**: Download from State GIS portal for all counties
  - Hawaii County: `https://geoportal.hawaii.gov/`
  - Maui County: `https://geoportal.hawaii.gov/`
  - Kauai County: `https://kauai-open-data-kauaigis.hub.arcgis.com/`
  - Honolulu: Separate download
  - Document in `data/04_docs/download_logs/YYYYMMDD_parcels.md`

- [ ] **Cesspools**: Obtain latest DOH cesspool inventory
  - Source: DOH Wastewater Branch
  - Both points and linked parcel TMKs
  - Document version and date

- [ ] **Wells**: Municipal and domestic well locations
  - Source: DOH Safe Drinking Water Branch
  - USGS National Water Information System
  - Verify 1000 ft municipal, 100 ft domestic setback compliance

- [ ] **Soils**: SSURGO data for Hawaii
  - Source: USDA NRCS
  - Must include: HSG, drainage class, texture, Ksat if available
  - Focus on fields needed for infiltration classification

#### Priority 2 - Physical Characteristics (Week 1-2)
- [ ] **Slope/DEM**: Digital Elevation Model
  - Source: USGS National Map, State GIS
  - 10m resolution minimum
  - For slope percentage calculation

- [ ] **Building Footprints**: All counties
  - Completed: Hawaii County ✓
  - Completed: Kauai County ✓
  - Needed: Maui County, Honolulu
  - Source: Microsoft/USGS Building Footprints

- [ ] **Groundwater Depth**: Depth to water table
  - Source: WRRC, CWRM
  - Critical for 3 ft separation requirement
  - May need modeling for data gaps

#### Priority 3 - Regulatory Overlays (Week 2)
- [ ] **Shoreline**: Official state shoreline
  - For 50 ft setback calculation

- [ ] **Special Management Areas**: County SMA boundaries
  - Required for permitting considerations

- [ ] **Flood Zones**: FEMA NFHL
  - Planning overlay (not HAR requirement)

- [ ] **Zoning**: County zoning districts
  - Affects technology placement constraints

- [ ] **Surface Water**: Streams, lakes, water bodies
  - USGS National Hydrography Dataset

#### Priority 4 - Optional Overlays (As Available)
- [ ] Tsunami evacuation zones
- [ ] Critical habitat designations
- [ ] Additional regulatory overlays

---

### **PHASE 2: Data Standardization** (Week 3)

**Goal**: Transform raw data into analysis-ready format in `01_interim/`

**Script**: `scripts/01_standardization/standardize_all_layers.py`

Tasks:
- [ ] Create standardization script that reads `configs/paths.yaml`
- [ ] Reproject all layers to EPSG:26904 (UTM Zone 4, NAD 83 HARN)
- [ ] Clip to study area extent if needed
- [ ] Standardize field names to match MPAT schema
- [ ] Clean attribute tables (remove unnecessary fields)
- [ ] Validate geometries and repair if needed
- [ ] Log all transformations to `01_interim/_processing_logs/`
- [ ] Quality control checks for each layer

**Outputs**: Standardized layers in `01_interim/reprojected/`

---

### **PHASE 3: Attribute Calculation** (Week 4)

**Goal**: Calculate all spatial attributes needed for MPAT

#### 3A: Physical Metrics
**Script**: `scripts/02_attribute_calculation/calculate_physical_metrics.py`

- [ ] Lot size (square feet and acres)
- [ ] Building footprint sum per parcel
- [ ] Available area (lot - buildings)
- [ ] Net buildable area (available × 0.85 usability factor)
- [ ] Average slope across parcel (zonal statistics from DEM)
- [ ] Percent area <12% slope
- [ ] Percent area <20% slope

#### 3B: Distance Calculations
**Script**: `scripts/02_attribute_calculation/calculate_distances.py`

- [ ] Distance to nearest municipal well
- [ ] Distance to nearest domestic well  
- [ ] Distance to shoreline
- [ ] Distance to nearest stream/water body
- [ ] Buffer compliance flags (YES/NO for each setback)

#### 3C: Soil Classification
**Script**: `scripts/02_attribute_calculation/classify_soil_infiltration.py`

- [ ] Implement composite infiltration classification methodology
- [ ] HSG-based scoring (A=100, B=75, C=50, D=25)
- [ ] Drainage class modifier
- [ ] Texture validation
- [ ] Buildable area weighted averaging
- [ ] 20% unsuitable threshold check
- [ ] Assign final infiltration class (HIGH/MODERATE/LOW/UNSUITABLE/UNKNOWN)
- [ ] Calculate confidence scores

#### 3D: Groundwater Assessment
**Script**: `scripts/02_attribute_calculation/assess_groundwater.py`

- [ ] Extract minimum groundwater depth per parcel
- [ ] Flag parcels with <3 ft separation (shallow GW)
- [ ] Interpolate where data gaps exist (if possible)
- [ ] Document confidence levels

---

### **PHASE 4: Master Parcel Attribute Table Assembly** (Week 5)

**Goal**: Create the definitive MPAT with all attributes joined

**Script**: `scripts/04_mpat_builder/build_mpat.py`

Tasks:
- [ ] Start with cesspool parcels as base layer
- [ ] Spatially join all calculated attributes
- [ ] Join tabular data (bedroom counts, PITT codes)
- [ ] Calculate derived fields:
  - Estimated GPD (200 × bedrooms × dwelling units)
  - Required drain field area (from HAR 11-62 lookup)
- [ ] Add metadata fields:
  - MPAT version
  - Processing date
  - Data quality score
  - Confidence levels
- [ ] Run comprehensive validation:
  - Check for null values in required fields
  - Verify geometric validity
  - Confirm all parcels have complete attributes
  - Generate validation report
- [ ] Export MPAT to:
  - `02_processed/MPAT_[date].gdb/Complete_Master_Analysis_Table`
  - `02_processed/MPAT_[date].csv` (for Matrix processing)
  - `02_processed/MPAT_[date]_metadata.txt`

**Validation Checklist**:
- [ ] All TMKs unique
- [ ] No null values in critical fields
- [ ] Geometric topology valid
- [ ] All distances >0
- [ ] Slope values 0-100%
- [ ] Soil classes assigned
- [ ] Data quality scores calculated

---

### **PHASE 5: Matrix Integration** (Week 6)

**Goal**: Process MPAT through Matrix to generate technology suitability

#### 5A: Matrix Spreadsheet Finalization
- [ ] Complete Matrix binary logic for all 24 technologies
- [ ] Verify HAR 11-62 compliance rules
- [ ] Add regulatory threshold lookups
- [ ] Document all decision rules in `matrix/Matrix_Logic_Documentation.md`
- [ ] Peer review with regulatory experts

#### 5B: Matrix Processing Pipeline
**Script**: `scripts/05_matrix_processor/run_matrix_analysis.py`

- [ ] Load MPAT CSV into memory
- [ ] Apply Matrix decision rules for each technology
- [ ] Generate binary suitability fields (0/1 for each tech)
- [ ] Calculate technology scores (sum of compatible options)
- [ ] Identify "limiting factors" for each parcel
- [ ] Classify parcels into suitability tiers:
  - Tier 1: Multiple options available (score ≥3)
  - Tier 2: Limited options (score 1-2)
  - Tier 3: No standard options (score 0, ATU required)
- [ ] Export results to `02_processed/matrix_results_[date].csv`
- [ ] Join results back to MPAT geodatabase

#### 5C: Results Validation
- [ ] Spot-check random parcels for logic errors
- [ ] Verify regulatory compliance
- [ ] Test edge cases (e.g., very small lots, steep slopes)
- [ ] Document any anomalies or required manual review

---

### **PHASE 6: Visualization & Deliverables** (Week 7-8)

**Goal**: Create maps, reports, and user-facing products

#### 6A: Map Production
- [ ] Statewide overview map (suitability tiers)
- [ ] County detail maps
- [ ] Technology-specific feasibility maps
- [ ] Limiting factor heat maps
- [ ] High-priority cluster identification

#### 6B: Reports & Tables
- [ ] Summary statistics by county
- [ ] Technology feasibility percentages
- [ ] Limiting factor frequency analysis
- [ ] Data quality assessment report
- [ ] Methodology documentation

#### 6C: Web Tool Integration (If Applicable)
- [ ] Export to web-friendly formats (GeoJSON)
- [ ] Prepare attribute table for web display
- [ ] Create simplified parcel summaries
- [ ] Develop query interfaces

---

## Key Milestones & Deliverables

| Milestone | Target Date | Deliverable |
|-----------|-------------|-------------|
| Data acquisition complete | End Week 2 | All layers in `00_raw/` with documentation |
| Standardization complete | End Week 3 | Clean layers in `01_interim/` |
| Attributes calculated | End Week 4 | All metrics computed |
| MPAT assembled | End Week 5 | Complete MPAT in `02_processed/` |
| Matrix processing complete | End Week 6 | Technology suitability results |
| Deliverables finalized | End Week 8 | Maps, reports, validated outputs |

---

## Critical Dependencies

**Data Access**:
- DOH cesspool inventory (may require data sharing agreement)
- County parcel data (publicly available)
- WRRC groundwater data (internal access)

**Technical Resources**:
- ArcGIS Pro license with Spatial Analyst
- Python environment with arcpy
- Sufficient storage (~50 GB for all data)

**Expertise**:
- Regulatory review of Matrix logic (DOH input)
- Soil science consultation (NRCS or UH faculty)
- GIS peer review of methodology

---

## Risk Mitigation

**Data Availability Risks**:
- Groundwater depth may have gaps → Use interpolation or assign UNKNOWN with caveats
- Building footprints incomplete → Estimate from tax assessor data or conservative assumptions
- Soil data missing for some areas → Flag as low confidence, require site-specific testing

**Technical Risks**:
- Large dataset processing times → Implement chunking and parallel processing
- Memory limitations → Process by county if needed
- Geodatabase corruption → Maintain backup copies at each phase

**Regulatory Risks**:
- Matrix logic errors → Thorough peer review and validation
- HAR 11-62 interpretation → Document assumptions and get DOH feedback
- Liability concerns → Prominent disclaimers about planning-level use only

---

## Success Criteria

1. **Complete statewide coverage**: All cesspool parcels have MPAT attributes
2. **Data quality**: >90% of parcels have HIGH or MEDIUM confidence scores
3. **Matrix validation**: Zero logical errors in technology compatibility rules
4. **Regulatory compliance**: All HAR 11-62 requirements correctly implemented
5. **Usability**: Clear documentation enables others to replicate and update
6. **Portability**: Framework can be adapted to other jurisdictions

---

## Next Actions (This Week)

### Immediate Tasks:
1. **Finalize Matrix spreadsheet** - Complete last technology compatibility rules
2. **Begin data downloads** - Start with parcels and cesspools (Priority 1)
3. **Set up data folders** - Create all `00_raw/` subdirectories
4. **Copy paths template** - Duplicate `paths.example.yaml` to `paths.yaml` and customize

### Communication:
- Email DOH for latest cesspool inventory
- Confirm WRRC groundwater data access
- Schedule Matrix peer review session

---

## Long-Term Maintenance Plan

**Annual Updates**:
- Refresh parcel boundaries
- Update cesspool conversion status
- Incorporate new building footprints
- Validate soil data currency

**Documentation**:
- Maintain CHANGELOG.md for all data refreshes
- Update provenance notes in `04_docs/`
- Archive previous MPAT versions

**Quality Assurance**:
- Annual validation against known site conditions
- Periodic regulatory compliance review
- User feedback integration

---

**Document Version**: 1.0  
**Last Updated**: October 2, 2025  
**Project Lead**: [Your Name], UH WRRC  
**Status**: Phase 0 Complete - Ready to Begin Phase 1
