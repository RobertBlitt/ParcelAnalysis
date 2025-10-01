# MPAT Step 1: Join Municipal and Domestic Wells Distance Data
# Master Parcel Attribute Table (MPAT) Development
# Run this script in ArcGIS Python window

import arcpy
import os
from datetime import datetime

print("MPAT Step 1: Joining Well Distance Data")
print("=" * 50)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# =============================================================================
# CONFIGURATION - PATHS CONFIGURED FOR ROBERT'S PROJECT STRUCTURE
# =============================================================================

# Project paths (configured for your actual structure)
project_root = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
gdb_path = os.path.join(project_root, "ParcelAnalysis.gdb")
data_folder = os.path.join(project_root, "data", "gis_downloads", "wells", "statewide")

# Set ArcGIS workspace
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# Input shapefiles (from Dr. Shuler's data)
municipal_wells_shp = os.path.join(data_folder, "CPs_Distance_to_Municipal_Wells.shp")
domestic_wells_shp = os.path.join(data_folder, "CPs_Distance_to_Domestic_Wells.shp")

# Output table name for the joined data
output_mpat = "MPAT_Wells_Joined"

print(f"Working in geodatabase: {gdb_path}")
print(f"Municipal wells shapefile: {municipal_wells_shp}")
print(f"Domestic wells shapefile: {domestic_wells_shp}")

# =============================================================================
# STEP 1: IMPORT SHAPEFILES TO GEODATABASE
# =============================================================================

def import_shapefiles():
    """Import the wells shapefiles into the geodatabase"""
    
    print("\nStep 1: Importing shapefiles to geodatabase...")
    
    try:
        # Import municipal wells
        muni_fc = "Municipal_Wells_Distance"
        print(f"Importing municipal wells to {muni_fc}...")
        arcpy.management.CopyFeatures(municipal_wells_shp, muni_fc)
        
        # Import domestic wells  
        domestic_fc = "Domestic_Wells_Distance"
        print(f"Importing domestic wells to {domestic_fc}...")
        arcpy.management.CopyFeatures(domestic_wells_shp, domestic_fc)
        
        # Get record counts
        muni_count = arcpy.management.GetCount(muni_fc)[0]
        domestic_count = arcpy.management.GetCount(domestic_fc)[0]
        
        print(f"✓ Municipal wells imported: {muni_count} records")
        print(f"✓ Domestic wells imported: {domestic_count} records")
        
        return muni_fc, domestic_fc
        
    except Exception as e:
        print(f"ERROR importing shapefiles: {str(e)}")
        return None, None

# =============================================================================
# STEP 2: VERIFY DATA STRUCTURE
# =============================================================================

def verify_data_structure(muni_fc, domestic_fc):
    """Examine the data structure and find TMK fields"""
    
    print("\nStep 2: Verifying data structure...")
    
    try:
        # Check municipal wells fields
        print(f"\n{muni_fc} fields:")
        muni_fields = [f.name for f in arcpy.ListFields(muni_fc)]
        for field in muni_fields:
            print(f"  {field}")
        
        # Check domestic wells fields
        print(f"\n{domestic_fc} fields:")
        domestic_fields = [f.name for f in arcpy.ListFields(domestic_fc)]
        for field in domestic_fields:
            print(f"  {field}")
        
        # Find TMK field (could be TMK, TMK9, TMK_txt)
        tmk_candidates = ['TMK', 'TMK9', 'TMK_txt', 'tmk', 'tmk9']
        muni_tmk = None
        domestic_tmk = None
        
        for candidate in tmk_candidates:
            if candidate in muni_fields:
                muni_tmk = candidate
                break
        
        for candidate in tmk_candidates:
            if candidate in domestic_fields:
                domestic_tmk = candidate
                break
        
        if not muni_tmk or not domestic_tmk:
            print("ERROR: Could not find TMK field in both datasets")
            return False, None, None
        
        print(f"✓ Municipal TMK field: {muni_tmk}")
        print(f"✓ Domestic TMK field: {domestic_tmk}")
        
        # Find distance fields
        muni_distance_fields = [f for f in muni_fields if 'dist' in f.lower() or 'near' in f.lower()]
        domestic_distance_fields = [f for f in domestic_fields if 'dist' in f.lower() or 'near' in f.lower()]
        
        print(f"Municipal distance fields: {muni_distance_fields}")
        print(f"Domestic distance fields: {domestic_distance_fields}")
        
        return True, muni_tmk, domestic_tmk
        
    except Exception as e:
        print(f"ERROR verifying data: {str(e)}")
        return False, None, None

# =============================================================================
# STEP 3: PERFORM THE JOIN
# =============================================================================

def join_wells_data(muni_fc, domestic_fc, muni_tmk, domestic_tmk):
    """Join the wells data on TMK field"""
    
    print("\nStep 3: Joining wells data...")
    
    try:
        # Create the join using JoinField (more reliable for attribute joins)
        print("Performing join operation...")
        
        # Start with municipal wells as base
        arcpy.management.CopyRows(muni_fc, output_mpat)
        
        # Join domestic wells data
        arcpy.management.JoinField(
            in_data=output_mpat,
            in_field=muni_tmk,
            join_table=domestic_fc,
            join_field=domestic_tmk,
            fields=None  # Join all fields
        )
        
        # Verify the result
        result_count = arcpy.management.GetCount(output_mpat)[0]
        result_fields = [f.name for f in arcpy.ListFields(output_mpat)]
        
        print(f"✓ Join completed successfully!")
        print(f"✓ Result records: {result_count}")
        print(f"✓ Result fields: {len(result_fields)}")
        
        # Show field structure
        print("\nJoined table structure:")
        for field in result_fields:
            print(f"  {field}")
        
        return True
        
    except Exception as e:
        print(f"ERROR during join: {str(e)}")
        return False

# =============================================================================
# STEP 4: CLEAN UP FIELD NAMES 
# =============================================================================

def cleanup_field_names():
    """Standardize field names for MPAT"""
    
    print("\nStep 4: Cleaning up field names...")
    
    try:
        # Get current fields
        fields = [f.name for f in arcpy.ListFields(output_mpat)]
        
        # Field renaming mapping (adjust based on actual field names found)
        rename_mapping = {
            # Look for distance fields and standardize names
            'NEAR_DIST': 'Dist_Municipal_Wells_ft',
            'Distance': 'Dist_Municipal_Wells_ft',
            'Muni_Dist': 'Dist_Municipal_Wells_ft',
            'NEAR_DIST_1': 'Dist_Domestic_Wells_ft',
            'Distance_1': 'Dist_Domestic_Wells_ft',
            'Domestic_Dist': 'Dist_Domestic_Wells_ft'
        }
        
        # Apply renames where fields exist
        renamed_count = 0
        for old_name, new_name in rename_mapping.items():
            if old_name in fields:
                try:
                    arcpy.management.AlterField(
                        in_table=output_mpat,
                        field=old_name,
                        new_field_name=new_name,
                        new_field_alias=new_name
                    )
                    print(f"✓ Renamed {old_name} → {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"⚠ Could not rename {old_name}: {e}")
        
        print(f"✓ Renamed {renamed_count} fields")
        return True
        
    except Exception as e:
        print(f"ERROR during cleanup: {str(e)}")
        return False

# =============================================================================
# STEP 5: ADD PROCESSING METADATA
# =============================================================================

def add_metadata():
    """Add processing timestamp and metadata"""
    
    print("\nStep 5: Adding processing metadata...")
    
    try:
        # Add processing date field
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Add field if it doesn't exist
        field_names = [f.name for f in arcpy.ListFields(output_mpat)]
        if "Process_Date" not in field_names:
            arcpy.management.AddField(
                output_mpat, 
                "Process_Date", 
                "TEXT", 
                field_length=20
            )
        
        # Update all records with timestamp
        with arcpy.da.UpdateCursor(output_mpat, ["Process_Date"]) as cursor:
            for row in cursor:
                row[0] = timestamp
                cursor.updateRow(row)
        
        print(f"✓ Added processing timestamp: {timestamp}")
        
        # Final summary
        final_count = arcpy.management.GetCount(output_mpat)[0]
        final_fields = [f.name for f in arcpy.ListFields(output_mpat)]
        
        print(f"\n🎉 MPAT Step 1 COMPLETE!")
        print(f"✓ Output table: {output_mpat}")
        print(f"✓ Records: {final_count}")
        print(f"✓ Fields: {len(final_fields)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR adding metadata: {str(e)}")
        return False

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute the complete wells join workflow"""
    
    try:
        print("Starting MPAT Wells Join Process...")
        
        # Step 1: Import shapefiles
        muni_fc, domestic_fc = import_shapefiles()
        if not muni_fc or not domestic_fc:
            print("\n❌ Import failed!")
            return
        
        # Step 2: Verify data structure
        success, muni_tmk, domestic_tmk = verify_data_structure(muni_fc, domestic_fc)
        if not success:
            print("\n❌ Data verification failed!")
            return
        
        # Step 3: Join the data
        if not join_wells_data(muni_fc, domestic_fc, muni_tmk, domestic_tmk):
            print("\n❌ Join failed!")
            return
        
        # Step 4: Clean up field names
        if not cleanup_field_names():
            print("\n⚠ Field cleanup had issues, continuing...")
        
        # Step 5: Add metadata
        if not add_metadata():
            print("\n⚠ Metadata addition had issues, continuing...")
        
        print(f"\n🎉 SUCCESS: MPAT Step 1 Complete!")
        print(f"   Next: Add slope, soil, and building data to {output_mpat}")
        print(f"   Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    main()

print("\n" + "=" * 50)
print("Script saved and ready to run!")
print("In ArcGIS Python window, run: exec(open(r'C:/Users/rober/OneDrive/Documents/GIS_Projects/ParcelAnalysis/scripts/mpat_development/01_MPAT_Wells_Join.py').read())")
