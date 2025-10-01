# The Matrix - Parcel-Level Technology Screening Tool
# Component of the Hawaii Cesspool Prioritization Tool (HCPT) Ecosystem

## **Project Positioning and Context**

### **The Matrix Role in HCPT Framework:**
The Matrix is a **parcel-level technology screening tool** that complements the broader Hawaii Cesspool Prioritization Tool (HCPT) ecosystem. While HCPT operates at census tract/block group level for statewide screening and the Infrastructure Overlay identifies areas suitable for sewer expansion, The Matrix provides **individual property-level analysis** for technology selection.

### **HCPT Ecosystem Components:**
1. **HCPT Core Tool**: Statewide cesspool risk screening (census tract level)
2. **Infrastructure Feasibility Overlay**: Identifies areas suitable for sewer expansion  
3. **The Matrix** (this project): Parcel-level technology suitability screening
4. **Spatial Resolution Addendum**: Standards for consistent spatial analysis

### **The Matrix Specific Purpose:**
- **Individual property assessment** for cesspools that will require onsite solutions
- **Technology matching** between site characteristics and DOH-approved IWS options
- **Site suitability analysis** based on HAR 11-62 Subchapter 3 requirements
- **Decision support** for property owners, engineers, and regulators

## **Technical Scope and Approach**

### **Target Properties:**
- Residential parcels with cesspools requiring conversion by 2050
- Properties in areas where sewer expansion is NOT feasible (per Infrastructure Overlay)
- Properties where owners need technology selection guidance

### **Analysis Framework:**
```
Parcel Characteristics → Site Constraints → Technology Options → Recommendations
        ↓                        ↓                    ↓               ↓
• Lot size/shape        • HAR 11-62 setbacks    • Conventional     • Primary choice
• Soil conditions       • Slope limitations      • Aerobic units    • Alternative
• Groundwater depth     • Flood zones           • Passive systems   • Cost estimates
• Existing development  • SMA/Critical habitat  • Composting       • Permits needed
```

### **DOH-Approved Technologies Evaluated:**
1. **Conventional Septic Systems** (IAPMO ANSI Z1000-2013)
2. **Aerobic Treatment Units** (NSF Standard No. 40)
3. **Passive Aerobic Systems** (Eljen, Presby)
4. **Bioreactor Gardens** (Ridge to Reefs)
5. **Composting Toilets** (toilet waste only)
6. **Incinerator Toilets** (toilet waste only)

### **Regulatory Compliance:**
- **HAR 11-62 Subchapter 3** requirements only
- **Setback calculations** (wells, shoreline, buildings)
- **Lot size minimums** (10,000 SF per IWS)
- **Soil percolation standards** (1-60 min/inch)
- **Professional pathway** (licensed engineer → DOH → licensed contractor)

## **Integration with HCPT Ecosystem**

### **Data Inputs from HCPT:**
- Parcel locations and TMK identifiers
- Cesspool inventory and verification status
- Priority classifications for context
- Environmental constraint layers

### **Coordination with Infrastructure Overlay:**
- Excludes parcels in sewer expansion areas
- Focuses on properties requiring onsite solutions
- Provides technology guidance where sewer is not feasible

### **Outputs for HCPT System:**
- Parcel-level technology recommendations
- Cost estimates for individual solutions
- Implementation complexity assessments
- Permit pathway guidance

## **Implementation Strategy**

### **Phase 1: Core Tool Development**
- Parcel characterization engine
- HAR 11-62 compliance checking
- Technology matching algorithms
- Basic cost estimation

### **Phase 2: Integration and Validation**
- HCPT data integration
- Infrastructure Overlay coordination
- DOH approval workflow integration
- Pilot testing with sample parcels

### **Phase 3: Deployment and Maintenance**
- Public web interface
- Professional tools for engineers
- Regular updates and calibration
- Training and support materials

## **Success Metrics**

### **Technical Performance:**
- Accurate technology recommendations for >90% of parcels
- Regulatory compliance verification
- Cost estimates within ±20% of actual
- Processing time <2 minutes per parcel

### **Ecosystem Integration:**
- Seamless data flow with HCPT components
- Consistent spatial standards compliance
- No duplication with Infrastructure Overlay
- Clear referral pathways between tools

### **User Adoption:**
- Property owner decision support
- Engineer workflow integration  
- DOH regulatory process streamlining
- County planning tool utilization

---

**The Matrix serves as the "last mile" tool in the HCPT ecosystem, providing the detailed, parcel-specific guidance needed when centralized solutions are not viable and individual onsite systems are the only path to 2050 compliance.**
