# Master Data Acquisition Plan - Matrix Technology Selection
# Hawaii Cesspool Analysis Project - HAR 11-62 Subchapter 3 Compliance ONLY

## **🎯 REQUIREMENTS BASED SOLELY ON HAR 11-62 SUBCHAPTER 3**

This plan identifies data layers needed for the binary technology suitability analysis based **exclusively** on HAR 11-62 Subchapter 3 requirements for Individual Wastewater Systems (IWS).

**Key HAR 11-62 Site Evaluation Requirements (Section 11-62-31.2):**
- **Soil factors and percolation testing**
- **Depth to seasonal high groundwater** (minimum 3 ft separation)
- **Land slope** (affects disposal system design)  
- **Flooding hazard** (explicitly mentioned)
- **Amount of suitable area available**

**Key HAR 11-62 Spacing Requirements (Section 11-62-32, Table II):**
- **Distance to water wells** (private: 100 ft, public: 150 ft)
- **Distance to shoreline** (50 ft minimum)
- **Distance to surface water** (50 ft minimum)
- **Distance to buildings** (10 ft minimum)

---

## **📐 PROJECTION STANDARD: NAD 83 HARN UTM ZONE 4N (EPSG:26904)**

**✅ CONFIRMED HCPT COMPATIBILITY**: From HCPT documentation: *"State GIS Program projected all county tmk layers to UTM Zone 4, NAD 83 HARN"*

**All downloaded data must be reprojected to this standard for:**
- **Accurate distance calculations** (critical for HAR 11-62 setbacks)
- **Perfect integration** with existing HCPT maps and tools  
- **Consistent spatial analysis** across all data layers

**⚠️ IMPORTANT**: Most downloads will be in WGS84 or other projections and require **Step 0: Reprojection** before analysis.

---

## **📊 PRIORITY 1: REGULATORY COMPLIANCE DATA (HAR 11-62 REQUIRED)**

### **1. Water Wells Database (CWRM) 🚨**
- **Source**: Commission on Water Resource Management (CWRM)
- **URL**: https://dlnr.hawaii.gov/cwrm/
- **HAR 11-62 Reference**: Section 11-62-32, Table II
  - Private wells: 100 ft setback minimum
  - Public wells: 150 ft setback minimum
- **Data Needed**: Point locations, well type (private/public), status (active/inactive)
- **Download Projection**: Unknown (likely various)
- **Folder**: `./_raw/wells/` → `./_standardized/wells/`
- **Status**: [ ] Not Downloaded

---

**🎯 FINAL COUNT: 13 Data Layers** 
- **7 HAR 11-62 Required** (Priority 1)
- **3 Parcel-Level** (Priority 2) 
- **3 Infrastructure Context** (Priority 3)

**✅ HCPT COMPATIBLE**: All data standardized to NAD 83 HARN UTM Zone 4N (EPSG:26904)

**📐 Critical: Use `_standardized/` folders for ALL Matrix analysis to ensure HCPT compatibility and accurate HAR 11-62 setback calculations.**
