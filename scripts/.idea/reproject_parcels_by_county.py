import arcpy
import os

# Path to your geodatabase
gdb_path = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis\ParcelAnalysis.gdb"

# Mapping of county names to WKIDs
county_proj = {
    "Hawaii": 102661,
    "Maui": 102642,
    "Honolulu": 102662,
    "Kauai": 102643
}

# Set the workspace
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

# List all feature classes in the geodatabase
fcs = arcpy.ListFeatureClasses()

for fc in fcs:
    print(f"Checking {fc}...")

    # Skip if name doesn't follow expected convention
    if not fc.startswith("Parcels_"):
        print(f"  Skipped: doesn't match naming convention.")
        continue

    # Extract county name
    county = fc.split("_")[1]

    # Lookup target projection
    wkid = county_proj.get(county)
    if not wkid:
        print(f"  Unknown county: {county}. Skipping.")
        continue

    # Get current spatial reference
    desc = arcpy.Describe(fc)
    current_wkid = desc.spatialReference.factoryCode

    if current_wkid == wkid:
        print(f"  Already in correct projection (WKID {wkid}). Skipping.")
        continue

    # Define target spatial reference
    target_sr = arcpy.SpatialReference(wkid)

    # Set output name
    out_fc = f"{fc}_proj"
    out_path = os.path.join(gdb_path, out_fc)

    # Reproject
    print(f"  Reprojecting to WKID {wkid} → {out_fc}")
    arcpy.Project_management(fc, out_path, target_sr)

print("✅ Reprojection complete.")
