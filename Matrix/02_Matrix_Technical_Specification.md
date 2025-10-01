# The Matrix - Technical Specification
# Parcel-Level Technology Screening for Individual Wastewater Systems

## **System Architecture**

### **Input Data Requirements:**
1. **Parcel Data**
   - TMK identifier and boundaries
   - Lot size and shape
   - Existing building footprints
   - Current system type (cesspool verification)

2. **Site Characteristics**
   - Soil survey data (NRCS + Hawaii DOH standards)
   - Groundwater depth (statewide models)
   - Slope analysis (10m DEM)
   - Flood zone designation

3. **Regulatory Overlays**
   - Well locations (private and public)
   - Surface water bodies
   - Special Management Areas
   - Critical habitat boundaries

4. **Infrastructure Context**
   - Sewer service availability (from Infrastructure Overlay)
   - Distance to existing utilities
   - Road access classification

### **Core Analysis Engine:**

#### **Step 1: Site Constraint Assessment**
```python
def assess_site_constraints(parcel_id):
    constraints = {
        'lot_size_compliant': check_minimum_lot_size(parcel_id),
        'setback_clearances': calculate_all_setbacks(parcel_id),
        'slope_limitations': analyze_slope_constraints(parcel_id),
        'soil_suitability': evaluate_percolation_rates(parcel_id),
        'groundwater_separation': check_vertical_separation(parcel_id),
        'flood_restrictions': assess_flood_zone_impacts(parcel_id),
        'regulatory_overlays': check_sma_habitat_constraints(parcel_id)
    }
    return constraints
```

#### **Step 2: Technology Matching Algorithm**
```python
def match_technologies(site_constraints):
    suitable_technologies = []
    
    # Conventional Septic System
    if (site_constraints['lot_size_sf'] >= 10000 and
        site_constraints['setback_clearances']['all_met'] and
        site_constraints['soil_perc_rate'] in range(1, 61) and
        site_constraints['groundwater_depth_ft'] >= 3):
        suitable_technologies.append({
            'technology': 'conventional_septic',
            'confidence': 'high',
            'estimated_cost': calculate_septic_cost(site_constraints)
        })
    
    # Aerobic Treatment Unit
    if (site_constraints['lot_size_sf'] >= 7500 and
        site_constraints['setback_clearances']['reduced_ok'] and
        site_constraints['soil_perc_rate'] in range(1, 61)):
        suitable_technologies.append({
            'technology': 'aerobic_treatment_unit',
            'confidence': 'high',
            'estimated_cost': calculate_atu_cost(site_constraints)
        })
    
    # Continue for all DOH-approved technologies...
    return suitable_technologies
```

#### **Step 3: Recommendation Ranking**
```python
def rank_recommendations(suitable_technologies, site_preferences):
    scored_options = []
    
    for tech in suitable_technologies:
        score = {
            'cost_factor': calculate_cost_score(tech['estimated_cost']),
            'maintenance_complexity': get_maintenance_score(tech['technology']),
            'regulatory_certainty': get_approval_likelihood(tech['technology']),
            'long_term_reliability': get_reliability_score(tech['technology'])
        }
        
        tech['composite_score'] = weighted_average(score)
        scored_options.append(tech)
    
    return sorted(scored_options, key=lambda x: x['composite_score'], reverse=True)
```

## **HAR 11-62 Subchapter 3 Compliance Engine**

### **Setback Requirements (HAR 11-62-32, Table II):**
```python
def calculate_setbacks(parcel_data):
    setbacks = {
        'private_wells': 100,      # feet
        'public_wells': 150,       # feet  
        'shoreline': 50,           # feet
        'surface_water': 50,       # feet
        'buildings': 10,           # feet
        'property_lines': 5,       # feet
        'swimming_pools': 10       # feet
    }
    
    # Calculate available area after setbacks
    available_area = apply_setback_buffers(parcel_data, setbacks)
    return available_area, setbacks
```

### **System Sizing (HAR 11-62-33.1):**
```python
def calculate_system_size(bedrooms):
    daily_flow = bedrooms * 200  # gallons per bedroom per day
    
    if bedrooms <= 4:
        septic_size = 1000  # gallons
    elif bedrooms == 5:
        septic_size = 1250  # gallons
    else:
        # Formula: 1000 + (Q-800) * 1.25
        septic_size = 1000 + (daily_flow - 800) * 1.25
    
    return {
        'daily_flow_gpd': daily_flow,
        'septic_tank_size_gal': int(septic_size),
        'disposal_area_sf': calculate_disposal_area(daily_flow)
    }
```

### **Soil Standards (Hawaii DOH Percolation Rates):**
```python
def evaluate_soil_suitability(soil_data):
    # Convert NRCS soil data to Hawaii DOH percolation standards
    perc_rate = convert_to_doh_standards(soil_data)
    
    if 1 <= perc_rate <= 60:  # minutes per inch
        return {
            'suitable': True,
            'percolation_rate': perc_rate,
            'treatment_level': determine_treatment_level(perc_rate)
        }
    else:
        return {
            'suitable': False,
            'issue': 'percolation_rate_out_of_range',
            'alternative_needed': True
        }
```

## **Technology Database Structure**

### **Conventional Septic System:**
```yaml
conventional_septic:
  name: "Conventional Septic System"
  doh_approval: "IAPMO ANSI Z1000-2013"
  treatment_level: "Primary"
  
  site_requirements:
    min_lot_size_sf: 10000
    setback_compliance: "full"
    soil_perc_range: [1, 60]
    groundwater_separation_ft: 3
    max_slope_percent: 15
  
  costs:
    base_cost: 20000
    size_multiplier: 1.2  # per additional bedroom
    site_difficulty_factor: [1.0, 2.0]  # easy to difficult
  
  maintenance:
    pumping_frequency_years: 3
    inspection_frequency_years: 1
    expected_lifespan_years: 25
```

### **Aerobic Treatment Unit:**
```yaml
aerobic_treatment_unit:
  name: "Aerobic Treatment Unit (ATU)"
  doh_approval: "NSF Standard No. 40"
  treatment_level: "Secondary"
  
  site_requirements:
    min_lot_size_sf: 7500
    setback_compliance: "reduced"
    soil_perc_range: [1, 60]
    groundwater_separation_ft: 2
    max_slope_percent: 20
    electrical_required: true
  
  costs:
    base_cost: 25000
    annual_maintenance: 800
    service_contract_required: true
  
  maintenance:
    inspection_frequency_months: 6
    service_contract_cost_annual: 800
    expected_lifespan_years: 20
```

## **Output Specifications**

### **Parcel Assessment Report:**
```json
{
  "parcel_id": "TMK123456789",
  "assessment_date": "2025-09-17",
  "site_analysis": {
    "lot_size_sf": 12000,
    "available_area_sf": 8500,
    "slope_max_percent": 8,
    "soil_percolation_rate": 25,
    "groundwater_depth_ft": 6,
    "constraints": ["close_to_well", "moderate_slope"]
  },
  "suitable_technologies": [
    {
      "technology": "conventional_septic",
      "rank": 1,
      "confidence": "high",
      "estimated_cost": 22000,
      "permit_complexity": "standard",
      "maintenance_cost_annual": 300
    },
    {
      "technology": "aerobic_treatment_unit", 
      "rank": 2,
      "confidence": "high",
      "estimated_cost": 28000,
      "permit_complexity": "standard",
      "maintenance_cost_annual": 800
    }
  ],
  "regulatory_pathway": {
    "engineer_required": true,
    "doh_permit_needed": true,
    "county_permit_needed": true,
    "estimated_timeline_months": 6
  },
  "recommendations": {
    "primary_choice": "conventional_septic",
    "rationale": "Most cost-effective option with lowest maintenance burden",
    "next_steps": ["hire_licensed_engineer", "soil_percolation_test", "design_development"]
  }
}
```

---

**This technical specification provides the detailed framework for implementing The Matrix as a robust, HAR 11-62 compliant, parcel-level technology screening tool within the HCPT ecosystem.**
