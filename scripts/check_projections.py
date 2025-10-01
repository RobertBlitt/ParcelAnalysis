"""
HAWAII MATRIX PROJECT - SIMPLE PROJECTION CHECKER
Automatically checks and fixes projections for downloaded GIS data

HOW TO USE:
1. Download GIS data to appropriate folders in data/gis_downloads/
2. Double-click this script OR run from command line
3. Script will check all data and fix projections if needed

WHAT IT DOES:
- Scans all shapefiles in gis_downloads folders
- Checks if already in NAD 83 HARN UTM Zone 4N
- If correct: Says "Ready to use"
- If wrong: Automatically reprojects and says "Fixed - now ready"
"""

import arcpy
import os
import sys
from datetime import datetime

def log_message(message, level="INFO"):
    """Print messages with timestamps"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_and_fix_projection(shapefile_path):
    """
    Check if shapefile is in correct projection, fix if needed
    Returns: True if ready to use, False if there was an error
    """
    try:
        file_name = os.path.basename(shapefile_path)
        
        # Check current projection by reading .prj file
        prj_file = shapefile_path.replace('.shp', '.prj')
        
        if not os.path.exists(prj_file):
            log_message(f"❌ {file_name}: No projection file found", "ERROR")
            return False
        
        with open(prj_file, 'r') as f:
            projection_text = f.read()
        
        # Check if already correct
        if "NAD_1983_HARN_UTM_Zone_4N" in projection_text:
            log_message(f"✅ {file_name}: ALREADY CORRECT - Ready for Matrix analysis")
            return True
        
        # Need to reproject
        log_message(f"⚠️  {file_name}: Wrong projection - Fixing now...")
        
        # Determine current projection type for user info
        if "GEOGCS" in projection_text and "PROJCS" not in projection_text:
            current_type = "Geographic coordinates (degrees)"
        elif "State_Plane" in projection_text:
            current_type = "Hawaii State Plane"
        elif "WGS_1984" in projection_text:
            current_type = "WGS84"
        else:
            current_type = "Other projection"
        
        log_message(f"   Current: {current_type}")
        
        # Create backup name and reproject
        backup_name = shapefile_path.replace('.shp', '_original.shp')
        temp_name = shapefile_path.replace('.shp', '_reprojected.shp')
        
        # Target projection: NAD 83 HARN UTM Zone 4N
        target_crs = arcpy.SpatialReference(26904)
        
        # Reproject to temporary file
        arcpy.management.Project(
            in_dataset=shapefile_path,
            out_dataset=temp_name,
            out_coor_system=target_crs
        )
        
        # Replace original with reprojected version
        # First rename original to backup
        arcpy.management.Rename(shapefile_path, backup_name)
        # Then rename reprojected to original name
        arcpy.management.Rename(temp_name, shapefile_path)
        
        log_message(f"✅ {file_name}: FIXED - Reprojected to NAD 83 HARN UTM Zone 4N")
        log_message(f"   Original saved as: {os.path.basename(backup_name)}")
        log_message(f"   Ready for Matrix analysis")
        
        return True
        
    except Exception as e:
        log_message(f"❌ Error processing {file_name}: {str(e)}", "ERROR")
        return False

def scan_gis_folders():
    """
    Scan all GIS download folders and check/fix projections
    """
    # Base folder for GIS downloads
    base_folder = os.path.join(os.path.dirname(__file__), "..", "data", "gis_downloads")
    base_folder = os.path.abspath(base_folder)
    
    if not os.path.exists(base_folder):
        log_message(f"❌ GIS downloads folder not found: {base_folder}", "ERROR")
        log_message("   Make sure you're running this from the project folder", "ERROR")
        input("\nPress Enter to exit...")
        return
    
    log_message("=" * 70)
    log_message("HAWAII MATRIX PROJECT - PROJECTION CHECKER")
    log_message(f"Scanning folder: {base_folder}")
    log_message("=" * 70)
    
    # Find all shapefiles
    shapefiles_found = []
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith('.shp') and not file.endswith('_original.shp'):
                shapefile_path = os.path.join(root, file)
                shapefiles_found.append(shapefile_path)
    
    if not shapefiles_found:
        log_message("No shapefiles found in gis_downloads folders")
        log_message("Download some GIS data first, then run this script again")
        input("\nPress Enter to exit...")
        return
    
    log_message(f"Found {len(shapefiles_found)} shapefile(s) to check")
    log_message("")
    
    # Process each shapefile
    ready_count = 0
    fixed_count = 0
    error_count = 0
    
    for shapefile in shapefiles_found:
        # Show relative path for readability
        rel_path = os.path.relpath(shapefile, base_folder)
        log_message(f"Checking: {rel_path}")
        
        # Check current projection
        prj_file = shapefile.replace('.shp', '.prj')
        try:
            with open(prj_file, 'r') as f:
                projection_text = f.read()
            
            if "NAD_1983_HARN_UTM_Zone_4N" in projection_text:
                log_message(f"✅ ALREADY CORRECT - Ready for Matrix analysis")
                ready_count += 1
            else:
                # Attempt to reproject
                if check_and_fix_projection(shapefile):
                    fixed_count += 1
                else:
                    error_count += 1
        except:
            log_message(f"❌ Could not read projection file")
            error_count += 1
        
        log_message("")  # Empty line for readability
    
    # Summary
    log_message("=" * 70)
    log_message("SUMMARY:")
    log_message(f"✅ Already ready for analysis: {ready_count} files")
    log_message(f"🔧 Fixed and now ready: {fixed_count} files")
    if error_count > 0:
        log_message(f"❌ Errors (need manual check): {error_count} files")
    log_message("")
    log_message("All correctly projected data is ready for Matrix analysis!")
    log_message("=" * 70)

def main():
    """Main function"""
    try:
        # Check if ArcGIS is available
        arcpy.CheckOutExtension("Spatial")
        scan_gis_folders()
        
    except ImportError:
        print("❌ ERROR: ArcGIS/arcpy not available")
        print("   This script requires ArcGIS Pro or ArcMap")
        print("   Make sure you're running from ArcGIS Python environment")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    finally:
        input("\nPress Enter to close...")

if __name__ == "__main__":
    main()
