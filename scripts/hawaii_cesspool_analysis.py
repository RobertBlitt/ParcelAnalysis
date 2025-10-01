# Hawaii Statewide Cesspool Prioritization Analysis
# Complete ArcPy Workflow for Cesspool Replacement Planning
# Based on Hawaii Administrative Rule 11-62 Requirements

import arcpy
import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys
from datetime import datetime

print("HAWAII STATEWIDE CESSPOOL PRIORITIZATION ANALYSIS")
print("=" * 60)
print(f"Analysis started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Based on Hawaii Administrative Rule 11-62")
print("")

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

class Config:
    """Configuration settings for the cesspool analysis"""
    
    def __init__(self):
        # File paths - ADJUST THESE TO MATCH YOUR SETUP
        self.project_folder = r"C:\Users\YourName\Documents\GIS_Projects\ParcelAnalysis"
        self.gdb_path = os.path.join(self.project_folder, "ParcelAnalysis.gdb")
        self.data_folder = os.path.join(self.project_folder, "data")
        self.output_folder = os.path.join(self.project_folder, "outputs")
        
        # Input data names
        self.tmk_fc = "tmk_state"  # Your statewide TMK feature class
        self.bedroom_csv = "bedrooms_out.csv"  # Your bedroom count data
        
        # Output feature class names
        self.parcels_with_bedrooms = "Parcels_With_Bedrooms"
        self.residential_parcels = "Residential_Parcels"
        self.cesspool_analysis = "Cesspool_Analysis_Final"
        
        # Hawaii Rule 11-62 Constants
        self.GALLONS_PER_BEDROOM_PER_DAY = 200
        self.GALLONS_PER_BATHROOM_PER_DAY = 50  # For agricultural facilities
        self.MIN_SEPTIC_TANK_SIZE = 1000
        
        # Analysis parameters
        self.min_lot_size_acres = 0.1  # Minimum lot size for individual systems
        self.max_bedrooms = 20  # Exclude large hotels/condos
        self.min_bedrooms_residential = 1

def setup_workspace(config):
    """Initialize workspace and verify file paths"""
    print("🔧 SETTING UP WORKSPACE")
    print("-" * 30)
    
    # Set workspace
    arcpy.env.workspace = config.gdb_path
    arcpy.env.overwriteOutput = True
    
    # Create output folder if it doesn't exist
    os.makedirs(config.output_folder, exist_ok=True)
    
    # Verify input files exist
    tmk_path = os.path.join(config.gdb_path, config.tmk_fc)
    bedroom_path = os.path.join(config.data_folder, config.bedroom_csv)
    
    if not arcpy.Exists(tmk_path):
        raise FileNotFoundError(f"TMK feature class not found: {tmk_path}")
    if not os.path.exists(bedroom_path):
        raise FileNotFoundError(f"Bedroom CSV not found: {bedroom_path}")
        
    print(f"✅ Workspace: {config.gdb_path}")
    print(f"✅ TMK Feature Class: {config.tmk_fc}")
    print(f"✅ Bedroom Data: {config.bedroom_csv}")
    print("")

# =============================================================================
# PHASE 1: DATA PREPARATION AND JOINING
# =============================================================================

def load_and_examine_data(config):
    """Load and examine the TMK and bedroom data"""
    print("📊 PHASE 1: DATA LOADING AND EXAMINATION")
    print("-" * 45)
    
    # Get TMK feature class info
    tmk_count = int(arcpy.GetCount_management(config.tmk_fc)[0])
    tmk_fields = [field.name for field in arcpy.ListFields(config.tmk_fc)]
    
    print(f"TMK Parcels: {tmk_count:,} features")
    print(f"TMK Fields: {tmk_fields[:10]}...")  # Show first 10 fields
    
    # Load bedroom CSV data
    bedroom_path = os.path.join(config.data_folder, config.bedroom_csv)
    bedroom_df = pd.read_csv(bedroom_path)
    
    print(f"Bedroom Data: {len(bedroom_df):,} records")
    print(f"Bedroom Fields: {list(bedroom_df.columns)}")
    print("")
    
    # Show sample of bedroom data
    print("Sample bedroom data:")
    print(bedroom_df.head())
    print("")
    
    return bedroom_df

def join_bedroom_data_to_parcels(config, bedroom_df):
    """Join bedroom count data to TMK parcels"""
    print("🔗 JOINING BEDROOM DATA TO PARCELS")
    print("-" * 35)
    
    try:
        # Create temporary table from bedroom CSV
        temp_table = "bedroom_temp"
        bedroom_path = os.path.join(config.data_folder, config.bedroom_csv)
        
        print(f"Creating temporary table from {config.bedroom_csv}...")
        arcpy.TableToTable_conversion(bedroom_path, config.gdb_path, temp_table)
        
        # Join bedroom data to TMK parcels
        print(f"Joining bedroom data to {config.tmk_fc}...")
        arcpy.JoinField_management(
            in_data=config.tmk_fc,
            in_field="TMK",  # Adjust field name if different
            join_table=temp_table,
            join_field="TMK",
            fields=["BED_ROOMS"]  # Adjust field name if different
        )
        
        # Copy to new feature class
        print(f"Creating {config.parcels_with_bedrooms}...")
        arcpy.CopyFeatures_management(config.tmk_fc, config.parcels_with_bedrooms)
        
        # Get count of parcels with bedroom data
        joined_count = int(arcpy.GetCount_management(config.parcels_with_bedrooms)[0])
        print(f"✅ Created {config.parcels_with_bedrooms}: {joined_count:,} parcels")
        
        # Clean up
        arcpy.Delete_management(temp_table)
        print("")
        
    except Exception as e:
        print(f"❌ Error joining data: {str(e)}")
        print("Trying alternative join method...")
        
        # Alternative method using pandas and field calculation
        join_bedroom_data_alternative(config, bedroom_df)

def join_bedroom_data_alternative(config, bedroom_df):
    """Alternative method to join bedroom data using field calculation"""
    print("Using alternative join method...")
    
    # Copy TMK to new feature class
    arcpy.CopyFeatures_management(config.tmk_fc, config.parcels_with_bedrooms)
    
    # Add bedroom field
    arcpy.AddField_management(config.parcels_with_bedrooms, "BED_ROOMS", "SHORT")
    
    # Create TMK to bedroom lookup dictionary
    bedroom_dict = dict(zip(bedroom_df['TMK'], bedroom_df['BED_ROOMS']))
    
    # Update bedroom values using cursor
    print("Updating bedroom values...")
    with arcpy.da.UpdateCursor(config.parcels_with_bedrooms, ['TMK', 'BED_ROOMS']) as cursor:
        for row in cursor:
            tmk = row[0]
            if tmk in bedroom_dict:
                row[1] = bedroom_dict[tmk]
                cursor.updateRow(row)
    
    print("✅ Alternative join method completed")
    print("")

# =============================================================================
# PHASE 2: RESIDENTIAL PARCEL FILTERING
# =============================================================================

def filter_residential_parcels(config):
    """Filter parcels for residential properties likely to need cesspool replacement"""
    print("🏠 PHASE 2: FILTERING RESIDENTIAL PARCELS")
    print("-" * 42)
    
    # Create SQL query for residential parcels
    # Adjust field names based on your actual schema
    where_clause = f"""
        BED_ROOMS >= {config.min_bedrooms_residential} AND 
        BED_ROOMS <= {config.max_bedrooms} AND 
        (ACRES >= {config.min_lot_size_acres} OR ACRES IS NULL)
    """
    
    print("Filtering criteria:")
    print(f"  • Bedrooms: {config.min_bedrooms_residential} to {config.max_bedrooms}")
    print(f"  • Lot size: >= {config.min_lot_size_acres} acres")
    print("")
    
    try:
        # Create feature layer with selection
        temp_layer = "residential_layer"
        arcpy.MakeFeatureLayer_management(config.parcels_with_bedrooms, temp_layer, where_clause)
        
        # Copy selected features to new feature class
        arcpy.CopyFeatures_management(temp_layer, config.residential_parcels)
        
        # Get count of residential parcels
        residential_count = int(arcpy.GetCount_management(config.residential_parcels)[0])
        original_count = int(arcpy.GetCount_management(config.parcels_with_bedrooms)[0])
        
        print(f"✅ Filtered {original_count:,} parcels to {residential_count:,} residential parcels")
        print(f"   Reduction: {original_count - residential_count:,} parcels removed")
        print("")
        
        # Clean up
        arcpy.Delete_management(temp_layer)
        
    except Exception as e:
        print(f"❌ Error filtering parcels: {str(e)}")
        print("Check your field names and try adjusting the where_clause")

# =============================================================================
# PHASE 3: CESSPOOL ANALYSIS CALCULATIONS
# =============================================================================

def calculate_cesspool_requirements(config):
    """Calculate wastewater flow and septic tank requirements per Hawaii Rule 11-62"""
    print("⚙️ PHASE 3: CALCULATING CESSPOOL REQUIREMENTS")
    print("-" * 47)
    
    # Copy residential parcels to analysis feature class
    arcpy.CopyFeatures_management(config.residential_parcels, config.cesspool_analysis)
    
    # Add new fields for analysis
    new_fields = [
        ("DAILY_FLOW_GAL", "LONG", "Daily wastewater flow (gallons)"),
        ("SEPTIC_SIZE_GAL", "LONG", "Required septic tank size (gallons)"),
        ("LOT_SIZE_SF", "LONG", "Lot size (square feet)"),
        ("LOT_SIZE_CAT", "TEXT", "Lot size category"),
        ("CESSPOOL_REPLACEMENT", "TEXT", "Needs cesspool replacement"),
        ("PRIORITY_SCORE", "SHORT", "Priority score (1-10)")
    ]
    
    print("Adding analysis fields...")
    for field_name, field_type, description in new_fields:
        arcpy.AddField_management(config.cesspool_analysis, field_name, field_type)
        print(f"  ✅ {field_name}: {description}")
    
    print("")
    
    # Calculate values using field calculator and cursor
    calculate_wastewater_flows(config)
    calculate_septic_tank_sizes(config)
    calculate_lot_characteristics(config)
    calculate_priority_scores(config)

def calculate_wastewater_flows(config):
    """Calculate daily wastewater flow per Hawaii Rule 11-62"""
    print("Calculating daily wastewater flows...")
    
    # Use field calculator for basic calculation
    expression = f"!BED_ROOMS! * {config.GALLONS_PER_BEDROOM_PER_DAY}"
    arcpy.CalculateField_management(
        config.cesspool_analysis, 
        "DAILY_FLOW_GAL", 
        expression, 
        "PYTHON3"
    )
    print("  ✅ Daily flows calculated (200 gal/bedroom/day)")

def calculate_septic_tank_sizes(config):
    """Calculate required septic tank sizes per Hawaii Rule 11-62"""
    print("Calculating septic tank size requirements...")
    
    # Use cursor for complex calculation
    with arcpy.da.UpdateCursor(config.cesspool_analysis, 
                              ['BED_ROOMS', 'DAILY_FLOW_GAL', 'SEPTIC_SIZE_GAL']) as cursor:
        for row in cursor:
            bedrooms = row[0] if row[0] else 0
            daily_flow = row[1] if row[1] else 0
            
            # Apply Hawaii Rule 11-62 septic tank sizing
            if bedrooms <= 4:
                septic_size = 1000  # Minimum 1000 gallons
            elif bedrooms == 5:
                septic_size = 1250  # 1250 gallons for 5 bedrooms
            else:
                # Formula: 1000 + (Q-800) × 1.25 where Q = design flow
                septic_size = 1000 + (daily_flow - 800) * 1.25
            
            row[2] = int(septic_size)
            cursor.updateRow(row)
    
    print("  ✅ Septic tank sizes calculated per HR 11-62")

def calculate_lot_characteristics(config):
    """Calculate lot size characteristics for technology matching"""
    print("Calculating lot size characteristics...")
    
    # Calculate lot size in square feet
    arcpy.CalculateField_management(
        config.cesspool_analysis,
        "LOT_SIZE_SF",
        "!ACRES! * 43560 if !ACRES! else 0",
        "PYTHON3"
    )
    
    # Categorize lot sizes for technology suitability
    lot_size_expression = """
def categorize_lot_size(lot_sf):
    if lot_sf < 10000:
        return '<10k sf'
    elif lot_sf <= 21000:
        return '10k-21k sf'
    else:
        return '>21k sf'

categorize_lot_size(!LOT_SIZE_SF!)
"""
    
    arcpy.CalculateField_management(
        config.cesspool_analysis,
        "LOT_SIZE_CAT",
        lot_size_expression,
        "PYTHON3"
    )
    
    # Mark all as needing cesspool replacement
    arcpy.CalculateField_management(
        config.cesspool_analysis,
        "CESSPOOL_REPLACEMENT",
        "'YES'",
        "PYTHON3"
    )
    
    print("  ✅ Lot characteristics calculated")

def calculate_priority_scores(config):
    """Calculate preliminary priority scores"""
    print("Calculating priority scores...")
    
    # Simple priority scoring based on bedrooms and lot size
    # Higher bedrooms = higher priority (more wastewater)
    # Smaller lots = higher priority (more challenging to upgrade)
    
    priority_expression = """
def calculate_priority(bedrooms, lot_sf):
    score = 5  # Base score
    
    # Bedroom factor (more bedrooms = higher priority)
    if bedrooms >= 6:
        score += 3
    elif bedrooms >= 4:
        score += 2
    elif bedrooms >= 2:
        score += 1
    
    # Lot size factor (smaller lots = higher priority)
    if lot_sf < 10000:
        score += 2
    elif lot_sf <= 21000:
        score += 1
    
    return min(score, 10)  # Cap at 10

calculate_priority(!BED_ROOMS! if !BED_ROOMS! else 1, !LOT_SIZE_SF!)
"""
    
    arcpy.CalculateField_management(
        config.cesspool_analysis,
        "PRIORITY_SCORE",
        priority_expression,
        "PYTHON3"
    )
    
    print("  ✅ Priority scores calculated")
    print("")

# =============================================================================
# PHASE 4: SPATIAL ANALYSIS AND ENVIRONMENTAL FACTORS
# =============================================================================

def add_environmental_factors(config):
    """Add environmental factors for technology suitability analysis"""
    print("🌍 PHASE 4: ADDING ENVIRONMENTAL FACTORS")
    print("-" * 42)
    
    print("Note: This section will be expanded when spatial data is available")
    print("Future additions will include:")
    print("  • Slope analysis from DEM")
    print("  • Groundwater depth")
    print("  • Soil permeability")
    print("  • Distance to shoreline")
    print("  • Distance to streams")
    print("  • Flood zone designation")
    print("")
    
    # Add placeholder fields for future environmental analysis
    env_fields = [
        ("SLOPE_PERCENT", "DOUBLE", "Slope percentage"),
        ("GROUNDWATER_FT", "DOUBLE", "Depth to groundwater (feet)"),
        ("SOIL_PERM", "TEXT", "Soil permeability category"),
        ("SHORE_DIST_FT", "LONG", "Distance to shoreline (feet)"),
        ("STREAM_DIST_FT", "LONG", "Distance to streams (feet)"),
        ("FLOOD_ZONE", "TEXT", "FEMA flood zone designation")
    ]
    
    print("Adding environmental analysis fields...")
    for field_name, field_type, description in env_fields:
        arcpy.AddField_management(config.cesspool_analysis, field_name, field_type)
        print(f"  ✅ {field_name}: {description}")
    
    print("")

# =============================================================================
# PHASE 5: REPORTING AND ANALYSIS SUMMARY
# =============================================================================

def generate_analysis_summary(config):
    """Generate summary statistics and analysis report"""
    print("📈 PHASE 5: ANALYSIS SUMMARY AND REPORTING")
    print("-" * 45)
    
    # Get summary statistics
    total_parcels = int(arcpy.GetCount_management(config.cesspool_analysis)[0])
    
    # Calculate statistics by island and priority
    print(f"Total parcels analyzed: {total_parcels:,}")
    
    # Create summary by county/island
    summarize_by_island(config)
    
    # Create summary by bedroom count
    summarize_by_bedrooms(config)
    
    # Create summary by priority score
    summarize_by_priority(config)
    
    # Export to CSV for additional analysis
    export_to_csv(config)

def summarize_by_island(config):
    """Create summary statistics by island"""
    print("\nSummary by Island:")
    print("-" * 20)
    
    # Use frequency analysis to get counts by island
    # Note: Adjust field name based on your TMK structure
    freq_table = "island_summary"
    
    try:
        # Create frequency table (assuming first digit of TMK indicates island)
        arcpy.AddField_management(config.cesspool_analysis, "ISLAND", "TEXT")
        
        # Calculate island from TMK (first digit: 1=Hawaii, 2=Maui, 3=Honolulu, 4=Kauai)
        island_expression = """
def get_island(tmk):
    if tmk:
        first_digit = str(tmk)[0]
        if first_digit == '1':
            return 'Hawaii'
        elif first_digit == '2':
            return 'Maui'
        elif first_digit == '3':
            return 'Honolulu'
        elif first_digit == '4':
            return 'Kauai'
    return 'Unknown'

get_island(!TMK!)
"""
        
        arcpy.CalculateField_management(
            config.cesspool_analysis,
            "ISLAND",
            island_expression,
            "PYTHON3"
        )
        
        # Get counts by island
        with arcpy.da.SearchCursor(config.cesspool_analysis, ['ISLAND']) as cursor:
            island_counts = {}
            for row in cursor:
                island = row[0]
                island_counts[island] = island_counts.get(island, 0) + 1
        
        for island, count in sorted(island_counts.items()):
            print(f"  {island}: {count:,} parcels")
            
    except Exception as e:
        print(f"  ⚠️ Could not calculate island summary: {str(e)}")

def summarize_by_bedrooms(config):
    """Create summary by bedroom count"""
    print("\nSummary by Bedrooms:")
    print("-" * 22)
    
    try:
        with arcpy.da.SearchCursor(config.cesspool_analysis, ['BED_ROOMS']) as cursor:
            bedroom_counts = {}
            for row in cursor:
                bedrooms = row[0] if row[0] else 0
                bedroom_counts[bedrooms] = bedroom_counts.get(bedrooms, 0) + 1
        
        for bedrooms in sorted(bedroom_counts.keys())[:10]:  # Show top 10
            count = bedroom_counts[bedrooms]
            print(f"  {bedrooms} bedrooms: {count:,} parcels")
            
    except Exception as e:
        print(f"  ⚠️ Could not calculate bedroom summary: {str(e)}")

def summarize_by_priority(config):
    """Create summary by priority score"""
    print("\nSummary by Priority Score:")
    print("-" * 28)
    
    try:
        with arcpy.da.SearchCursor(config.cesspool_analysis, ['PRIORITY_SCORE']) as cursor:
            priority_counts = {}
            total_flow = 0
            count = 0
            
            for row in cursor:
                priority = row[0] if row[0] else 5
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                count += 1
        
        for priority in sorted(priority_counts.keys(), reverse=True):
            count = priority_counts[priority]
            print(f"  Priority {priority}: {count:,} parcels")
            
    except Exception as e:
        print(f"  ⚠️ Could not calculate priority summary: {str(e)}")

def export_to_csv(config):
    """Export results to CSV for further analysis"""
    print(f"\nExporting results to CSV...")
    
    try:
        # Export to CSV
        output_csv = os.path.join(config.output_folder, "Hawaii_Cesspool_Analysis_Results.csv")
        
        # Get field names
        field_names = [field.name for field in arcpy.ListFields(config.cesspool_analysis) 
                      if field.name not in ['OBJECTID', 'Shape', 'Shape_Length', 'Shape_Area']]
        
        # Export using pandas for better control
        data = []
        with arcpy.da.SearchCursor(config.cesspool_analysis, field_names) as cursor:
            for row in cursor:
                data.append(row)
        
        df = pd.DataFrame(data, columns=field_names)
        df.to_csv(output_csv, index=False)
        
        print(f"  ✅ Results exported: {output_csv}")
        print(f"  📊 Records: {len(df):,}")
        print(f"  📋 Fields: {len(field_names)}")
        
    except Exception as e:
        print(f"  ⚠️ Could not export CSV: {str(e)}")

# =============================================================================
# MAIN EXECUTION FUNCTION
# =============================================================================

def main():
    """Main execution function"""
    try:
        # Initialize configuration
        config = Config()
        
        # Setup workspace
        setup_workspace(config)
        
        # Phase 1: Data Loading and Examination
        bedroom_df = load_and_examine_data(config)
        join_bedroom_data_to_parcels(config, bedroom_df)
        
        # Phase 2: Residential Filtering
        filter_residential_parcels(config)
        
        # Phase 3: Cesspool Analysis
        calculate_cesspool_requirements(config)
        
        # Phase 4: Environmental Factors (placeholder)
        add_environmental_factors(config)
        
        # Phase 5: Summary and Reporting
        generate_analysis_summary(config)
        
        # Final success message
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 60)
        print(f"✅ Final output: {config.cesspool_analysis}")
        print(f"✅ Results exported to: {config.output_folder}")
        print("")
        print("NEXT STEPS:")
        print("1. Review the analysis results in ArcGIS Pro")
        print("2. Add environmental spatial data when available")
        print("3. Apply technology suitability matrix")
        print("4. Create priority maps by island")
        print("5. Generate cost estimates and implementation timeline")
        print("")
        print("This analysis provides the foundation for comprehensive")
        print("cesspool replacement planning across Hawaii.")
        
    except Exception as e:
        print(f"❌ ANALYSIS FAILED: {str(e)}")
        print("Check your file paths and data structure")
        import traceback
        traceback.print_exc()

# =============================================================================
# UTILITY FUNCTIONS FOR FUTURE ENHANCEMENTS
# =============================================================================

def add_slope_analysis(config, dem_raster):
    """Add slope analysis from DEM (for future use)"""
    print("Adding slope analysis from DEM...")
    
    # Calculate slope
    slope_raster = os.path.join(config.gdb_path, "slope_raster")
    arcpy.Slope_3d(dem_raster, slope_raster, "PERCENT_RISE")
    
    # Extract slope values to points
    arcpy.sa.ExtractValuesToPoints(
        config.cesspool_analysis,
        slope_raster,
        "parcels_with_slope"
    )

def add_groundwater_analysis(config, groundwater_layer):
    """Add groundwater depth analysis (for future use)"""
    print("Adding groundwater depth analysis...")
    
    # Spatial join or near analysis to get groundwater depths
    arcpy.SpatialJoin_analysis(
        config.cesspool_analysis,
        groundwater_layer,
        "parcels_with_groundwater"
    )

def apply_technology_matrix(config, technology_matrix_csv):
    """Apply technology suitability matrix (for future use)"""
    print("Applying technology suitability matrix...")
    
    # Load technology matrix
    tech_df = pd.read_csv(technology_matrix_csv)
    
    # Apply suitability rules based on parcel characteristics
    # This will be a complex matching algorithm based on:
    # - Lot size category
    # - Slope percentage  
    # - Groundwater depth
    # - Soil type
    # - Distance to sensitive areas

# =============================================================================
# RUN THE ANALYSIS
# =============================================================================

if __name__ == "__main__":
    main()