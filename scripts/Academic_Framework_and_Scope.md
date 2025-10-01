# Hawaii Cesspool Matrix Analysis - Academic Framework and Scope

**Revised Academic Structure with Extracted Key Concepts**

## **SCOPE CLARIFICATION**

### **✅ Confirmed: Individual Property Owner Focus**
Based on HCPT documentation and HAR 11-62 regulations:

**Target Audience:** Individual residential property owners  
**Regulatory Framework:** HAR 11-62 Subchapter 3 (Individual Wastewater Systems) ONLY  
**Scale:** Single-family residential dwellings and agricultural parcels with dwellings

### **🚨 APARTMENT TMK ALERT IDENTIFIED**
**PITT Codes show apartment classifications exist:**
- **Hawaii County:** Code 2 = Apartment (Value = 200)
- **Maui County:** Code 2 = Apartment (Value = 200)

**ACTION REQUIRED:** Verify if HCPT included apartment TMKs in cesspool inventory. If yes, need to determine:
- Are these small residential-scale apartments (2-4 units) under HAR 11-62?
- Or larger complexes requiring different regulatory treatment?

### **Regulatory Boundaries - STRICT FOCUS**
**INCLUDED (HAR 11-62 Subchapter 3):**
- Individual wastewater systems for single-family residences
- Septic tanks, aerobic treatment units, seepage pits
- Systems serving ≤5 bedrooms (per IWS application form)
- CPR units with individual systems

**EXCLUDED:**
- Municipal wastewater treatment (different regulations)
- Large-scale systems (hotels, resorts, large apartments)
- Commercial/industrial wastewater treatment
- Any system not covered by HAR 11-62 Subchapter 3

## **TRANSFERABLE METHODOLOGY FRAMEWORK**

### **Core Methodological Essence**

You've identified a **universally applicable three-stage analytical framework**:

#### **Stage 1: Characteristics Compilation**
**"Find and compute and compile the relevant characteristics of study units"**
- **Study Units:** Can be parcels, buildings, watersheds, municipalities, etc.
- **Characteristics:** Any measurable attributes relevant to the inquiry (slope, soil, proximity, demographics, etc.)
- **Spatial Scale:** Adaptable from parcel to regional level

#### **Stage 2: Suitability Matrix Analysis**  
**"Run through a sieve matrix of suitability"**
- **Constraints Matrix:** Binary compatibility assessment
- **Threshold-Based:** Each characteristic has defined suitability thresholds
- **Multi-Criteria:** Combines multiple limiting factors simultaneously

#### **Stage 3: Solution Matching**
**"Produce tailored recommendations that fit each unit"**
- **Site-Specific:** Recommendations customized to individual unit characteristics
- **Multiple Options:** Where feasible, provide ranked alternatives
- **Implementation-Ready:** Results formatted for decision-making

### **Professional Planning Terminology**

This methodology aligns with established planning and environmental engineering approaches:

**Environmental Site Assessment:** Systematic evaluation of site constraints and opportunities  
**Multi-Criteria Decision Analysis (MCDA):** Structured approach to complex decisions involving multiple factors  
**Suitability Analysis:** Geographic method for determining optimal locations based on criteria  
**Constraint Mapping:** Identification and spatial representation of limiting factors

### **Key Distinction from HCPT**

**HCPT Approach:** **Comparative Risk Assessment**
- **Question:** "Which cesspools pose higher environmental/health risks relative to each other?"
- **Scale:** Regional prioritization (census tract level)
- **Output:** Risk rankings for resource allocation
- **Analogy:** "Which parks need funding priority based on use and location?"

**Matrix Approach:** **Site-Specific Feasibility Assessment**  
- **Question:** "Which solutions will work at this specific location?"
- **Scale:** Individual parcel analysis
- **Output:** Technology recommendations per property
- **Analogy:** "What playground equipment will fit in this specific park space?"

## **ACADEMIC WORKFLOW STRUCTURE**

### **1. Data Preparation**
**Purpose:** Standardize and validate input data layers  
**HAR 11-62 Focus:** Ensure all data processing supports IWS regulatory requirements  
**Key Concepts from Food-Metaphor:** Sequential processing with JOIN_LOG tracking

### **2. Geospatial Analysis**  
**Purpose:** Calculate site characteristics for Matrix input  
**HAR 11-62 Focus:** Distance calculations (1000ft wells), slope thresholds (8%, 12%), soil percolation rates  
**Key Concepts:** Modular processing, swappable data sources, QA at each step

### **3. Data Validation**
**Purpose:** Verify accuracy before Matrix processing  
**HAR 11-62 Focus:** Regulatory compliance verification  
**Key Concepts:** Join success monitoring, completeness assessment

### **4. Data Assembly and Processing**
**Purpose:** Create MPAT and execute Matrix analysis  
**Matrix Processing:** Binary suitability assessment per parcel  
**Output:** SSPSCRT (Site Specific Potentially Suitable Cesspool Replacement Technologies)  
**Critical Check:** Verify ATU feasibility assumption (should work for ~95% of parcels)

### **5. Results Refinement**
**Purpose:** Format for property owner interface  
**User Experience:** Address-based lookup with clear explanations  
**Output Format:** 
- Site Limiting Factors: [specific constraints]
- Recommended Technologies: [ranked options with brief rationale]

### **6. Documentation and Deployment**
**Purpose:** Academic documentation and public deployment  
**Transferability:** Document methodology for replication in other contexts  
**Integration:** Connect with existing HCPT web tools

## **CRITICAL VALIDATION NOTES**

### **ATU Default Assumption**
**Hypothesis:** Advanced Treatment Units work for ~95% of residential parcels  
**Edge Cases to Verify:**
- Slopes >30% (may require pumped systems)
- Groundwater <2 feet (installation challenges)  
- Lots <0.1 acres (space constraints)
- Extreme setback situations (1000ft from wells)

**Validation Method:** Cross-reference Matrix results against known ATU installations

### **Apartment TMK Investigation Required**
**Immediate Action:** Check HCPT methodology for apartment inclusion criteria  
**Decision Point:** If apartments included, determine appropriate regulatory framework  
**Potential Solution:** Separate analysis track for multi-unit residential (if HAR 11-62 applicable)

## **TRANSFERABILITY APPLICATIONS**

This methodology framework can be adapted for:
- **Renewable Energy Siting:** Solar/wind feasibility by parcel
- **Agricultural Planning:** Crop suitability assessment  
- **Flood Mitigation:** Property-level resilience strategies
- **Historic Preservation:** Development compatibility analysis
- **Public Health:** Facility location optimization

The core principle remains: **systematic site characterization → constraint analysis → tailored solution matching**

---

**Next Steps:**
1. Verify apartment TMK treatment in HCPT
2. Organize existing useful code into new academic structure  
3. Begin Data Preparation phase with HAR 11-62 compliance focus
4. Implement JOIN_LOG tracking system for reproducibility
