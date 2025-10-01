# UPDATED Project Inventory - IWS Focus
# Revised based on HAR 11-62 Subchapter 3 scope and DOH research

## **🎯 CLARIFIED PROJECT SCOPE**

### **WHAT WE'RE ANALYZING:**
- ✅ **Individual Wastewater Systems (IWS)** only
- ✅ **Residential parcels** with cesspools needing conversion
- ✅ **DOH-approved technologies** for replacement
- ✅ **HAR 11-62 Subchapter 3** requirements only

### **WHAT WE'RE NOT ANALYZING:**
- ❌ Large municipal wastewater treatment works
- ❌ Industrial/commercial wastewater systems  
- ❌ Properties already on centralized sewer
- ❌ Large-scale wastewater management

---

## **✅ CONFIRMED PROJECT ASSETS**

### **Spatial Data**
- ✅ **TMK Statewide Parcels** (`data/tmk_state.shp`) - HAVE
- ✅ **DWELDAT Residential Data** (`scripts/dweldat25_cleaned.csv`) - HAVE  
- ✅ **Bedroom/Bathroom Summary** (`scripts/TMK_Bedrooms.csv`) - HAVE

### **Project Infrastructure**
- ✅ **Enhanced Directory Structure** - COMPLETE
- ✅ **Configuration System** (`hawaii_iws_config.yaml`) - COMPLETE
- ✅ **Documentation Framework** - COMPLETE
- ✅ **DOH Resource Inventory** - COMPLETE

---

## **🚨 CRITICAL DATA NEEDS (Start Immediately)**

### **1. DOH Priority Area Boundaries** 🎯
- **Source**: DOH 2022 Cesspool Hazard Assessment & Prioritization Tool
- **Contact**: DOH Wastewater Branch (808) 586-4400
- **Why Critical**: Align our analysis with official DOH priorities
- **Format**: GIS boundaries for Priority 1-4 areas
- **Status**: **NEED TO REQUEST**

### **2. Existing Cesspool Locations** 📍
- **Source**: DOH Cesspool Registration Cards
- **Contact**: DOH Wastewater Branch
- **Why Critical**: Identify conversion candidates
- **Format**: Point locations with TMK references
- **Status**: **NEED TO REQUEST**

### **3. Current IWS Database** 🗄️
- **Source**: DOH Wastewater Branch IWS records
- **Why Critical**: Exclude parcels with compliant systems
- **Format**: Database with TMK, system type, approval status
- **Status**: **NEED TO REQUEST**

### **4. Sewer Service Area Boundaries** 🚰
- **Source**: Individual county utilities
- **Why Critical**: Exclude parcels already on sewer
- **Counties**: Hawaii, Maui, Honolulu, Kauai
- **Status**: **NEED TO REQUEST FROM EACH COUNTY**

---

## **🔍 ENVIRONMENTAL DATA (Still Required)**

### **Water Well Locations** 💧
- **Source**: CWRM Well Database
- **URL**: https://dlnr.hawaii.gov/cwrm/groundwater/well-data/
- **Why**: HAR 11-62 setback requirements (100 ft private, 150 ft public)
- **Status**: **READY TO DOWNLOAD**

### **Soil Survey Data** 🌱
- **Source**: NRCS Web Soil Survey
- **URL**: https://websoilsurvey.sc.egov.usda.gov/
- **Why**: Percolation rates for IWS technology selection
- **Status**: **READY TO DOWNLOAD**

### **Digital Elevation Model** 🏔️
- **Source**: USGS 3DEP
- **URL**: https://elevation.nationalmap.gov/
- **Why**: Slope analysis for site suitability
- **Status**: **READY TO DOWNLOAD**

---

## **📋 DOH DATA REQUEST STRATEGY**

### **Contact Information:**
- **DOH Wastewater Branch**: (808) 586-4400
- **Email**: wastewater@doh.hawaii.gov
- **Main Office**: 2827 Waimano Home Road, Ste 207, Pearl City, HI 96782

### **Information to Request:**

#### **Email Template for DOH:**
```
Subject: Research Request - Cesspool Conversion Analysis Data

Dear DOH Wastewater Branch,

I am conducting academic research on cesspool conversion planning in Hawaii, 
aligned with Act 125 requirements and HAR 11-62 Subchapter 3 regulations. 

Could you please provide access to the following data layers for research purposes:

1. DOH Priority Area boundaries (from 2022 Hazard Assessment)
2. Cesspool registration card locations (anonymized if needed)
3. Current IWS database (system types and approval status)
4. Any GIS layers related to wastewater system classification

This research aims to support systematic conversion planning and technology 
selection for Hawaii's 2050 cesspool conversion mandate.

Research Contact: [Your Name and Institution]
Phone: [Your Phone]
Email: [Your Email]

Thank you for your assistance with this important public health research.
```

---

## **🏛️ COUNTY DATA REQUESTS**

### **Sewer Service Areas** (Critical for excluding parcels)

#### **Hawaii County:**
- **Contact**: Department of Environmental Management
- **Phone**: (808) 961-8681
- **Website**: https://www.dem.hawaiicounty.gov/

#### **Maui County:**
- **Contact**: Environmental Management Division  
- **Phone**: (808) 270-7285
- **Website**: https://www.mauicounty.gov/

#### **City & County of Honolulu:**
- **Contact**: Department of Environmental Services
- **Phone**: (808) 768-3486
- **Website**: https://www.honolulu.gov/env

#### **Kauai County:**
- **Contact**: Department of Public Works
- **Phone**: (808) 241-4787
- **Website**: https://www.kauai.gov/

---

## **📊 REVISED ANALYSIS FRAMEWORK**

### **Phase 1: IWS Candidate Identification**
1. **Start with all residential parcels** (from DWELDAT)
2. **Exclude parcels on sewer** (county service areas)
3. **Exclude parcels with compliant IWS** (DOH database)
4. **Identify cesspool locations** (DOH registration cards)
5. **Result**: Definitive list of conversion candidates

### **Phase 2: Technology Suitability Analysis**
1. **Apply HAR 11-62 Subchapter 3 requirements**
2. **Evaluate for DOH-approved technologies only**
3. **Consider site constraints** (soil, slope, setbacks)
4. **Integrate DOH priority area classifications**
5. **Result**: Technology recommendations per parcel

### **Phase 3: Implementation Guidance**
1. **Professional pathway** (licensed engineer → DOH → licensed contractor)
2. **Financing options** (tax credits, USDA, CWSRF)
3. **Priority sequencing** (align with DOH priorities)
4. **Economic analysis** (costs, incentives, ROI)

---

## **🎯 IMMEDIATE ACTION PLAN (This Week)**

### **Day 1: DOH Data Request**
- ✅ Send email to DOH Wastewater Branch requesting priority areas, cesspool locations, IWS database
- ✅ Call main office to follow up and clarify data availability

### **Day 2: County Sewer Data**
- ✅ Contact all 4 counties requesting sewer service area boundaries
- ✅ Explain cesspool conversion research purpose

### **Day 3-4: Environmental Data**
- ✅ Download water well data from CWRM
- ✅ Download soil survey data from NRCS
- ✅ Download elevation data from USGS

### **Day 5-7: Data Integration Setup**
- ✅ Set up data standardization procedures
- ✅ Create initial quality control framework
- ✅ Prepare for data integration workflow

---

## **📈 SUCCESS METRICS (Week 1)**

### **Critical Data Acquired:**
- ✅ DOH priority area boundaries received
- ✅ Cesspool location data received  
- ✅ County sewer service areas received
- ✅ Water well locations downloaded
- ✅ Soil and elevation data downloaded

### **Analysis Ready:**
- ✅ Conversion candidate identification possible
- ✅ Technology suitability analysis framework ready
- ✅ Regulatory compliance checking enabled
- ✅ Priority area integration prepared

**The focused IWS scope dramatically simplifies our data requirements while ensuring we address Hawaii's actual cesspool conversion needs!**
