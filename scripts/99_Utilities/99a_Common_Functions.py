# COMMON FUNCTIONS - Kitchen Utilities
# Reusable functions for Hawaii Cesspool Matrix Analysis

import arcpy
import os
from datetime import datetime

def log_workflow_step(step_name, details=""):
    """Log workflow steps with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {step_name}: {details}")

def validate_layer_exists(layer_name):
    """Check if layer exists in current map"""
    try:
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map_obj = aprx.activeMap
        layer_names = [layer.name for layer in map_obj.listLayers()]
        
        if layer_name not in layer_names:
            print(f"Available layers: {layer_names}")
            raise ValueError(f"Layer '{layer_name}' not found in map")
        return True
    except Exception as e:
        print(f"Error validating layer: {e}")
        return False

def create_output_path(base_folder, layer_name, suffix=""):
    """Create standardized output paths"""
    if suffix:
        output_name = f"{layer_name}_{suffix}"
    else:
        output_name = layer_name
    
    return os.path.join(base_folder, output_name + ".shp")

def get_field_info(layer_path):
    """Get comprehensive field information for a layer"""
    fields_info = []
    for field in arcpy.ListFields(layer_path):
        fields_info.append({
            'name': field.name,
            'type': field.type,
            'length': field.length,
            'alias': field.aliasName
        })
    return fields_info

def count_records_by_field(layer_path, field_name):
    """Count unique values in a field"""
    value_counts = {}
    with arcpy.da.SearchCursor(layer_path, [field_name]) as cursor:
        for row in cursor:
            value = row[0] if row[0] is not None else "NULL"
            value_counts[value] = value_counts.get(value, 0) + 1
    return value_counts

def create_folder_if_not_exists(folder_path):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        log_workflow_step("Folder Creation", f"Created: {folder_path}")
        return True
    return False

def backup_layer(source_layer, backup_folder):
    """Create timestamped backup of a layer"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_layer}_backup_{timestamp}"
    backup_path = os.path.join(backup_folder, backup_name + ".shp")
    
    arcpy.management.CopyFeatures(source_layer, backup_path)
    log_workflow_step("Backup", f"Created backup: {backup_path}")
    return backup_path

def validate_required_fields(layer_path, required_fields):
    """Check if all required fields exist in layer"""
    existing_fields = [f.name for f in arcpy.ListFields(layer_path)]
    missing_fields = [f for f in required_fields if f not in existing_fields]
    
    if missing_fields:
        raise ValueError(f"Missing required fields in {layer_path}: {missing_fields}")
    else:
        log_workflow_step("Validation", f"All required fields present: {required_fields}")
        return True

def calculate_completeness_stats(layer_path, fields_to_check):
    """Calculate data completeness statistics for specified fields"""
    total_records = int(arcpy.management.GetCount(layer_path)[0])
    completeness_stats = {}
    
    for field in fields_to_check:
        non_null_count = 0
        with arcpy.da.SearchCursor(layer_path, [field]) as cursor:
            for row in cursor:
                if row[0] is not None and str(row[0]).strip() != "":
                    non_null_count += 1
        
        completeness_pct = (non_null_count / total_records) * 100 if total_records > 0 else 0
        completeness_stats[field] = {
            'populated': non_null_count,
            'total': total_records,
            'percentage': completeness_pct
        }
    
    return completeness_stats

def add_tracking_field(layer_path, field_name="PROCESS_LOG", initial_value=""):
    """Add a tracking field to monitor processing steps"""
    try:
        arcpy.management.AddField(layer_path, field_name, "TEXT", field_length=200)
        
        if initial_value:
            with arcpy.da.UpdateCursor(layer_path, [field_name]) as cursor:
                for row in cursor:
                    row[0] = initial_value
                    cursor.updateRow(row)
        
        log_workflow_step("Tracking", f"Added tracking field: {field_name}")
        return True
    except Exception as e:
        log_workflow_step("Error", f"Could not add tracking field: {e}")
        return False

def export_summary_csv(layer_path, output_csv, fields_to_export):
    """Export specified fields to CSV for analysis"""
    import csv
    
    # Validate fields exist
    existing_fields = [f.name for f in arcpy.ListFields(layer_path)]
    export_fields = [f for f in fields_to_export if f in existing_fields]
    
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(export_fields)  # Header
        
        with arcpy.da.SearchCursor(layer_path, export_fields) as cursor:
            for row in cursor:
                writer.writerow(row)
    
    log_workflow_step("Export", f"CSV created: {output_csv}")
    return output_csv

def print_layer_summary(layer_path, layer_name="Layer"):
    """Print comprehensive layer summary"""
    try:
        record_count = int(arcpy.management.GetCount(layer_path)[0])
        fields = [f.name for f in arcpy.ListFields(layer_path)]
        
        print(f"\n=== {layer_name.upper()} SUMMARY ===")
        print(f"Path: {layer_path}")
        print(f"Records: {record_count:,}")
        print(f"Fields ({len(fields)}): {', '.join(fields[:10])}{'...' if len(fields) > 10 else ''}")
        
        # Get spatial extent if it's a feature class
        try:
            desc = arcpy.Describe(layer_path)
            if hasattr(desc, 'extent'):
                extent = desc.extent
                print(f"Extent: {extent.XMin:.2f}, {extent.YMin:.2f}, {extent.XMax:.2f}, {extent.YMax:.2f}")
                print(f"Spatial Reference: {desc.spatialReference.name}")
        except:
            pass
        
        return True
    except Exception as e:
        print(f"Error summarizing layer: {e}")
        return False

# HAR 11-62 specific validation functions
def validate_har_classifications(layer_path):
    """Validate HAR 11-62 classification fields"""
    har_fields = ['HAR_SLOPE_CLASS', 'HAR_PERC_CLASS', 'HAR_DRAINAGE_CLASS']
    
    valid_values = {
        'HAR_SLOPE_CLASS': ['<8%', '8-12%', '>12%', 'Unknown'],
        'HAR_PERC_CLASS': ['<1 min/inch', '1-10 min/inch', '10-60 min/inch', '>60 min/inch', 'Unknown'],
        'HAR_DRAINAGE_CLASS': ['Good', 'Moderate', 'Poor', 'Unknown']
    }
    
    validation_results = {}
    
    for field in har_fields:
        if field not in [f.name for f in arcpy.ListFields(layer_path)]:
            validation_results[field] = "MISSING"
            continue
        
        invalid_count = 0
        total_count = 0
        
        with arcpy.da.SearchCursor(layer_path, [field]) as cursor:
            for row in cursor:
                total_count += 1
                if row[0] not in valid_values[field]:
                    invalid_count += 1
        
        validation_results[field] = {
            'invalid_count': invalid_count,
            'total_count': total_count,
            'validity_percentage': ((total_count - invalid_count) / total_count) * 100 if total_count > 0 else 0
        }
    
    return validation_results

# Add more utility functions as needed...
