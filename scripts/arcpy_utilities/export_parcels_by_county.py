import arcpy

# Set workspace to your ParcelAnalysis.gdb path
arcpy.env.workspace = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis\ParcelAnalysis.gdb"
arcpy.env.overwriteOutput = True

# Input feature class (must be inside the gdb)
input_fc = "tmk_state"

# Get all unique counties
counties = set(row[0] for row in arcpy.da.SearchCursor(input_fc, ["COUNTY"]))

# Loop through and export each county to its own feature class
for county in sorted(counties):
    out_fc = f"Parcels_{county.replace(' ', '_')}"
    where_clause = f"COUNTY = '{county}'"
    print(f"Exporting {out_fc}...")
    arcpy.Select_analysis(input_fc, out_fc, where_clause)

print("✅ All county parcel exports complete.")
