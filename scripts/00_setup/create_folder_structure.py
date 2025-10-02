"""
Setup Data Folder Structure for ParcelAnalysis Project

Creates complete folder hierarchy with proper organization for:
- Source data (read-only)
- Interim/working data
- Processed outputs
- Documentation

Run this once to initialize project structure.

Author: UH WRRC
Date: October 2, 2025
"""

import os
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """Create complete ParcelAnalysis data folder structure."""
    
    print("=" * 70)
    print("ParcelAnalysis Data Folder Setup")
    print("University of Hawaii Water Resources Research Center")
    print("=" * 70)
    print()
    
    # Base paths
    project_root = Path("C:/GIS_Projects/ParcelAnalysis")
    data_root = project_root / "data"
    
    # Folder structure
    folders = {
        # Raw data folders (source data, read-only)
        "00_raw": [
            "parcels",
            "cesspools",
            "slope",
            "soils",
            "groundwater",
            "wells_domestic",
            "wells_municipal",
            "shoreline",
            "surface_water",
            "zoning",
            "sma",
            "flood",
            "tsunami",
            "habitat",
            "building_footprints"
        ],
        
        # Interim/working folders
        "01_interim": [
            "reprojected",
            "clipped",
            "cleaned",
            "_processing_logs"
        ],
        
        # Processed/final folders
        "02_processed": [
            "Master_Parcel_Attribute_Table",
            "classified_soils",
            "buildable_areas",
            "wells_with_buffers",
            "matrix_results"
        ],
        
        # External reference data
        "03_external": [
            "lookup_tables",
            "regulatory_thresholds"
        ],
        
        # Documentation
        "04_docs": [
            "data_dictionaries",
            "licenses",
            "download_logs",
            "provenance_notes"
        ]
    }
    
    # Additional top-level folders
    other_folders = [
        "outputs/maps",
        "outputs/reports",
        "outputs/tables",
        "outputs/final_deliverables",
        "matrix",
        "notes_readme/methodology",
        "notes_readme/meeting_notes",
        "notes_readme/decisions_log",
        "validation/QC_scripts",
        "validation/validation_reports"
    ]
    
    created_count = 0
    
    # Create data subfolders
    print("Creating data folder structure...")
    print()
    
    for main_folder, subfolders in folders.items():
        main_path = data_root / main_folder
        main_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: data/{main_folder}/")
        created_count += 1
        
        for subfolder in subfolders:
            sub_path = main_path / subfolder
            sub_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {subfolder}/")
            created_count += 1
    
    print()
    
    # Create other project folders
    print("Creating additional project folders...")
    print()
    
    for folder in other_folders:
        folder_path = project_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {folder}/")
        created_count += 1
    
    print()
    print("=" * 70)
    print(f"Setup Complete! Created {created_count} folders.")
    print("=" * 70)
    print()
    
    # Create README placeholders in key folders
    print("Creating README files in key locations...")
    print()
    
    readme_locations = {
        data_root / "00_raw" / "README.txt": 
            "SOURCE DATA - READ ONLY\n\n"
            "This folder contains original data exactly as downloaded from source.\n"
            "DO NOT EDIT files in this folder.\n"
            "Copy to 01_interim/ for any modifications.\n\n"
            "Document all downloads in 04_docs/download_logs/",
            
        data_root / "01_interim" / "README.txt":
            "WORKING DATA\n\n"
            "Temporary workspace for data transformations.\n"
            "Safe to delete and regenerate.\n"
            "Log all processing steps in _processing_logs/",
            
        data_root / "02_processed" / "README.txt":
            "FINAL OUTPUTS\n\n"
            "Analysis-ready datasets and deliverables.\n"
            "These are your publication-quality products.\n"
            "Use version dates in filenames: [name]_YYYYMMDD.[ext]",
            
        data_root / "03_external" / "README.txt":
            "REFERENCE DATA\n\n"
            "Small lookup tables and regulatory thresholds.\n"
            "These may be tracked in Git if lightweight (<1 MB).",
            
        data_root / "04_docs" / "download_logs" / "README.txt":
            "DATA ACQUISITION LOG\n\n"
            "For each dataset, create a file: YYYYMMDD_[dataset_name].md\n"
            "Include:\n"
            "- Source URL\n"
            "- Download date\n"
            "- Dataset version/date\n"
            "- Contact information\n"
            "- License information\n"
            "- Known limitations"
    }
    
    for readme_path, content in readme_locations.items():
        readme_path.write_text(content)
        print(f"✓ Created: {readme_path.relative_to(project_root)}")
    
    print()
    print("=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print()
    print("1. Set data/00_raw/ folder to READ-ONLY in Windows Explorer")
    print("   (Right-click folder → Properties → Read-only → Apply)")
    print()
    print("2. Copy configs/paths.example.yaml to configs/paths.yaml")
    print("   and customize for your machine")
    print()
    print("3. Begin data acquisition - see ROADMAP.md Phase 1")
    print()
    print("4. Document all downloads in data/04_docs/download_logs/")
    print()
    print("=" * 70)
    
    # Create initial download log template
    today = datetime.now().strftime("%Y%m%d")
    template_path = data_root / "04_docs" / "download_logs" / f"{today}_TEMPLATE.md"
    template_content = """# Data Download Log Template

**Dataset Name**: [Name of the dataset]  
**Downloaded By**: [Your name]  
**Download Date**: [YYYY-MM-DD]  

## Source Information

**Source Agency**: [e.g., Hawaii State GIS, DOH, NRCS]  
**Source URL**: [Direct download link]  
**Dataset Version/Date**: [Version number or date of data]  
**Contact**: [Name and email of data provider]  

## Dataset Description

[Brief description of what this dataset contains and its purpose in the project]

## Technical Details

**Format**: [e.g., Shapefile, GeoTIFF, GDB, CSV]  
**Projection**: [Native CRS/projection]  
**Coverage**: [Geographic extent - county, island, statewide]  
**Resolution**: [For rasters - cell size; for vectors - scale]  
**Record Count**: [Number of features/records]  

## License and Usage

**License Type**: [e.g., Public domain, Creative Commons, restricted use]  
**Attribution Required**: [Yes/No - and specific requirements]  
**Redistribution Allowed**: [Yes/No/Conditional]  

## Quality Assessment

**Data Quality**: [Excellent/Good/Fair/Poor]  
**Known Issues**: [Any known gaps, errors, or limitations]  
**Metadata Available**: [Yes/No - link if available]  
**Last Updated by Source**: [When was the source data last updated]  

## File Location

**Saved To**: `data/00_raw/[subfolder]/[filename]`  
**File Size**: [Size in MB/GB]  

## Processing Notes

**Standardization Needed**: [Reprojection, clipping, field renaming, etc.]  
**Expected Use**: [How this data will be used in MPAT]  
**MPAT Fields Generated**: [List of fields this dataset will contribute]  

## Additional Notes

[Any other relevant information, caveats, or special considerations]
"""
    
    template_path.write_text(template_content)
    print(f"✓ Created download log template: {template_path.name}")
    print()
    print("Folder structure setup complete! Ready to begin data acquisition.")
    print()

if __name__ == "__main__":
    create_directory_structure()
