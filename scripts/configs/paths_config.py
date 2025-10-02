"""
Path Configuration for ParcelAnalysis Project
University of Hawaii Water Resources Research Center

Update BASE_PATH when moving between machines.
All other paths are derived from BASE_PATH.

Last Updated: October 2, 2025
"""

import os

# ============================================================================
# BASE PATH - UPDATE THIS FOR YOUR MACHINE
# ============================================================================
BASE_PATH = r"C:\GIS_Projects\ParcelAnalysis"

# ============================================================================
# DERIVED PATHS - Do not modify these (they're built from BASE_PATH)
# ============================================================================

# Main directories
DATA_DIR = os.path.join(BASE_PATH, "data")
OUTPUTS_DIR = os.path.join(BASE_PATH, "Outputs")
SCRIPTS_DIR = os.path.join(BASE_PATH, "scripts")
REFERENCE_DIR = os.path.join(BASE_PATH, "reference")
MATRIX_DIR = os.path.join(BASE_PATH, "Matrix")
SCRATCH_DIR = os.path.join(BASE_PATH, "scratch")

# Geodatabase
GDB_PATH = os.path.join(BASE_PATH, "ParcelAnalysis.gdb")

# Data subdirectories
GIS_DOWNLOADS_DIR = os.path.join(DATA_DIR, "gis_downloads")
WELLS_DIR = os.path.join(GIS_DOWNLOADS_DIR, "wells")
SOILS_DIR = os.path.join(DATA_DIR, "soils")
BUILDING_FOOTPRINTS_DIR = os.path.join(DATA_DIR, "buildings")
PARCELS_DIR = os.path.join(DATA_DIR, "parcels")

# Output subdirectories
SOIL_ANALYSIS_DIR = os.path.join(OUTPUTS_DIR, "soil_analysis")
FOUNDATION_DIR = os.path.join(OUTPUTS_DIR, "foundation")
VALIDATION_DIR = os.path.join(OUTPUTS_DIR, "validation")
MAPS_DIR = os.path.join(OUTPUTS_DIR, "maps")

# ============================================================================
# GEODATABASE FEATURE CLASSES
# ============================================================================

# Master tables
MASTER_TABLE = os.path.join(GDB_PATH, "Complete_Master_Analysis_Table")

# Soil layers
SOIL_LAYER = os.path.join(GDB_PATH, "HIstate_nrcs_join2")
CLASSIFIED_SOILS = os.path.join(GDB_PATH, "Classified_Soil_Units")
BUILDABLE_AREAS = os.path.join(GDB_PATH, "Parcel_Buildable_Areas")
SOIL_INTERSECTIONS = os.path.join(GDB_PATH, "Buildable_Soil_Intersections")

# Wells layers
MUNICIPAL_WELLS = os.path.join(GDB_PATH, "Municipal_Wells")
DOMESTIC_WELLS = os.path.join(GDB_PATH, "Domestic_Wells")

# Building footprints
ALL_BUILDING_FOOTPRINTS = os.path.join(GDB_PATH, "All_Building_Footprints")
HONOLULU_BUILDINGS = os.path.join(GDB_PATH, "Honolulu_Building_Footprints")
MAUI_BUILDINGS = os.path.join(GDB_PATH, "Maui_Building_Footprints")
HAWAII_BUILDINGS = os.path.join(GDB_PATH, "Hawaii_Building_Footprints")
KAUAI_BUILDINGS = os.path.join(GDB_PATH, "Kauai_Building_Footprints")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_paths():
    """
    Validate that critical paths exist.
    Returns: (bool, list of missing paths)
    """
    critical_paths = [
        (BASE_PATH, "Base project directory"),
        (GDB_PATH, "Geodatabase"),
        (DATA_DIR, "Data directory"),
        (SCRIPTS_DIR, "Scripts directory")
    ]
    
    missing = []
    for path, description in critical_paths:
        if not os.path.exists(path):
            missing.append(f"{description}: {path}")
    
    if missing:
        return False, missing
    return True, []

def print_config():
    """Print current configuration for debugging."""
    print("=" * 70)
    print("ParcelAnalysis Path Configuration")
    print("=" * 70)
    print(f"Base Path: {BASE_PATH}")
    print(f"Geodatabase: {GDB_PATH}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Scripts Directory: {SCRIPTS_DIR}")
    print(f"Outputs Directory: {OUTPUTS_DIR}")
    print()
    
    valid, missing = validate_paths()
    if valid:
        print("✅ All critical paths exist")
    else:
        print("❌ Missing paths:")
        for path in missing:
            print(f"  - {path}")
    print("=" * 70)

# ============================================================================
# VERIFY ON IMPORT
# ============================================================================

if __name__ == "__main__":
    print_config()
else:
    # Quick validation on import
    valid, missing = validate_paths()
    if not valid:
        import warnings
        warnings.warn(
            f"ParcelAnalysis paths_config: Some critical paths don't exist. "
            f"Run paths_config.print_config() to see details."
        )
