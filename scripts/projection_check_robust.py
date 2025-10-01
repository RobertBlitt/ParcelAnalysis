"""
Hawaii Matrix Project - Projection Checker (Robust Version)
Works around ArcGIS Pro installation issues
"""

import os

def check_projections_simple():
    """Simple projection checker using file system approach"""
    
    print("=" * 50)
    print("HAWAII MATRIX PROJECT - PROJECTION CHECKER")
    print("=" * 50)
    
    try:
        # Try to get project folder - fallback to hard-coded path if needed
        try:
            import arcpy
            project = arcpy.mp.ArcGISProject("CURRENT")
            project_folder = project.homeFolder
            print("Using current ArcGIS Pro project folder")
        except:
            # Fallback to known path
            project_folder = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
            print("Using fallback project folder")
        
        data_folder = os.path.join(project_folder, "data", "gis_downloads")
        
        if not os.path.exists(data_folder):
            print(f"ERROR: Could not find data folder: {data_folder}")
            return
        
        print(f"Scanning: {data_folder}")
        
        # Find shapefiles and check their .prj files
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
        
        # Check each file by reading .prj files
        ready_count = 0
        needs_fix_count = 0
        
        for shapefile in shapefiles:
            file_name = os.path.basename(shapefile)
            print(f"Checking: {file_name}")
            
            # Check projection by reading .prj file
            prj_file = shapefile.replace('.shp', '.prj')
            
            if os.path.exists(prj_file):
                try:
                    with open(prj_file, 'r') as f:
                        projection_text = f.read()
                    
                    if "NAD_1983_HARN_UTM_Zone_4N" in projection_text:
                        print("  -> Already correct (NAD 83 HARN UTM Zone 4N)")
                        ready_count += 1
                    else:
                        print("  -> NEEDS REPROJECTION")
                        if "GEOGCS" in projection_text and "PROJCS" not in projection_text:
                            print("  -> Currently: Geographic coordinates (degrees)")
                        elif "WGS_1984" in projection_text:
                            print("  -> Currently: WGS84")
                        elif "State_Plane" in projection_text:
                            print("  -> Currently: Hawaii State Plane")
                        else:
                            print("  -> Currently: Other projection")
                        needs_fix_count += 1
                        
                except Exception as e:
                    print(f"  -> Error reading projection: {e}")
            else:
                print("  -> ERROR: No .prj file found")
            
            print()
        
        # Summary
        print("=" * 50)
        print("PROJECTION STATUS SUMMARY:")
        print(f"Ready for analysis: {ready_count} files")
        print(f"Need reprojection: {needs_fix_count} files")
        print("=" * 50)
        
        if needs_fix_count > 0:
            print()
            print("TO FIX PROJECTIONS:")
            print("1. Use ArcGIS Pro Data Management Tools")
            print("2. Go to: Data Management Tools > Projections > Project")
            print("3. Target: NAD 83 HARN UTM Zone 4N (EPSG: 26904)")
            print("4. Or use the ArcGIS Pro Project tool in the ribbon")
        
        print()
        print("All files with correct projection are ready for Matrix analysis!")
        
    except Exception as e:
        print(f"Script error: {str(e)}")

# Run the function
check_projections_simple()
