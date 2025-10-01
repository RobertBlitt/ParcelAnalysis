# Appetizers - Data Preparation 🥗

Data preparation and setup for the Hawaii Cesspool Matrix Analysis

## Notebooks in this course:

- **`01a_TMK_Foundation_Setup.ipynb`** - Creates TMK foundation layer from municipal wells data
- **`01b_Wells_Distance_Join.ipynb`** - Joins domestic wells distance data to foundation  
- *`01c_Data_Quality_Check.ipynb`* - (planned) Comprehensive data validation
- *`01d_Workspace_Configuration.ipynb`* - (planned) Final workspace setup

## Purpose
These are your "appetizers" - the essential preparation steps that set up everything for the main analysis. Like mise en place in cooking, these notebooks ensure all your ingredients are properly prepared and organized.

## Sequential Execution
Run in order:
1. **01a** - Creates TMK_Foundation_Master with municipal wells distances
2. **01b** - Adds domestic wells distances to complete wells setback data
3. Additional quality checks and workspace setup as needed

## Key Outputs
- **TMK_Foundation_Master.shp** - Base layer with both municipal and domestic wells distances
- Quality-checked data layers  
- Properly configured workspace and folder structure
- JOIN_LOG tracking for all subsequent data additions

## Dependencies
- Municipal Wells shapefile (already processed in 01a)
- Domestic Wells shapefile from Dr. Shuler's portal
- Access to data/gis_downloads/ folder structure
- Configured Outputs/ folder structure

## HAR 11-62 Context
The wells distance data is critical for Matrix technology assessment:
- Municipal wells: 1000-foot setback requirement
- Domestic wells: 1000-foot setback requirement  
- These setbacks determine which wastewater technologies are permissible per parcel

## Usage Notes
- Always run these before the main course
- The TMK Foundation Setup is particularly critical - it creates the skeleton for all other joins
- Wells Distance Join builds on the foundation created in 01a
- Each notebook updates the JOIN_LOG field to track processing sequence
- These notebooks create the organized folder structure in your Outputs folder

## Integration with Existing Structure
The wells join has been integrated into your existing food-metaphor structure rather than creating a separate MPAT system. This maintains consistency with your established workflow organization.
