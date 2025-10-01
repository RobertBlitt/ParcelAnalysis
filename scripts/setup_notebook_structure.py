# HAWAII CESSPOOL MATRIX ANALYSIS - NOTEBOOK WORKFLOW STRUCTURE
# Following the "Dinner Menu" organizational approach

import arcpy
import os
from datetime import datetime

# ============================================================================
# NOTEBOOK WORKFLOW ORGANIZATION
# ============================================================================

print("=== SETTING UP NOTEBOOK WORKFLOW STRUCTURE ===")

# Your paths
scripts_folder = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis\scripts"
outputs_folder = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis\Outputs"

# Create notebook structure in scripts folder
notebook_structure = {
    "00_Master_Menu": {
        "description": "The complete meal - orchestrates all notebooks",
        "files": ["00_Master_Hawaii_Matrix_Analysis.ipynb"]
    },
    "01_Appetizers": {
        "description": "Data preparation and setup",
        "files": [
            "01a_TMK_Foundation_Setup.ipynb",
            "01b_Data_Quality_Check.ipynb", 
            "01c_Workspace_Configuration.ipynb"
        ]
    },
    "02_Main_Course": {
        "description": "Core data processing recipes",
        "files": [
            "02a_Soil_HAR_Classification.ipynb",
            "02b_Slope_Analysis.ipynb",
            "02c_Distance_Calculations.ipynb",
            "02d_Regulatory_Overlays.ipynb"
        ]
    },
    "03_Side_Dishes": {
        "description": "Supporting analysis and utilities",
        "files": [
            "03a_Data_Validation.ipynb",
            "03b_Quality_Metrics.ipynb",
            "03c_Visualization_Tools.ipynb"
        ]
    },
    "04_Dessert": {
        "description": "Final assembly and outputs",
        "files": [
            "04a_Master_Table_Assembly.ipynb",
            "04b_Matrix_Technology_Analysis.ipynb",
            "04c_Results_Export.ipynb"
        ]
    },
    "99_Kitchen_Utils": {
        "description": "Reusable functions and utilities",
        "files": [
            "99a_Common_Functions.py",
            "99b_HAR_11_62_Standards.py",
            "99c_Data_Management_Utils.py"
        ]
    }
}

# Create the folder structure
for course, info in notebook_structure.items():
    course_folder = os.path.join(scripts_folder, course)
    if not os.path.exists(course_folder):
        os.makedirs(course_folder)
        print(f"✅ Created: {course}")
    
    # Create README for each course
    readme_path = os.path.join(course_folder, "README.md")
    with open(readme_path, 'w') as f:
        f.write(f"# {course.replace('_', ' ').title()}\n\n")
        f.write(f"{info['description']}\n\n")
        f.write("## Notebooks in this course:\n\n")
        for file in info['files']:
            f.write(f"- `{file}`\n")

print(f"✅ Notebook structure created in: {scripts_folder}")

# ============================================================================
# CREATE MASTER MENU NOTEBOOK TEMPLATE
# ============================================================================

master_notebook_template = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Hawaii Cesspool Matrix Analysis - Master Menu\\n",
    "\\n",
    "**Purpose**: Complete workflow for onsite wastewater technology assessment\\n",
    "**Author**: ParcelAnalysis Project\\n",
    "**Date**: ''' + datetime.now().strftime('%Y-%m-%d') + '''\\n",
    "\\n",
    "## The Complete Meal Plan\\n",
    "\\n",
    "This master notebook orchestrates the entire analysis workflow:\\n",
    "\\n",
    "### 🥗 Appetizers (Data Preparation)\\n",
    "- TMK Foundation Setup\\n",
    "- Data Quality Checks\\n",
    "- Workspace Configuration\\n",
    "\\n",
    "### 🍖 Main Course (Core Processing)\\n",
    "- Soil HAR 11-62 Classification\\n",
    "- Slope Analysis\\n",
    "- Distance Calculations\\n",
    "- Regulatory Overlays\\n",
    "\\n",
    "### 🥔 Side Dishes (Supporting Analysis)\\n",
    "- Data Validation\\n",
    "- Quality Metrics\\n",
    "- Visualization Tools\\n",
    "\\n",
    "### 🍰 Dessert (Final Assembly)\\n",
    "- Master Table Assembly\\n",
    "- Matrix Technology Analysis\\n",
    "- Results Export\\n",
    "\\n",
    "## Usage Examples\\n",
    "\\n",
    "### Run Complete Workflow\\n",
    "```python\\n",
    "# Run all courses in sequence\\n",
    "%run 01_Appetizers/01a_TMK_Foundation_Setup.ipynb\\n",
    "%run 02_Main_Course/02a_Soil_HAR_Classification.ipynb\\n",
    "# ... etc\\n",
    "```\\n",
    "\\n",
    "### Swap Ingredients (Data)\\n",
    "```python\\n",
    "# Change soil data source and re-run just the soil processing\\n",
    "soil_layer = 'NEW_Soil_Data_Layer'\\n",
    "%run 02_Main_Course/02a_Soil_HAR_Classification.ipynb\\n",
    "%run 04_Dessert/04a_Master_Table_Assembly.ipynb  # Re-assemble\\n",
    "```"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# MASTER CONFIGURATION\\n",
    "# All notebooks inherit these settings\\n",
    "\\n",
    "import arcpy\\n",
    "import os\\n",
    "from datetime import datetime\\n",
    "\\n",
    "# Project paths\\n",
    "project_folder = arcpy.mp.ArcGISProject(\\"CURRENT\\").homeFolder\\n",
    "data_folder = os.path.join(project_folder, \\"data\\")\\n",
    "outputs_folder = r\\"C:\\\\Users\\\\rober\\\\OneDrive\\\\Documents\\\\GIS_Projects\\\\ParcelAnalysis\\\\Outputs\\"\\n",
    "scripts_folder = r\\"C:\\\\Users\\\\rober\\\\OneDrive\\\\Documents\\\\GIS_Projects\\\\ParcelAnalysis\\\\scripts\\"\\n",
    "\\n",
    "# Key data layers\\n",
    "soil_layer = \\"HIstate_nrcs_join2\\"\\n",
    "municipal_wells_layer = \\"Distance to Municipal Wells\\"\\n",
    "\\n",
    "# Workflow settings\\n",
    "arcpy.env.workspace = outputs_folder\\n",
    "arcpy.env.overwriteOutput = True\\n",
    "\\n",
    "print(\\"✅ Master configuration loaded\\")\\n",
    "print(f\\"📁 Outputs: {outputs_folder}\\")\\n",
    "print(f\\"🗂️ Scripts: {scripts_folder}\\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "ArcGISPro",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}'''

# Save master notebook
master_notebook_path = os.path.join(scripts_folder, "00_Master_Menu", "00_Master_Hawaii_Matrix_Analysis.ipynb")
with open(master_notebook_path, 'w') as f:
    f.write(master_notebook_template)

print(f"✅ Master notebook created: {master_notebook_path}")

# ============================================================================
# CREATE SOIL PROCESSING NOTEBOOK TEMPLATE (Example "Recipe")
# ============================================================================

soil_notebook_template = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Soil HAR 11-62 Classification Recipe\\n",
    "\\n",
    "**Purpose**: Process soil data for Hawaii onsite wastewater regulations\\n",
    "**Inputs**: HIstate_nrcs_join2 (or configurable soil layer)\\n",
    "**Outputs**: HAR 11-62 classified soil data\\n",
    "\\n",
    "## Recipe Ingredients\\n",
    "- NRCS SSURGO soil data\\n",
    "- HAR 11-62 regulatory thresholds\\n",
    "- Matrix compatibility requirements\\n",
    "\\n",
    "## Cooking Instructions\\n",
    "1. Load and validate soil data\\n",
    "2. Calculate slope classifications (<8%, 8-12%, >12%)\\n",
    "3. Convert Ksat to percolation rates\\n",
    "4. Apply HAR 11-62 compatibility rules\\n",
    "5. Export processed layer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# CONFIGURABLE INGREDIENTS\\n",
    "# Change these to swap data sources\\n",
    "\\n",
    "# Default soil layer (can be overridden)\\n",
    "if 'soil_layer' not in globals():\\n",
    "    soil_layer = \\"HIstate_nrcs_join2\\"\\n",
    "\\n",
    "# Output naming\\n",
    "processed_soil_output = f\\"{soil_layer}_HAR_Processed\\"\\n",
    "\\n",
    "print(f\\"🥘 Cooking with soil layer: {soil_layer}\\")\\n",
    "print(f\\"📤 Output will be: {processed_soil_output}\\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "source": [
    "# SOIL PROCESSING RECIPE\\n",
    "# This cell contains the actual processing logic\\n",
    "\\n",
    "# Import common functions\\n",
    "import sys\\n",
    "sys.path.append(os.path.join(scripts_folder, '99_Kitchen_Utils'))\\n",
    "from HAR_11_62_Standards import *\\n",
    "\\n",
    "# Process the soil data\\n",
    "result = process_soil_har_classifications(\\n",
    "    input_layer=soil_layer,\\n",
    "    output_layer=processed_soil_output\\n",
    ")\\n",
    "\\n",
    "print(f\\"✅ Soil processing complete: {result}\\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "ArcGISPro",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}'''

# Save soil notebook template
soil_notebook_folder = os.path.join(scripts_folder, "02_Main_Course")
soil_notebook_path = os.path.join(soil_notebook_folder, "02a_Soil_HAR_Classification.ipynb")
with open(soil_notebook_path, 'w') as f:
    f.write(soil_notebook_template)

print(f"✅ Soil recipe notebook created: {soil_notebook_path}")

# ============================================================================
# CREATE COMMON FUNCTIONS MODULE
# ============================================================================

common_functions_template = '''# COMMON FUNCTIONS - Kitchen Utilities
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
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map_obj = aprx.activeMap
    layer_names = [layer.name for layer in map_obj.listLayers()]
    
    if layer_name not in layer_names:
        raise ValueError(f"Layer '{layer_name}' not found in map")
    return True

def create_output_path(base_folder, layer_name, suffix=""):
    """Create standardized output paths"""
    if suffix:
        output_name = f"{layer_name}_{suffix}"
    else:
        output_name = layer_name
    
    return os.path.join(base_folder, output_name + ".shp")

# Add more common functions as needed...
'''

# Save common functions
utils_folder = os.path.join(scripts_folder, "99_Kitchen_Utils")
utils_path = os.path.join(utils_folder, "99a_Common_Functions.py")
with open(utils_path, 'w') as f:
    f.write(common_functions_template)

print(f"✅ Kitchen utilities created: {utils_path}")

print(f"\n=== NOTEBOOK WORKFLOW STRUCTURE COMPLETE ===")
print(f"📚 Created modular 'dinner menu' structure")
print(f"🍽️ Each 'recipe' is swappable and reusable") 
print(f"🔄 Can easily swap data sources and re-run specific steps")
print(f"📁 All organized in: {scripts_folder}")
