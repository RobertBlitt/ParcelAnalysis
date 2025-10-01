# CLEAN SLATE START - Hawaii Cesspool Matrix Analysis
# Academic Framework Foundation Setup
# Map: Parcel_Analysis_Statewide (Clean Start)

import arcpy
import os
from datetime import datetime
from pathlib import Path

print("Hawaii Cesspool Matrix Analysis - Clean Start")
print("=" * 70)
print("Academic Framework - University of Hawaii WRRC")
print("Map: Parcel_Analysis_Statewide")
print("Started: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print()

# =============================================================================
# PROJECT CONFIGURATION
# =============================================================================

# Project paths
project_root = Path(r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis")
gdb_path = project_root / "ParcelAnalysis.gdb"
outputs_folder = project_root / "Outputs"
foundation_folder = outputs_folder / "Foundation_Academic"

# Data sources available
wells_folder = project_root / "data" / "gis_downloads" / "wells" / "statewide"
soils_folder = project_root / "data" / "gis_downloads" / "soils" / "Statewide"
tmk_folder = project_root / "data" / "tmk_state.shp"

# ArcGIS environment
arcpy.env.workspace = str(gdb_path)
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_4N']"

print("Project: " + project_root.name)
print("Geodatabase: " + gdb_path.name)
print("Map: Parcel_Analysis_Statewide")
print("Output: Academic MPAT Foundation")
print()

# =============================================================================
# DATA INVENTORY
# =============================================================================

print("DATA INVENTORY CHECK")
print("-" * 40)

# Check available data
data_sources = {
    "Municipal Wells": wells_folder / "CPs_Distance_to_Municipal_Wells.shp",
    "Domestic Wells": wells_folder / "CPs_Distance_to_Domestic_Wells.shp", 
    "NRCS Soils": soils_folder / "HIstate_nrcs_join2" / "HIstate_nrcs_join2.shp",
    "TMK Parcels": tmk_folder / "tmk_state.shp"
}

available_data = {}
for name, path in data_sources.items():
    if path.exists():
        print("Available: " + name + " - " + path.name)
        available_data[name] = path
    else:
        print("Missing: " + name + " - " + str(path))

print("Available datasets: " + str(len(available_data)) + "/4")
print()

# =============================================================================
# STEP 1: CREATE ACADEMIC FRAMEWORK STRUCTURE
# =============================================================================

print("STEP 1: ACADEMIC FRAMEWORK SETUP")
print("-" * 40)

# Create clean foundation folder
foundation_folder.mkdir(exist_ok=True)
print("Foundation folder: " + str(foundation_folder))

# Clean any old foundations
old_foundations = ["MPAT_Foundation", "TMK_Foundation_Master", "Foundation_Academic"]
cleaned = 0
for old_name in old_foundations:
    if arcpy.Exists(old_name):
        arcpy.management.Delete(old_name)
        print("Removed old: " + old_name)
        cleaned += 1

if cleaned == 0:
    print("Geodatabase clean - no old foundations found")

print()

# =============================================================================
# STEP 2: IMPORT AND PROCESS WELLS DATA
# =============================================================================

print("STEP 2: WELLS DISTANCE DATA PROCESSING")
print("-" * 40)

if "Municipal Wells" in available_data and "Domestic Wells" in available_data:
    
    # Import municipal wells as foundation base
    municipal_fc = "Municipal_Wells_Base"
    arcpy.management.CopyFeatures(str(available_data["Municipal Wells"]), municipal_fc)
    muni_count = int(arcpy.management.GetCount(municipal_fc)[0])
    print("Municipal wells imported: " + str(muni_count) + " records")
    
    # Import domestic wells for joining
    domestic_fc = "Domestic_Wells_Join"  
    arcpy.management.CopyFeatures(str(available_data["Domestic Wells"]), domestic_fc)
    domestic_count = int(arcpy.management.GetCount(domestic_fc)[0])
    print("Domestic wells imported: " + str(domestic_count) + " records")
    
    # Create foundation from municipal wells (already has TMK + distances)
    foundation_name = "MPAT_Academic_Foundation"
    foundation_shp = foundation_folder / (foundation_name + ".shp")
    
    print("Creating academic foundation: " + foundation_name)
    arcpy.management.CopyFeatures(municipal_fc, str(foundation_shp))
    
    print("Foundation base created with " + str(muni_count) + " records")
    
else:
    print("ERROR: Cannot proceed - Missing wells distance data")
    print("Required: Municipal and Domestic wells shapefiles")

print()

# =============================================================================
# STEP 3: ADD ACADEMIC FRAMEWORK FIELDS
# =============================================================================

print("STEP 3: ADDING ACADEMIC FRAMEWORK FIELDS")
print("-" * 40)

# Academic MPAT field structure
mpat_fields = [
    # Processing tracking
    ("JOIN_LOG", "TEXT", 255, "Processing sequence log"),
    ("DATA_STATUS", "TEXT", 50, "Data completeness status"), 
    ("CONFIDENCE", "TEXT", 20, "Analysis confidence level"),
    ("LAST_UPDATED", "DATE", None, "Last processing date"),
    
    # Site characteristics for Matrix
    ("SOIL_PERC_RATE", "DOUBLE", None, "Soil percolation rate (min/inch)"),
    ("SOIL_HAR_CLASS", "TEXT", 20, "HAR 11-62 soil classification"),
    ("SLOPE_PERCENT", "DOUBLE", None, "Average slope percentage"),
    ("SLOPE_HAR_CLASS", "TEXT", 15, "HAR 11-62 slope class"),
    ("LOT_SIZE_ACRES", "DOUBLE", None, "Parcel size in acres"),
    ("AVAILABLE_AREA", "DOUBLE", None, "Available septic area (sq ft)"),
    ("BEDROOMS_COUNT", "SHORT", None, "Number of bedrooms"),
    ("ESTIMATED_FLOW", "DOUBLE", None, "Daily wastewater flow (gallons)"),
    
    # Regulatory constraints
    ("SMA_STATUS", "TEXT", 5, "Special Management Area (Y/N)"),
    ("FLOOD_ZONE", "TEXT", 10, "FEMA flood zone"),
    ("GROUNDWATER_DEPTH", "DOUBLE", None, "Depth to groundwater (feet)"),
    ("WELLS_1000FT", "TEXT", 5, "Within 1000ft of wells (Y/N)"),
    ("SHORE_50FT", "TEXT", 5, "Within 50ft of shore (Y/N)"),
    ("WATER_50FT", "TEXT", 5, "Within 50ft of surface water (Y/N)"),
    
    # Matrix results
    ("MATRIX_PROCESSED", "SHORT", None, "Matrix analysis complete (1/0)"),
    ("SSPSCRT", "TEXT", 255, "Site Specific Suitable Technologies"),
    ("LIMITING_FACTORS", "TEXT", 255, "Site constraints documentation"),
    ("RECOMMENDED_TECH", "TEXT", 100, "Primary recommended technology"),
    ("ALTERNATIVE_TECH", "TEXT", 100, "Alternative technology options"),
    ("IMPLEMENTATION", "TEXT", 50, "Implementation complexity level")
]

# Add each field to foundation
fields_added = 0
print("Adding MPAT fields:")
for field_name, field_type, field_length, field_alias in mpat_fields:
    try:
        if field_length:
            arcpy.management.AddField(
                str(foundation_shp), field_name, field_type,
                field_length=field_length, field_alias=field_alias
            )
        else:
            arcpy.management.AddField(
                str(foundation_shp), field_name, field_type,
                field_alias=field_alias
            )
        print("  Added: " + field_name)
        fields_added += 1
    except Exception as e:
        print("  Issue with " + field_name + ": " + str(e))

print("Added " + str(fields_added) + "/" + str(len(mpat_fields)) + " MPAT fields")
print()

# =============================================================================
# STEP 4: JOIN DOMESTIC WELLS DATA
# =============================================================================

print("STEP 4: JOINING DOMESTIC WELLS DISTANCE")
print("-" * 40)

# Find TMK fields for joining
foundation_fields = [f.name for f in arcpy.ListFields(str(foundation_shp))]
domestic_fields = [f.name for f in arcpy.ListFields(domestic_fc)]

# Find matching TMK field
tmk_candidates = ['TMK', 'TMK9', 'TMK_txt']
foundation_tmk = None
domestic_tmk = None

for candidate in tmk_candidates:
    if candidate in foundation_fields and not foundation_tmk:
        foundation_tmk = candidate
    if candidate in domestic_fields and not domestic_tmk:
        domestic_tmk = candidate

if foundation_tmk and domestic_tmk:
    print("Joining on TMK fields: " + foundation_tmk + " and " + domestic_tmk)
    
    try:
        arcpy.management.JoinField(
            in_data=str(foundation_shp),
            in_field=foundation_tmk,
            join_table=domestic_fc,
            join_field=domestic_tmk
        )
        print("Domestic wells data joined successfully")
        wells_status = "Both wells joined"
        
    except Exception as e:
        print("Join issue: " + str(e))
        wells_status = "Municipal only"
else:
    print("Could not match TMK fields")
    wells_status = "Municipal only"

print()

# =============================================================================
# STEP 5: INITIALIZE ACADEMIC TRACKING
# =============================================================================

print("STEP 5: INITIALIZING ACADEMIC TRACKING")
print("-" * 40)

# Initialize processing tracking
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
init_log = "Academic Foundation: " + timestamp + "; Wells: " + wells_status

update_count = 0
with arcpy.da.UpdateCursor(str(foundation_shp), 
                          ["JOIN_LOG", "DATA_STATUS", "CONFIDENCE", "LAST_UPDATED"]) as cursor:
    for row in cursor:
        row[0] = init_log
        row[1] = wells_status  
        row[2] = "High"  # Wells data is high confidence
        row[3] = datetime.now()
        cursor.updateRow(row)
        update_count += 1

print("Initialized tracking for " + str(update_count) + " records")
print("Join log: " + init_log)
print()

# =============================================================================
# STEP 6: ADD TO MAP AND FINAL SUMMARY  
# =============================================================================

print("STEP 6: ADDING TO PARCEL_ANALYSIS_STATEWIDE MAP")
print("-" * 40)

# Add foundation to current map
try:
    # Get current map
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map_obj = aprx.activeMap
    
    # Add foundation layer
    foundation_layer = map_obj.addDataFromPath(str(foundation_shp))
    print("Added " + foundation_name + " to " + map_obj.name)
        
except Exception as e:
    print("Could not auto-add to map: " + str(e))
    print("Manually add: " + str(foundation_shp))

print()

# Clean up temporary feature classes
for temp_fc in [municipal_fc, domestic_fc]:
    if arcpy.Exists(temp_fc):
        arcpy.management.Delete(temp_fc)

# =============================================================================
# ACADEMIC FOUNDATION COMPLETE
# =============================================================================

final_count = int(arcpy.management.GetCount(str(foundation_shp))[0])
final_fields = [f.name for f in arcpy.ListFields(str(foundation_shp))]

print("ACADEMIC FOUNDATION SETUP COMPLETE!")
print("=" * 70)
print("Foundation: " + foundation_shp.name)
print("Records: " + str(final_count) + " TMK parcels statewide")
print("Structure: " + str(len(final_fields)) + " fields (academic framework)")
print("Created: " + timestamp)
print("Location: " + str(foundation_shp))
print()
print("READY FOR PHASE 2: GEOSPATIAL ANALYSIS")
print("Next steps:")
print("  - Slope analysis from DEM")
print("  - Soil classification (NRCS data available)")
print("  - Regulatory overlays (SMA, flood zones)")
print("  - Building characteristics integration")
print()
print("FOUNDATION CONTENTS:")
print("  TMK identifiers for all Hawaii parcels")
print("  Municipal wells distances (HAR 11-62: 1000ft setback)")
print("  Domestic wells distances (HAR 11-62: 1000ft setback)")
print("  Academic tracking fields (JOIN_LOG, confidence, etc.)")
print("  Matrix analysis fields (SSPSCRT, limiting factors)")
print("  Soil, slope, regulatory data (Phase 2)")
print()
print("PHASE 1 COMPLETE - Data Preparation Foundation Ready")
print("=" * 70)
