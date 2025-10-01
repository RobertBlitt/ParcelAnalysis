"""
Create consistent folder structure for Hawaii Matrix Project
Each data type gets both county-specific and statewide folders
"""

import os

# Base path
base_path = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis\data\gis_downloads"

# Data types that need county + statewide organization
data_types = [
    'wells',
    'elevation', 
    'soils',
    'shoreline',
    'groundwater',
    'surface_water',
    'flood_zones',
    'parcels',
    'building_footprints',
    'zoning',
    'sewer_systems',
    'special_management_areas',
    'doh_priority_areas'
]

# County names
counties = ['hawaii_county', 'maui_county', 'honolulu_county', 'kauai_county']

def create_folder_structure():
    """Create consistent folder structure for all data types"""
    
    print("Creating consistent folder structure for Matrix project...")
    print(f"Base path: {base_path}")
    print()
    
    for data_type in data_types:
        print(f"Setting up: {data_type}")
        
        # Create main data type folder
        data_type_path = os.path.join(base_path, data_type)
        if not os.path.exists(data_type_path):
            os.makedirs(data_type_path)
            print(f"  Created: {data_type}/")
        
        # Create statewide folder
        statewide_path = os.path.join(data_type_path, 'statewide')
        if not os.path.exists(statewide_path):
            os.makedirs(statewide_path)
            print(f"  Created: {data_type}/statewide/")
        
        # Create county folders
        for county in counties:
            county_path = os.path.join(data_type_path, county)
            if not os.path.exists(county_path):
                os.makedirs(county_path)
                print(f"  Created: {data_type}/{county}/")
        
        print()
    
    print("✅ Folder structure creation complete!")
    print()
    print("📁 FINAL STRUCTURE:")
    print("gis_downloads/")
    for data_type in data_types:
        print(f"├── {data_type}/")
        print(f"│   ├── statewide/")
        for i, county in enumerate(counties):
            connector = "└──" if i == len(counties)-1 else "├──"
            print(f"│   {connector} {county}/")
    print()

if __name__ == "__main__":
    create_folder_structure()
