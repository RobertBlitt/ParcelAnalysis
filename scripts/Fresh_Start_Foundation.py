# Fresh Start - Foundation Setup for Academic Framework
# Hawaii Cesspool Matrix Analysis - Master Parcel Attribute Table (MPAT)
# Run this in ArcGIS Python Window

import arcpy
import os
from datetime import datetime
from pathlib import Path

print("🚀 FRESH START: Academic Framework Foundation Setup")
print("=" * 60)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Project configuration
project_root = Path(r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis")
gdb_path = project_root / "ParcelAnalysis.gdb"
data_folder = project_root / "data" / "gis_downloads" / "wells" / "statewide"
outputs_folder = project_root / "Outputs"
foundation_folder = outputs_folder / "Foundation_Clean"

# Set ArcGIS environment
arcpy.env.workspace = str(gdb_path)
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = "PROJCS['NAD_1983_UTM_Zone_4N']"

print(f"📁 Project: {project_root.name}")
print(f"🗃️ Geodatabase: {gdb_path}")
print(f"📍 Coordinate System: NAD 1983 UTM Zone 4N")
print()

# =============================================================================
# STEP 1: CLEAN SLATE SETUP
# =============================================================================

print("STEP 1: PREPARING CLEAN WORKSPACE")
print("-" * 40)

# Create clean foundation folder
foundation_folder.mkdir(exist_ok=True)
print(f"✅ Clean foundation folder: {foundation_folder}")

# Remove old foundation if it exists in geodatabase
old_foundations = ["TMK_Foundation_Master", "Foundation_Master", "MPAT_Wells_Joined"]
for old_name in old_foundations:
    if arcpy.Exists(old_name):
        arcpy.management.Delete(old_name)
        print(f"🗑️ Removed old foundation: {old_name}")

print("✅ Workspace cleaned for fresh start")
print()

# =============================================================================
# STEP 2: IMPORT WELLS DATA
# =============================================================================

print("STEP 2: IMPORTING WELLS DATA")
print("-" * 40)

# Wells shapefiles
municipal_wells_shp = data_folder / "CPs_Distance_to_Municipal_Wells.shp"
domestic_wells_shp = data_folder / "CPs_Distance_to_Domestic_Wells.shp"

# Check if files exist
if not municipal_wells_shp.exists():
    print(f"❌ Municipal wells not found: {municipal_wells_shp}")
    print("   Download from Dr. Shuler's GIS portal")
    
if not domestic_wells_shp.exists():
    print(f"❌ Domestic wells not found: {domestic_wells_shp}")
    print("   Download from Dr. Shuler's GIS portal")

# Import to geodatabase
municipal_fc = "Municipal_Wells_Import"
domestic_fc = "Domestic_Wells_Import"

if municipal_wells_shp.exists():
    arcpy.management.CopyFeatures(str(municipal_wells_shp), municipal_fc)
    muni_count = int(arcpy.management.GetCount(municipal_fc)[0])
    print(f"✅ Municipal wells imported: {muni_count:,} records")
else:
    print("⚠️ Skipping municipal wells import - file not found")

if domestic_wells_shp.exists():
    arcpy.management.CopyFeatures(str(domestic_wells_shp), domestic_fc)
    domestic_count = int(arcpy.management.GetCount(domestic_fc)[0])
    print(f"✅ Domestic wells imported: {domestic_count:,} records")
else:
    print("⚠️ Skipping domestic wells import - file not found")

print()

# =============================================================================
# STEP 3: CREATE ACADEMIC FRAMEWORK FOUNDATION
# =============================================================================

print("STEP 3: CREATING ACADEMIC FRAMEWORK FOUNDATION")
print("-" * 40)

if arcpy.Exists(municipal_fc):
    # New clean foundation name
    foundation_name = "MPAT_Foundation_v2"
    foundation_path = foundation_folder / f"{foundation_name}.shp"
    
    # Create foundation from municipal wells (has TMK + distance data)
    print("Creating foundation table with academic framework structure...")
    arcpy.management.CopyFeatures(municipal_fc, str(foundation_path))
    
    # Add academic framework fields
    academic_fields = [
        ("JOIN_LOG", "TEXT", 255, "Processing sequence tracking"),
        ("DATA_STATUS", "TEXT", 50, "Data completion status"),
        ("SOIL_CLASS", "TEXT", 20, "HAR 11-62 soil classification"),
        ("SLOPE_PERCENT", "DOUBLE", None, "Average slope percentage"),
        ("SLOPE_CLASS", "TEXT", 15, "Slope suitability class"),
        ("PERC_RATE", "DOUBLE", None, "Soil percolation rate (min/inch)"),
        ("LOT_SIZE_SQFT", "DOUBLE", None, "Lot size in square feet"),
        ("AVAILABLE_AREA", "DOUBLE", None, "Available area for septic"),
        ("SMA_STATUS", "TEXT", 10, "Special Management Area (Y/N)"),
        ("FLOOD_ZONE", "TEXT", 10, "FEMA flood zone designation"),
        ("SSPSCRT", "TEXT", 255, "Site Specific Suitable Technologies"),
        ("LIMITING_FACTORS", "TEXT", 255, "Site constraint documentation"),
        ("MATRIX_READY", "SHORT", None, "Ready for Matrix analysis (1/0)"),
        ("CONFIDENCE", "TEXT", 20, "Data confidence level"),
        ("LAST_UPDATED", "DATE", None, "Last processing date")
    ]
    
    # Add each field
    fields_added = 0
    for field_name, field_type, field_length, field_alias in academic_fields:
        try:
            if field_length:
                arcpy.management.AddField(
                    str(foundation_path), field_name, field_type,
                    field_length=field_length, field_alias=field_alias
                )
            else:
                arcpy.management.AddField(
                    str(foundation_path), field_name, field_type,
                    field_alias=field_alias
                )
            print(f"  ✅ Added: {field_name}")
            fields_added += 1
        except Exception as e:
            print(f"  ⚠️ Could not add {field_name}: {e}")
    
    print(f"✅ Added {fields_added} academic framework fields")
    
    # Initialize tracking
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    with arcpy.da.UpdateCursor(str(foundation_path), ["JOIN_LOG", "DATA_STATUS", "LAST_UPDATED"]) as cursor:
        for row in cursor:
            row[0] = f"Foundation: {timestamp}"
            row[1] = "Municipal wells only"
            row[2] = datetime.now()
            cursor.updateRow(row)
    
    final_count = int(arcpy.management.GetCount(str(foundation_path))[0])
    print(f"✅ Foundation initialized with {final_count:,} records")
    print()
    
    # =============================================================================
    # STEP 4: JOIN DOMESTIC WELLS (IF AVAILABLE)
    # =============================================================================
    
    print("STEP 4: JOINING DOMESTIC WELLS DATA")
    print("-" * 40)
    
    if arcpy.Exists(domestic_fc):
        # Find TMK fields
        foundation_fields = [f.name for f in arcpy.ListFields(str(foundation_path))]
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
            print(f"Joining on: {foundation_tmk} ←→ {domestic_tmk}")
            
            try:
                arcpy.management.JoinField(
                    in_data=str(foundation_path),
                    in_field=foundation_tmk,
                    join_table=domestic_fc,
                    join_field=domestic_tmk
                )
                
                # Update status
                with arcpy.da.UpdateCursor(str(foundation_path), ["JOIN_LOG", "DATA_STATUS"]) as cursor:
                    for row in cursor:
                        row[0] = f"{row[0]}; Domestic wells: {timestamp}"
                        row[1] = "Both wells joined"
                        cursor.updateRow(row)
                
                print("✅ Domestic wells data joined successfully")
                
            except Exception as e:
                print(f"⚠️ Join partially successful: {e}")
        else:
            print(f"⚠️ Could not match TMK fields")
            print(f"   Foundation TMK candidates: {[f for f in foundation_fields if 'TMK' in f.upper()]}")
            print(f"   Domestic TMK candidates: {[f for f in domestic_fields if 'TMK' in f.upper()]}")
    else:
        print("⚠️ Domestic wells not available - skipping join")
    
    print()
    
    # =============================================================================
    # FINAL SUMMARY
    # =============================================================================
    
    print("🎉 FRESH FOUNDATION SETUP COMPLETE!")
    print("=" * 60)
    print(f"📊 Foundation Location: {foundation_path}")
    print(f"📈 Records: {final_count:,}")
    print(f"🏗️ Structure: Academic framework with full field set")
    print(f"⏰ Created: {timestamp}")
    print()
    print("🎯 READY FOR PHASE 2: Geospatial Analysis")
    print("   Next: Add slope analysis, soil classification, regulatory overlays")
    print()
    print("📋 TO USE THIS FOUNDATION:")
    print(f"   1. Add layer to map from: {foundation_path}")
    print(f"   2. Check JOIN_LOG field for processing history")
    print(f"   3. Proceed with Phase 2 notebooks")
    
    # Clean up temporary imports
    for temp_fc in [municipal_fc, domestic_fc]:
        if arcpy.Exists(temp_fc):
            arcpy.management.Delete(temp_fc)
            print(f"🗑️ Cleaned up: {temp_fc}")

else:
    print("❌ Cannot create foundation - municipal wells data not available")
    print("   Please download wells data from Dr. Shuler's GIS portal")

print()
print("=" * 60)
print("Fresh start setup complete!")
