# Kitchen Utils - Reusable Functions

Reusable functions and utilities

## Files in this course:

- `99a_Common_Functions.py`
- `99b_HAR_11_62_Standards.py`
- `99c_Data_Management_Utils.py`

## Purpose
These are your "kitchen utilities" - the essential tools, functions, and standards that all other notebooks use. Like having a well-stocked kitchen with sharp knives and quality ingredients, these utilities make everything else work better.

## Key Modules

### 99a_Common_Functions.py
**General-purpose GIS and workflow functions**
- `log_workflow_step()`: Timestamp and track processing steps
- `validate_layer_exists()`: Check if layers are available
- `create_output_path()`: Standardized file naming
- `print_layer_summary()`: Quick data inspection
- `calculate_completeness_stats()`: Data quality assessment

### 99b_HAR_11_62_Standards.py
**Hawaii wastewater regulation compliance**
- **Constants**: All HAR 11-62 thresholds and requirements
- **Conversion Functions**: Ksat to percolation rate, classification functions
- **Compatibility Checks**: Technology suitability assessment
- **Validation Functions**: Ensure regulatory compliance

**Key Constants:**
```python
SLOPE_THRESHOLDS = {
    'ABSORPTION_BEDS': 8.0,      # Max 8% slope
    'ABSORPTION_TRENCHES': 12.0,  # Max 12% slope
}

PERCOLATION_LIMITS = {
    'TRENCHES_BEDS_MAX': 60.0,   # Max 60 min/inch
    'SEEPAGE_PITS_MAX': 10.0,    # Max 10 min/inch
}
```

### 99c_Data_Management_Utils.py (Future)
**Planned utilities for data management**
- Backup and versioning functions
- Data export utilities
- Report generation tools

## Usage in Notebooks
```python
# Import common functions
import sys
sys.path.append(os.path.join(scripts_folder, '99_Kitchen_Utils'))
from Common_Functions import *
from HAR_11_62_Standards import *

# Use in your processing
log_workflow_step("Processing", "Starting soil classification")
perc_rate = ksat_to_percolation_rate(ksat_value)
compatible = check_septic_compatibility(slope, perc, drainage)
```

## Benefits
- **Consistency**: Same standards across all notebooks
- **Reusability**: Write once, use everywhere
- **Maintainability**: Update standards in one place
- **Regulatory Compliance**: Built-in HAR 11-62 requirements
- **Quality Assurance**: Standardized validation functions

## Adding New Functions
When you develop useful functions, add them to the appropriate module:
- General GIS operations → `99a_Common_Functions.py`
- Regulatory compliance → `99b_HAR_11_62_Standards.py` 
- Data management → `99c_Data_Management_Utils.py`
