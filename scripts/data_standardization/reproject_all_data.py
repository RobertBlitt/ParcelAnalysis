"""
Data Standardization Script for Hawaii Matrix Project
Reprojects all downloaded GIS data to HCPT standard: NAD 83 HARN UTM Zone 4N (EPSG:26904)
"""

import arcpy
import os
import sys
from datetime import datetime

# Set up logging
def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def reproject_to_hcpt_standard(input_dataset, output_dataset):
    """
    Reproject any dataset to HCPT standard: NAD 83 HARN UTM Zone 4N (EPSG:26904)
    
    Parameters:
    input_dataset (str): Path to source dataset
    output_dataset (str): Path for reprojected output
    
    Returns:
    bool: True if successful, False if failed
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_dataset)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            log_message(f"Created directory: {output_dir}")
        
        # Target coordinate system: NAD 83 HARN UTM Zone 4N
        target_crs = arcpy.SpatialReference(26904)
        
        # Get source projection info
        desc = arcpy.Describe(input_dataset)
        source_crs = desc.spatialReference
        
        log_message(f"Source: {source_crs.name} (EPSG:{source_crs.factoryCode})")
        log_message(f"Target: {target_crs.name} (EPSG:{target_crs.factoryCode})")
        
        # Check if reprojection is needed
        if source_crs.factoryCode == 26904:
            log_message("Dataset already in target projection, copying...")
            arcpy.management.Copy(input_dataset, output_dataset)
        else:
            # Reproject
            log_message("Reprojecting dataset...")
            arcpy.management.Project(
                in_dataset=input_dataset,
                out_dataset=output_dataset,
                out_coor_system=target_crs,
                transform_method="",  # Auto-select transformation
                in_coor_system="",    # Auto-detect source
                preserve_shape="NO_PRESERVE_SHAPE",
                max_deviation="",
                vertical="NO_VERTICAL"
            )
        
        # Verify output projection
        output_desc = arcpy.Describe(output_dataset)
        if output_desc.spatialReference.factoryCode == 26904:
            log_message(f"✅ Successfully reprojected: {os.path.basename(output_dataset)}")
            return True
        else:
            log_message(f"❌ Reprojection failed: Wrong output projection", "ERROR")
            return False
            
    except Exception as e:
        log_message(f"❌ Error reprojecting {input_dataset}: {str(e)}", "ERROR")
        return False

def batch_reproject_folder(input_folder, output_folder, file_extensions=None):
    """
    Batch reproject all GIS files in a folder structure
    
    Parameters:
    input_folder (str): Root folder containing raw downloads
    output_folder (str): Root folder for standardized outputs
    file_extensions (list): File extensions to process (default: ['.shp', '.gdb'])
    """
    if file_extensions is None:
        file_extensions = ['.shp', '.gdb']
    
    log_message(f"Starting batch reprojection:")
    log_message(f"Input folder: {input_folder}")
    log_message(f"Output folder: {output_folder}")
    
    success_count = 0
    error_count = 0
    
    # Walk through input folder structure
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if file has target extension
            file_name, file_ext = os.path.splitext(file)
            if file_ext.lower() in file_extensions:
                
                # Build paths
                input_path = os.path.join(root, file)
                
                # Create corresponding output path structure
                rel_path = os.path.relpath(root, input_folder)
                output_root = os.path.join(output_folder, rel_path)
                output_path = os.path.join(output_root, file)
                
                log_message(f"Processing: {file}")
                
                # Reproject
                if reproject_to_hcpt_standard(input_path, output_path):
                    success_count += 1
                else:
                    error_count += 1
    
    log_message(f"Batch processing complete:")
    log_message(f"✅ Successfully processed: {success_count} files")
    log_message(f"❌ Errors: {error_count} files")
    
    return success_count, error_count

def verify_projection_batch(folder_path):
    """
    Verify that all datasets in folder are in correct projection
    """
    log_message("Verifying projections...")
    
    correct_count = 0
    incorrect_count = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.shp'):
                file_path = os.path.join(root, file)
                
                try:
                    desc = arcpy.Describe(file_path)
                    if desc.spatialReference.factoryCode == 26904:
                        correct_count += 1
                        log_message(f"✅ {file}: Correct projection")
                    else:
                        incorrect_count += 1
                        log_message(f"❌ {file}: Wrong projection ({desc.spatialReference.name})", "WARNING")
                        
                except Exception as e:
                    incorrect_count += 1
                    log_message(f"❌ {file}: Error checking projection - {str(e)}", "ERROR")
    
    log_message(f"Verification complete: {correct_count} correct, {incorrect_count} incorrect")
    return correct_count, incorrect_count

# Configuration for Matrix project
MATRIX_CONFIG = {
    'project_root': r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis",
    'raw_data_folder': r"data\state_gis_downloads\_raw",
    'standardized_folder': r"data\state_gis_downloads\_standardized",
    'target_epsg': 26904,  # NAD 83 HARN UTM Zone 4N
}

def main():
    """
    Main function - standardize all Matrix project data
    """
    log_message("=" * 60)
    log_message("HAWAII MATRIX PROJECT - DATA STANDARDIZATION")
    log_message("Target Projection: NAD 83 HARN UTM Zone 4N (EPSG:26904)")
    log_message("=" * 60)
    
    # Set up paths
    project_root = MATRIX_CONFIG['project_root']
    raw_folder = os.path.join(project_root, MATRIX_CONFIG['raw_data_folder'])
    standardized_folder = os.path.join(project_root, MATRIX_CONFIG['standardized_folder'])
    
    # Check if raw data folder exists
    if not os.path.exists(raw_folder):
        log_message(f"Raw data folder not found: {raw_folder}", "ERROR")
        log_message("Please download data first using the acquisition plan.", "ERROR")
        return
    
    # Create standardized folder if needed
    if not os.path.exists(standardized_folder):
        os.makedirs(standardized_folder)
        log_message(f"Created standardized data folder: {standardized_folder}")
    
    # Batch reproject all data
    success_count, error_count = batch_reproject_folder(raw_folder, standardized_folder)
    
    # Verify results
    if success_count > 0:
        log_message("Verifying reprojected datasets...")
        verify_projection_batch(standardized_folder)
    
    log_message("=" * 60)
    log_message("DATA STANDARDIZATION COMPLETE")
    log_message(f"All standardized data ready in: {standardized_folder}")
    log_message("=" * 60)

if __name__ == "__main__":
    # Check if ArcGIS is available
    try:
        import arcpy
        log_message("ArcGIS environment detected")
        main()
    except ImportError:
        print("ERROR: ArcGIS/arcpy not available. This script requires ArcGIS Pro or ArcMap.")
        print("Alternative: Use GDAL/OGR tools for reprojection.")
        sys.exit(1)
