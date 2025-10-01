\# ParcelAnalysis (HCPT Infrastructure Feasibility Screening)



This repository holds notebooks, Python scripts, and documentation for building the \*\*Master Parcel Attribute Table (MPAT)\*\* and running \*\*The Matrix\*\* screening for cesspool parcels in Hawaiʻi counties.



\## Contents

\- `scripts/` → Jupyter notebooks and Python utilities (MPAT assembly, wells distances, soil HAR classification)

\- `Matrix/` → screening spreadsheets and supporting docs

\- `notes\_readme/`, `Academic\_Paper/`, `validation/`, `reference/` → project notes and references



\## Not included

Large GIS datasets and outputs are \*\*not\*\* tracked in GitHub. They remain local in:

\- `data/`

\- `Outputs/`

\- `ParcelAnalysis.gdb/`



\## Workflow

1\. Build MPAT by joining TMK, wells, soils, slope, zoning, and related attributes to cesspool parcels.

2\. Run parcels through \*\*The Matrix\*\* ruleset (e.g., slope thresholds, soil infiltration class, bedroom-based sizing).

3\. Export results for planning maps and reports.



\## Environments

\- ArcGIS Pro with ArcPy for geoprocessing

\- Jupyter notebooks for orchestration and documentation

## Collaborator Quickstart

**Repo purpose.** This repo tracks the *brains* (code, notebooks, docs) for the ParcelAnalysis sub-project of HCPT. Large GIS data (file geodatabases, shapefiles, rasters) remains local and is excluded via `.gitignore`.

### Folder map
- `scripts/` – Python modules and notebooks for:
  - MPAT assembly (`mpat_development/`), exploratory previews (`exploration/`)
  - Data standardization / reprojection (`data_standardization/`)
  - Utilities (`99_Utilities/99a_Common_Functions.py`, `99b_HAR_11_62_Standards.py`)
- `Matrix/` – screening spreadsheets and documentation for “The Matrix”
- `notes_readme/`, `Academic_Paper/`, `reference/` – project docs, HAR refs, and write-ups

### Local data locations (not in Git)
Keep your GIS data adjacent to this repo, e.g.:




