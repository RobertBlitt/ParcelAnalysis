# Data Acquisition and Standardization Guide
# Hawaii Cesspool Analysis Project - UPDATED FOR MATRIX REQUIREMENTS

## **🎯 UPDATED FOR MATRIX ANALYSIS (September 2024)**

**⚠️ This guide has been enhanced based on Matrix Technology Specification requirements and comprehensive HAR 11-62 Subchapter 3 analysis.**

**👉 FOR COMPLETE DATA REQUIREMENTS: See `../data/state_gis_downloads/MASTER_Data_Acquisition_Plan.md`**

---

## **Overview**

This guide provides the methodological framework for acquiring, standardizing, and quality-controlling all data layers needed for parcel-based Matrix technology analysis. The approach is specifically designed for Hawaii cesspool technology selection under HAR 11-62 Subchapter 3, but the framework is adaptable to other jurisdictions and analysis types.

## **Key Updates Based on Matrix Requirements**

### **✅ Enhanced Data Requirements**
- **16 critical data layers** identified for binary suitability analysis
- **County-by-county data collection** for varying regulatory environments
- **HAR 11-62 compliance focus** on Individual Wastewater Systems only
- **Technology-specific constraints** mapped to data requirements

### **✅ Regulatory Compliance Integration**
- **Setback calculations**: Wells (1000 ft), shoreline (50 ft), surface water (50 ft)
- **Site constraints**: Slope limits, soil percolation rates, groundwater separation
- **Lot size requirements**: 10,000 sq ft minimum per IWS
- **Environmental overlays**: SMA, critical habitat, flood zones

### **✅ Binary Decision Matrix Support**
Each data layer supports specific binary (1/0) suitability determinations:
- **Septic systems**: Slope <15%, lot size >10,000 sq ft, setbacks met
- **Aerobic Treatment Units**: More flexible constraints, electrical required
- **Alternative systems**: Site-specific requirements

---

## **Data Layer Requirements Matrix - UPDATED**

### **🚨 PRIORITY 1: Regulatory Compliance Data**
| Data Layer | HAR 11-62 Reference | Matrix Use | Critical Constraint |
|------------|-------------------|-------------|-------------------|
| **Water Wells** | Section 11-62-32, Table II | 1000 ft setbacks | Binary elimination |
| **Digital Elevation** | Slope limitations | Technology-specific limits | <15% for septic |
| **Soil Survey** | Section 11-62-33 | Percolation 1-60 min/in | Binary suitability |
| **Shoreline** | Section 11-62-32 | 50 ft coastal setback | Binary elimination |
| **Groundwater** | Section 11-62-32 | 3 ft vertical separation | Binary elimination |

### **🔴 PRIORITY 2: County-Specific Data (All 4 Counties)**
| Data Layer | County Variation | Matrix Use | Folder Structure |
|------------|-----------------|-------------|------------------|
| **TMK Parcels** | Different formats | Base spatial unit | `./parcels/[county]/` |
| **Zoning** | Local regulations | Residential filter | `./zoning/[county]/` |
| **Building Footprints** | County mapping | Available area calc | `./building_footprints/[county]/` |
| **Sewer Systems** | Local infrastructure | Centralized option | `./sewer_systems/[county]/` |
| **SMA Boundaries** | County CZM programs | Regulatory overlay | `./special_management_areas/[county]/` |

### **🟡 PRIORITY 3: Environmental Constraints**
| Data Layer | Source | Matrix Impact | Technology Effect |
|------------|--------|---------------|------------------|
| **Surface Water** | USGS/State | 50 ft setbacks | All technologies |
| **Flood Zones** | FEMA | Design modifications | Cost/complexity |
| **Critical Habitat** | USFWS/DLNR | Permit complexity | Timeline/cost |
| **DOH Priority Areas** | DOH Wastewater | Priority weighting | Implementation order |

---

## **Enhanced Hawaii-Specific Data Sources**

### **🏛️ State of Hawaii Sources - UPDATED CONTACTS**
- **Hawaii Statewide GIS**: https://geoportal.hawaii.gov/
- **DOH Wastewater Branch**: (808) 586-4400, wastewater@doh.hawaii.gov
- **CWRM Well Database**: (808) 587-0214
- **DLNR Environmental Data**: Various divisions

### **🏢 County Sources - VERIFIED CURRENT**
| County | GIS Portal | Priority Data Available |
|--------|-----------|----------------------|
| **Hawaii County** | https://higisupdates-hawaiicountygis.opendata.arcgis.com/ | TMK, Zoning, Buildings |
| **Maui County** | https://gis.mauicounty.gov/ | TMK, Zoning, SMA |
| **Honolulu County** | https://honolulu-cchnl.opendata.arcgis.com/ | TMK, Buildings, Sewer |
| **Kauai County** | https://kauai-county-gis-kauaicounty.hub.arcgis.com/ | TMK, Zoning, SMA |

### **🇺🇸 Federal Sources - CRITICAL FOR MATRIX**
- **USGS National Map**: https://apps.nationalmap.gov/downloader/ (DEM data)
- **NRCS Web Soil Survey**: https://websoilsurvey.sc.egov.usda.gov/ (Soil data)
- **FEMA**: Flood Insurance Rate Maps
- **USFWS**: Critical habitat boundaries

---

## **Matrix-Specific Standardization Requirements**

### **Spatial Reference System - HAWAII FOCUSED**
- **Primary**: Hawaii State Plane Zone 3 (EPSG:2783)
- **Alternative**: UTM Zone 4N (EPSG:32604) for statewide
- **Vertical**: NAVD88 (critical for groundwater analysis)

### **Field Naming Conventions - MATRIX ANALYSIS**
| Matrix Function | Field Prefix | Example | HAR 11-62 Application |
|-----------------|--------------|---------|---------------------|
| **Setback Distances** | DIST_ | DIST_WELL_FT | Regulatory compliance |
| **Site Characteristics** | SITE_ | SITE_SLOPE_PCT | Technology suitability |
| **Available Areas** | AVAIL_ | AVAIL_AREA_SF | System sizing |
| **Binary Results** | BIN_ | BIN_SEPTIC_OK | Suitability matrix |
| **Regulatory Status** | REG_ | REG_SMA_FLAG | Permit complexity |

### **Data Quality Standards - ENHANCED FOR MATRIX**
- **Spatial Accuracy**: ±5 feet (critical for setback calculations)
- **Attribute Completeness**: >95% for regulatory fields
- **Currency**: <2 years for dynamic data (wells, permits)
- **Consistency**: Standardized across all 4 counties

---

## **Matrix Decision Support Framework**

### **Binary Suitability Algorithm**
```yaml
# Matrix configuration example
septic_system_requirements:
  lot_size_min_sf: 10000
  well_setback_min_ft: 1000
  shoreline_setback_min_ft: 50
  slope_max_pct: 15
  soil_perc_min: 1
  soil_perc_max: 60
  groundwater_depth_min_ft: 3
  
aerobic_treatment_unit:
  lot_size_min_sf: 7500
  well_setback_min_ft: 100
  shoreline_setback_min_ft: 50
  slope_max_pct: 20
  electrical_required: true
  service_contract_required: true
```

### **County Configuration Management**
Each county requires specific configuration for:
- **Zoning code mappings** (residential classification)
- **SMA regulation variations**
- **Local permit requirements**
- **Infrastructure availability**

---

## **Updated Implementation Workflow**

### **Phase 1: State-Level Critical Data (Week 1)**
1. **Wells Database** (CWRM) - Setback calculations
2. **Digital Elevation** (USGS) - Slope analysis  
3. **Soil Survey** (NRCS) - Percolation rates
4. **Shoreline Data** (Hawaii GIS) - Coastal setbacks
5. **Groundwater Models** (CWRM/USGS) - Vertical separation

### **Phase 2: County Data Collection (Weeks 2-5)**
**Week 2: Hawaii County**
**Week 3: Maui County** 
**Week 4: Honolulu County**
**Week 5: Kauai County**

*Each week follows same pattern:*
- Day 1-2: TMK parcels and zoning
- Day 3: Building footprints
- Day 4: Sewer systems and SMA
- Day 5: Quality control and integration

### **Phase 3: Environmental Overlays (Week 6)**
- Surface water bodies
- Flood zones
- Critical habitat
- DOH priority areas

---

## **Enhanced Quality Control for Matrix Analysis**

### **Matrix-Specific QC Checklist**
- [ ] **Setback calculations verified** against HAR 11-62 Table II
- [ ] **Slope analysis validated** using known benchmarks
- [ ] **Soil data converted** to Hawaii DOH percolation standards
- [ ] **County data aligned** across all 4 jurisdictions
- [ ] **Binary logic tested** with sample parcels

### **Regulatory Compliance Validation**
- [ ] **HAR 11-62 Subchapter 3** requirements mapped to data
- [ ] **Technology specifications** match DOH approvals
- [ ] **County variations** documented and configured
- [ ] **Permit pathways** verified with agencies

### **Academic Documentation - ENHANCED**
- **Complete data provenance** for all 16 layers
- **Processing methodology** documented for reproducibility  
- **Quality control results** with statistical validation
- **Regulatory compliance verification**
- **County comparison analysis**

---

## **Integration with Matrix Technical System**

### **Data Flow to Matrix Analysis**
```
Raw County Data → Standardization → QC Validation → 
Matrix Analysis Engine → Binary Suitability → Technology Recommendations
```

### **Output Standards for Matrix**
- **Parcel-level results** for every eligible TMK
- **Technology rankings** with confidence scores
- **Regulatory pathway guidance**
- **Cost estimates** with local factors
- **Implementation priority** based on DOH areas

---

## **Future Enhancement Framework**

### **Automated Update Procedures**
- **County data monitoring** for new releases
- **Regulatory change tracking** (HAR 11-62 amendments)
- **Technology approval updates** (DOH equipment lists)
- **Quality metrics dashboard**

### **Multi-State Adaptation Template**
- **Configuration-driven approach** for other jurisdictions
- **Regulatory standard mappings** (Oregon, California, etc.)
- **Technology matrix variations** by state requirements
- **Academic framework replication**

---

## **Critical Success Factors**

### **Technical Requirements**
- ✅ **All 16 data layers** acquired and standardized
- ✅ **County variations** properly configured  
- ✅ **HAR 11-62 compliance** verified throughout
- ✅ **Matrix binary logic** functioning correctly

### **Academic Standards**
- ✅ **Complete methodology** documentation
- ✅ **Reproducible procedures** with version control
- ✅ **Quality validation** with statistical testing
- ✅ **Multi-jurisdictional applicability** demonstrated

### **Practical Utility**
- ✅ **Technology recommendations** for every parcel
- ✅ **Regulatory pathway** clarity
- ✅ **Implementation guidance** for counties
- ✅ **Homeowner accessibility** through web tools

---

**📋 This enhanced guide provides the complete methodological framework for Matrix-compliant data acquisition while maintaining academic rigor and regulatory compliance with HAR 11-62 Subchapter 3.**

**👉 Next Step: Begin Priority 1 data acquisition using the MASTER_Data_Acquisition_Plan.md**
