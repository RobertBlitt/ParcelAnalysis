# Master Menu

The complete meal - orchestrates all notebooks

## Notebooks in this course:

- `00_Master_Hawaii_Matrix_Analysis.ipynb`

## Purpose
This is your central control notebook - like a master recipe that coordinates all the other "courses" in your workflow. Use this to:

- Set global configuration variables
- Run the complete workflow from start to finish
- Swap ingredients (data sources) and re-run specific steps
- Track overall progress

## Usage Examples

### Run Complete Workflow
```python
# Execute all notebooks in sequence
%run 01_Appetizers/01a_TMK_Foundation_Setup.ipynb
%run 02_Main_Course/02a_Soil_HAR_Classification.ipynb
%run 04_Dessert/04a_Master_Table_Assembly.ipynb
```

### Swap Data Sources
```python
# Use different soil data
soil_layer = "New_Soil_Data_2024"
%run 02_Main_Course/02a_Soil_HAR_Classification.ipynb
%run 04_Dessert/04a_Master_Table_Assembly.ipynb  # Re-assemble
```
