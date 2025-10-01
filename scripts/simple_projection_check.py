"""
Hawaii Matrix Project - Simple Projection Checker Script
Run this directly in ArcGIS Pro Python window

HOW TO USE:
1. Open ArcGIS Pro
2. Open Python window (View > Python)
3. Copy and paste this entire script
4. Press Enter twice to run
"""

import arcpy
import os

def check_projections():
    """Check and fix projections for Hawaii Matrix project"""
    
    print("=" * 50)
    print("HAWAII MATRIX PROJECT - PROJECTION CHECKER")
    print("=" * 50)
    
    try:
        # Get project folder
        project = arcpy.mp.ArcGISProject("CURRENT")
        project_folder = project.homeFolder
        data_folder = os.path.join(project_folder, "data", "gis_downloads")
        
        if not os.path.exists(data_folder):
            print(f"ERROR: Could not find data folder: {data_folder}")
            return
        
        print(f"Scanning: {data_folder}")
        
        # Target projection: NAD 83 HARN UTM Zone 4N
        target_crs = arcpy.SpatialReference(26904)
        
        # Find shapefiles
        shapefiles = []
        for root, dirs, files in os.walk(data_folder):
            for file in files:
                if file.endswith('.shp') and not file.endswith('_original.shp'):
                    shapefiles.append(os.path.join(root, file))
        
        if not shapefiles:
            print("No shapefiles found")
            return
        
        print(f"Found {len(shapefiles)} shapefiles")
        print()
        
        # Check each file
        ready_count = 0
        fixed_count = 0
        
        for shapefile in shapefiles:
            try:
                file_name = os.path.basename(shapefile)
                print(f"Checking: {file_name}")
                
                desc = arcpy.Describe(shapefile)
                current_crs = desc.spatialReference
                
                if current_crs.factoryCode == 26904:
                    print("  -> Already correct (NAD 83 HARN UTM Zone 4N)")
                    ready_count += 1
                else:
                    print(f"  -> Wrong projection: {current_crs.name}")
                    print("  -> Reprojecting...")
                    
                    # Create backup
                    backup_name = shapefile.replace('.shp', '_original.shp')
                    if not os.path.exists(backup_name):
                        arcpy.management.Copy(shapefile, backup_name)
                        print("  -> Backup created")
                    
                    # Reproject to temporary file
                    temp_name = shapefile.replace('.shp', '_temp.shp')
                    arcpy.management.Project(shapefile, temp_name, target_crs)
                    
                    # Replace original with reprojected
                    arcpy.management.Delete(shapefile)
                    arcpy.management.Rename(temp_name, shapefile)
                    
                    print("  -> Reprojected to NAD 83 HARN UTM Zone 4N")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"  -> ERROR: {str(e)}")
            
            print()
        
        # Summary
        print("=" * 50)
        print("SUMMARY:")
        print(f"Already ready: {ready_count} files")
        print(f"Fixed: {fixed_count} files")
        print("All data now ready for Matrix analysis!")
        print("=" * 50)
        
    except Exception as e:
        print(f"Script failed: {str(e)}")

# Run the function
if __name__ == "__main__":
    check_projections()
