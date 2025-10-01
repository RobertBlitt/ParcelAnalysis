    # Seepage pits have stricter percolation requirements
    if perc_class != '1-10 min/inch':
        compatible = False
        if perc_class == '<1 min/inch':
            limiting_factors.append('Percolation too fast for seepage pits')
        elif perc_class in ['>60 min/inch', '10-60 min/inch']:
            limiting_factors.append('Percolation too slow for seepage pits')
        else:
            limiting_factors.append('Unknown percolation rate')
    
    # Good drainage required
    if drainage_class not in ['Good', 'Moderate']:
        compatible = False
        if drainage_class == 'Poor':
            limiting_factors.append('Poor drainage')
        else:
            limiting_factors.append('Unknown drainage')
    
    return compatible, limiting_factors

# ============================================================================
# COMPREHENSIVE PROCESSING FUNCTIONS
# ============================================================================

def process_soil_har_classifications(input_layer, output_layer):
    """
    Complete HAR 11-62 soil processing workflow
    
    Args:
        input_layer (str): Input soil layer name
        output_layer (str): Output processed layer name
        
    Returns:
        str: Path to processed layer
    """
    print(f"Processing soil data for HAR 11-62 compliance...")
    
    # Create working copy
    arcpy.management.CopyFeatures(input_layer, output_layer)
    
    # Add HAR classification fields
    har_fields = [
        ("HAR_SLOPE_CLASS", "TEXT", 15),
        ("HAR_PERC_CLASS", "TEXT", 20), 
        ("HAR_DRAINAGE_CLASS", "TEXT", 20),
        ("PERC_RATE_EST", "DOUBLE", None),
        ("MATRIX_SEPTIC_OK", "SHORT", None),
        ("MATRIX_ATU_OK", "SHORT", None),
        ("MATRIX_SEEPAGE_PIT_OK", "SHORT", None),
        ("LIMITING_FACTORS", "TEXT", 200)
    ]
    
    for field_name, field_type, field_length in har_fields:
        try:
            if field_length:
                arcpy.management.AddField(output_layer, field_name, field_type, field_length=field_length)
            else:
                arcpy.management.AddField(output_layer, field_name, field_type)
        except:
            pass  # Field may already exist
    
    # Process records
    process_fields = [
        'slope_r', 'ksat_r', 'drainagecl',
        'HAR_SLOPE_CLASS', 'HAR_PERC_CLASS', 'HAR_DRAINAGE_CLASS',
        'PERC_RATE_EST', 'MATRIX_SEPTIC_OK', 'MATRIX_ATU_OK', 
        'MATRIX_SEEPAGE_PIT_OK', 'LIMITING_FACTORS'
    ]
    
    processed_count = 0
    with arcpy.da.UpdateCursor(output_layer, process_fields) as cursor:
        for row in cursor:
            slope_r, ksat_r, drainagecl = row[0], row[1], row[2]
            
            # Classify slope
            slope_class = classify_slope_har(slope_r)
            row[3] = slope_class
            
            # Convert Ksat and classify percolation
            perc_rate = ksat_to_percolation_rate(ksat_r)
            row[6] = perc_rate
            perc_class = classify_percolation_har(perc_rate)
            row[4] = perc_class
            
            # Classify drainage
            drainage_class = classify_drainage_har(drainagecl)
            row[5] = drainage_class
            
            # Check technology compatibility
            septic_ok, septic_limits = check_septic_compatibility(slope_class, perc_class, drainage_class)
            atu_ok, atu_limits = check_atu_compatibility(slope_class, perc_class, drainage_class)
            seepage_ok, seepage_limits = check_seepage_pit_compatibility(slope_class, perc_class, drainage_class)
            
            row[7] = 1 if septic_ok else 0
            row[8] = 1 if atu_ok else 0
            row[9] = 1 if seepage_ok else 0
            
            # Combine all limiting factors
            all_limits = list(set(septic_limits + atu_limits + seepage_limits))
            row[10] = '; '.join(all_limits) if all_limits else 'Suitable'
            
            cursor.updateRow(row)
            processed_count += 1
            
            if processed_count % 1000 == 0:
                print(f"Processed {processed_count} records...")
    
    print(f"HAR 11-62 processing complete: {processed_count} records")
    return output_layer

def calculate_disposal_area_requirements(num_bedrooms, perc_rate, soil_type='standard'):
    """
    Calculate minimum disposal area per HAR 11-62 requirements
    
    Args:
        num_bedrooms (int): Number of bedrooms
        perc_rate (float): Percolation rate in minutes per inch
        soil_type (str): Soil type classification
        
    Returns:
        dict: Disposal area requirements for different system types
    """
    if not num_bedrooms or num_bedrooms <= 0:
        return None
    
    base_flow = num_bedrooms * DESIGN_FLOW_RATES['GALLONS_PER_BEDROOM_PER_DAY']
    
    # Disposal area factors based on percolation rate
    # (These are approximate - actual HAR 11-62 Appendix D Table III should be used)
    area_factors = {
        '<1 min/inch': 70,      # Very fast - needs larger area
        '1-10 min/inch': 85,    # Good percolation
        '10-60 min/inch': 125,  # Slower percolation - needs more area
        '>60 min/inch': None    # Too slow - not suitable
    }
    
    perc_class = classify_percolation_har(perc_rate)
    area_factor = area_factors.get(perc_class)
    
    if area_factor is None:
        return None
    
    disposal_area_sqft = (base_flow / 100) * area_factor  # Simplified calculation
    
    return {
        'bedrooms': num_bedrooms,
        'design_flow_gpd': base_flow,
        'percolation_class': perc_class,
        'disposal_area_sqft': round(disposal_area_sqft, 0),
        'area_factor': area_factor
    }

def validate_har_compliance(layer_path):
    """
    Validate a layer for HAR 11-62 compliance
    
    Args:
        layer_path (str): Path to layer to validate
        
    Returns:
        dict: Validation results
    """
    validation_results = {
        'valid_records': 0,
        'invalid_records': 0,
        'field_completeness': {},
        'classification_validity': {},
        'compliance_summary': {}
    }
    
    required_fields = ['HAR_SLOPE_CLASS', 'HAR_PERC_CLASS', 'HAR_DRAINAGE_CLASS']
    
    # Check field existence
    existing_fields = [f.name for f in arcpy.ListFields(layer_path)]
    missing_fields = [f for f in required_fields if f not in existing_fields]
    
    if missing_fields:
        validation_results['missing_fields'] = missing_fields
        return validation_results
    
    # Validate classifications
    total_records = 0
    with arcpy.da.SearchCursor(layer_path, required_fields) as cursor:
        for row in cursor:
            total_records += 1
            slope_class, perc_class, drainage_class = row
            
            valid_record = (
                slope_class in VALID_CLASSIFICATIONS['SLOPE_CLASSES'] and
                perc_class in VALID_CLASSIFICATIONS['PERCOLATION_CLASSES'] and
                drainage_class in VALID_CLASSIFICATIONS['DRAINAGE_CLASSES']
            )
            
            if valid_record:
                validation_results['valid_records'] += 1
            else:
                validation_results['invalid_records'] += 1
    
    # Calculate validation percentages
    if total_records > 0:
        validation_results['validity_percentage'] = (validation_results['valid_records'] / total_records) * 100
    
    return validation_results

# ============================================================================
# REGULATORY REFERENCE INFORMATION
# ============================================================================

HAR_11_62_REFERENCES = {
    'TITLE': 'Hawaii Administrative Rules, Title 11, Chapter 62 - Wastewater Systems',
    'SECTIONS': {
        '11-62-31': 'Individual wastewater systems - General requirements',
        '11-62-31.1': 'Cesspool prohibition',
        '11-62-31.2': 'Site evaluation requirements', 
        '11-62-32': 'Individual wastewater systems - Location and setback requirements',
        '11-62-33': 'Individual wastewater systems - Design requirements',
        '11-62-34': 'Individual wastewater systems - Construction requirements'
    },
    'KEY_TABLES': {
        'Table II': 'Minimum setback distances (HAR 11-62-32)',
        'Appendix D Table III': 'Disposal area requirements by soil percolation rate'
    },
    'LAST_UPDATED': '2014-07-01',
    'AUTHORITY': 'Hawaii Department of Health - Wastewater Branch'
}

def print_har_reference_info():
    """Print HAR 11-62 reference information"""
    print(f"\n{HAR_11_62_REFERENCES['TITLE']}")
    print("=" * len(HAR_11_62_REFERENCES['TITLE']))
    print(f"Authority: {HAR_11_62_REFERENCES['AUTHORITY']}")
    print(f"Last Updated: {HAR_11_62_REFERENCES['LAST_UPDATED']}")
    
    print(f"\nKey Sections:")
    for section, description in HAR_11_62_REFERENCES['SECTIONS'].items():
        print(f"  {section}: {description}")
    
    print(f"\nImportant Tables:")
    for table, description in HAR_11_62_REFERENCES['KEY_TABLES'].items():
        print(f"  {table}: {description}")

# Export key constants for easy access
__all__ = [
    'SLOPE_THRESHOLDS', 'PERCOLATION_LIMITS', 'SETBACK_DISTANCES',
    'DESIGN_FLOW_RATES', 'VALID_CLASSIFICATIONS', 'DRAINAGE_CLASSIFICATION_MAP',
    'ksat_to_percolation_rate', 'classify_slope_har', 'classify_percolation_har',
    'classify_drainage_har', 'check_septic_compatibility', 'check_atu_compatibility',
    'check_seepage_pit_compatibility', 'process_soil_har_classifications',
    'calculate_disposal_area_requirements', 'validate_har_compliance',
    'print_har_reference_info', 'HAR_11_62_REFERENCES'
]
