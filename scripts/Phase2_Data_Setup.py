"""
Hawaii Cesspool Matrix Analysis - Phase 2: Data Setup
University of Hawaii Water Resources Research Center
Sets up the data directory structure and locates existing files
"""

print("=" * 70)
print("Hawaii Cesspool Matrix Analysis - Phase 2: Data Setup")
print("=" * 70)
print("Academic Framework - University of Hawaii WRRC")

import datetime
import os
import glob
import shutil

print(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Set workspace
workspace = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
data_dir = os.path.join(workspace, "data")

# Create all required subdirectories
required_subdirs = [
    "parcels",
    "iww_inventory", 
    "wells",
    "elevation",
    "soils",
    "zoning",
    "gis_downloads"  # For new data downloads
]

print("\nCreating data directory structure...")
for subdir in required_subdirs:
    dir_path = os.path.join(data_dir, subdir)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created: {dir_path}")
    else:
        print(f"Found: {dir_path}")

# Look for the technology matrix file (TechnologyTreatmentDisposalTreat.xlsx)
print("\n=== SEARCHING FOR EXISTING FILES ===")

def find_files_recursive(root_dir, pattern):
    """Find files matching pattern in root_dir and all subdirectories"""
    matches = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if pattern.lower() in filename.lower():
                matches.append(os.path.join(root, filename))
    return matches

# Search for technology matrix
print("Searching for TechnologyTreatmentDisposalTreat.xlsx...")
tech_files = find_files_recursive(workspace, "TechnologyTreatmentDisposalTreat")
if tech_files:
    print("Found technology matrix files:")
    for i, file_path in enumerate(tech_files, 1):
        print(f"  {i}. {file_path}")
    
    # Copy the first one to the correct location if it's not there already
    target_path = os.path.join(data_dir, "TechnologyTreatmentDisposalTreat.xlsx")
    if not os.path.exists(target_path) and tech_files:
        shutil.copy2(tech_files[0], target_path)
        print(f"✓ Copied technology matrix to: {target_path}")
else:
    print("⚠ Technology matrix not found in project directory")

# Search for other data files
file_patterns = {
    "parcel": ["parcel", "tmk", "tax"],
    "cesspool": ["cesspool", "iww", "wastewater"],
    "wells": ["well", "water"],
    "dem": ["dem", "elevation", "topography"],
    "soil": ["soil", "nrcs"],
    "zoning": ["zoning", "landuse"]
}

print("\nSearching for other data files...")
for category, patterns in file_patterns.items():
    print(f"\n--- {category.upper()} FILES ---")
    found_files = []
    
    for pattern in patterns:
        # Look for shapefiles
        shp_files = find_files_recursive(workspace, f"{pattern}.shp")
        found_files.extend(shp_files)
        
        # Look for other GIS files
        gdb_files = find_files_recursive(workspace, f"{pattern}")
        gdb_files = [f for f in gdb_files if f.endswith(('.gdb', '.tif', '.tiff'))]
        found_files.extend(gdb_files)
    
    # Remove duplicates
    found_files = list(set(found_files))
    
    if found_files:
        print(f"Found {len(found_files)} {category} file(s):")
        for file_path in found_files[:5]:  # Show first 5
            print(f"  • {os.path.basename(file_path)} in {os.path.dirname(file_path)}")
        if len(found_files) > 5:
            print(f"  ... and {len(found_files) - 5} more")
    else:
        print(f"No {category} files found")

# Create a data inventory report
inventory_file = os.path.join(workspace, "data_inventory_report.txt")
print(f"\n=== CREATING DATA INVENTORY REPORT ===")
print(f"Report will be saved to: {inventory_file}")

with open(inventory_file, 'w', encoding='utf-8') as f:
    f.write("Hawaii Cesspool Matrix Analysis - Data Inventory Report\n")
    f.write("=" * 60 + "\n")
    f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Project Directory: {workspace}\n\n")
    
    f.write("REQUIRED DATA FILES:\n")
    f.write("-" * 20 + "\n")
    
    required_files = {
        "Technology Matrix": "TechnologyTreatmentDisposalTreat.xlsx",
        "Parcel Data": "Statewide parcel/TMK shapefiles",
        "Cesspool Inventory": "Individual wastewater system locations",
        "Wells Data": "Municipal and domestic well locations", 
        "Elevation Data": "Digital elevation model (DEM)",
        "Soils Data": "NRCS soils shapefile",
        "Zoning Data": "County zoning/land use data"
    }
    
    for desc, filename in required_files.items():
        f.write(f"• {desc}: {filename}\n")
    
    f.write(f"\nDATA DIRECTORY STRUCTURE:\n")
    f.write("-" * 25 + "\n")
    for subdir in required_subdirs:
        dir_path = os.path.join(data_dir, subdir)
        status = "EXISTS" if os.path.exists(dir_path) else "CREATED"
        f.write(f"• data/{subdir}/  [{status}]\n")
    
    f.write(f"\nNEXT STEPS:\n")
    f.write("-" * 10 + "\n")
    f.write("1. Locate and copy required data files to appropriate directories\n")
    f.write("2. Run data verification script to check file formats\n")
    f.write("3. Proceed with Phase 3: Site Conditions Analysis\n")

print(f"✓ Data inventory report created: {inventory_file}")

print("\n=== PHASE 2 COMPLETE ===")
print("Directory structure is now ready for data files.")
print("Next: Locate your Hawaii GIS data and place in appropriate folders:")
print("  • Technology matrix → data/")
print("  • Parcel data → data/parcels/")
print("  • Cesspool inventory → data/iww_inventory/")
print("  • Wells data → data/wells/")
print("  • DEM → data/elevation/")
print("  • Soils → data/soils/")
print("  • Zoning → data/zoning/")
