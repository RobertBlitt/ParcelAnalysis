# Data Standardization and Reprojection Tools
# Hawaii Cesspool Analysis Project - HCPT Compatible Projection

## **🎯 TARGET PROJECTION: NAD 83 HARN UTM Zone 4N (EPSG:26904)**

Based on HCPT documentation: "State GIS Program projected all county tmk layers to UTM Zone 4, NAD 83 HARN"

This ensures our Matrix analysis is fully compatible with existing HCPT maps and tools.

---

## **📊 COMMON DATA SOURCE PROJECTIONS WE'LL ENCOUNTER:**

### **Hawaii State GIS Downloads**
- **As Downloaded**: WGS84 Geographic (EPSG:4326) 
- **Internal Storage**: NAD 83 HARN UTM Zone 4N (EPSG:26904)
- **Reprojection Needed**: YES (from WGS84 to NAD 83 HARN UTM)

### **County GIS Downloads**
- **Variable by County**: Each county may use different projections
- **Common**: Hawaii State Plane Zone 3 (EPSG:2783) or WGS84 (EPSG:4326)
- **Reprojection Needed**: YES (standardize all to NAD 83 HARN UTM)

### **Federal Data (USGS, NRCS, FEMA)**
- **Typical**: NAD 83 Geographic (EPSG:4269) or WGS84 (EPSG:4326)
- **Reprojection Needed**: YES (to NAD 83 HARN UTM Zone 4N)

### **CWRM Data**
- **Likely**: Various projections depending on data age
- **Reprojection Needed**: Assume YES

---

## **🔧 REPROJECTION TOOLS AND SCRIPTS**

### **Option 1: ArcGIS Pro Geoprocessing**
```python
import arcpy

def reproject_to_hcpt_standard(input_dataset, output_dataset):
    """
    Reproject any dataset to HCPT standard: NAD 83 HARN UTM Zone 4N
    """
    # Target coordinate system
    target_crs = arcpy.SpatialReference(26904)  # NAD 83 HARN UTM Zone 4N
    
    # Reproject
    arcpy.management.Project(
        in_dataset=input_dataset,
        out_dataset=output_dataset,
        out_coor_system=target_crs,
        transform_method="",  # ArcGIS will auto-select appropriate transformation
        in_coor_system="",    # Auto-detect source projection
        preserve_shape="NO_PRESERVE_SHAPE",
        max_deviation="",
        vertical="NO_VERTICAL"
    )
    
    print(f"Reprojected {input_dataset} to NAD 83 HARN UTM Zone 4N")
    print(f"Output: {output_dataset}")

# Example usage
input_path = r"C:\...\original_data.shp"
output_path = r"C:\...\standardized_data.shp"
reproject_to_hcpt_standard(input_path, output_path)
```

### **Option 2: Batch Processing Script**
```python
import arcpy
import os

def batch_reproject_folder(input_folder, output_folder):
    """
    Batch reproject all shapefiles in a folder to HCPT standard
    """
    target_crs = arcpy.SpatialReference(26904)  # NAD 83 HARN UTM Zone 4N
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Walk through input folder
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.shp'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_folder, file)
                
                try:
                    arcpy.management.Project(
                        in_dataset=input_path,
                        out_dataset=output_path,
                        out_coor_system=target_crs
                    )
                    print(f"✅ Reprojected: {file}")
                except Exception as e:
                    print(f"❌ Error reprojecting {file}: {e}")

# Example usage
batch_reproject_folder(
    r"C:\...\ParcelAnalysis\data\state_gis_downloads\parcels\raw",
    r"C:\...\ParcelAnalysis\data\state_gis_downloads\parcels\standardized"
)
```

### **Option 3: GDAL/OGR Command Line (Alternative)**
```bash
# Reproject shapefile using ogr2ogr
ogr2ogr -f "ESRI Shapefile" \
        -t_srs EPSG:26904 \
        -s_srs EPSG:4326 \
        output_file.shp \
        input_file.shp

# Batch processing with PowerShell/Bash
for file in *.shp; do
    ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:26904 "standardized_$file" "$file"
done
```

---

## **📋 STEP 0: DATA STANDARDIZATION WORKFLOW**

### **For Each Downloaded Dataset:**

**Step 0.1: Check Source Projection**
```python
import arcpy

def check_projection(dataset_path):
    desc = arcpy.Describe(dataset_path)
    if desc.spatialReference.name:
        print(f"Current projection: {desc.spatialReference.name}")
        print(f"EPSG Code: {desc.spatialReference.factoryCode}")
    else:
        print("⚠️ WARNING: No projection defined!")
```

**Step 0.2: Reproject to Standard**
```python
# Use the reproject_to_hcpt_standard function above
reproject_to_hcpt_standard(input_dataset, output_dataset)
```

**Step 0.3: Verify Reprojection**
```python
def verify_projection(dataset_path):
    desc = arcpy.Describe(dataset_path)
    target_name = "NAD_1983_HARN_UTM_Zone_4N"
    
    if target_name in desc.spatialReference.name:
        print(f"✅ Correct projection: {desc.spatialReference.name}")
        return True
    else:
        print(f"❌ Wrong projection: {desc.spatialReference.name}")
        return False
```

**Step 0.4: Update Field Names (if needed)**
```python
def standardize_field_names(dataset_path):
    """
    Standardize field names according to our Matrix conventions
    """
    field_mappings = {
        'OBJECTID': 'ID_FEATURE',
        'TMK': 'ID_TMK',
        'Shape_Area': 'AREA_SQFT',
        'Shape_Length': 'LENGTH_FT'
    }
    
    fields = arcpy.ListFields(dataset_path)
    for field in fields:
        if field.name in field_mappings:
            arcpy.management.AlterField(
                dataset_path, 
                field.name, 
                field_mappings[field.name]
            )
```

---

## **🗂️ ORGANIZED FOLDER STRUCTURE FOR STANDARDIZATION**

```
data/state_gis_downloads/
├── _raw/                     # Original downloads (preserve originals)
│   ├── wells/
│   ├── parcels/
│   └── [other folders]
├── _standardized/            # Reprojected to NAD 83 HARN UTM Zone 4N
│   ├── wells/
│   ├── parcels/
│   └── [other folders]
└── [working folders continue as normal]
```

### **Modified Workflow:**
1. **Download** → Save to `_raw/` folders
2. **Step 0: Standardize** → Reproject and save to `_standardized/`
3. **Analysis** → Use data from `_standardized/` folders

---

## **⚠️ IMPORTANT PROJECTION NOTES:**

### **NAD 83 vs NAD 83 HARN Transformation**
- **NAD 83 HARN** (High Accuracy Reference Network) is more precise
- **Transformation required** when going from NAD 83 to NAD 83 HARN
- **ArcGIS will auto-select** appropriate transformation method

### **Coordinate System Verification**
Always verify after reprojection:
- **Check extent** - should be in meters, roughly 200,000-800,000 range for Hawaii
- **Check units** - should be meters, not degrees
- **Visual inspection** - overlay with known HCPT data to verify alignment

### **Precision Considerations for Setback Calculations**
- **UTM projection** provides accurate distance calculations
- **Critical for Matrix analysis** where 100/150 ft setbacks must be precise
- **Avoids distortion** that would occur with geographic coordinates

---

## **🔧 IMPLEMENTATION IN JUPYTER NOTEBOOKS**

### **Notebook 1A: Data Acquisition and Standardization**
```python
# Cell 1: Import and setup
import arcpy
import os
import sys

# Set workspace
workspace = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
arcpy.env.workspace = workspace

# Cell 2: Define reprojection function
def reproject_to_hcpt_standard(input_dataset, output_dataset):
    # [Function code as above]

# Cell 3: Process each downloaded dataset
datasets_to_process = [
    (r"data\_raw\wells\cwrm_wells.shp", r"data\_standardized\wells\cwrm_wells.shp"),
    (r"data\_raw\parcels\hawaii_county\tmk.shp", r"data\_standardized\parcels\hawaii_county\tmk.shp"),
    # ... etc for all datasets
]

for input_path, output_path in datasets_to_process:
    if arcpy.Exists(input_path):
        reproject_to_hcpt_standard(input_path, output_path)
    else:
        print(f"⚠️ File not found: {input_path}")
```

---

**🎯 This ensures all Matrix analysis data is in the same projection as the existing HCPT, enabling perfect integration and accurate distance calculations for HAR 11-62 setback requirements.**
