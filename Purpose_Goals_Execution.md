Purpose. Develop a parcel-level technology suitability and screening framework that determines feasible wastewater replacement options for parcels with cesspools, consistent with Hawaiʻi administrative rules and local environmental constraints. The framework produces parcel diagnostics for owners and an adjustable, scenario-based planning view for policymakers and agencies.



Planning framing.



* Objective: Maximize compliant, cost-aware, and environmentally protective cesspool conversions by 2050.
* 
* Decision units: Individual parcels that contain a cesspool (TMK keyed).
* 
* Attributes: Parcel characteristics relevant to wastewater siting and performance, for example slope, soils/infiltration class, distances to wells and shorelines, groundwater depth, zoning, SMA, etc.
* 
* Constraints: Regulatory thresholds and siting criteria derived from HAR 11-62 and related guidance.
* 
* Criteria and rules: A codified rule set (your “Matrix”) that maps parcel attributes to technology eligibility and required performance level.
* 
* Scenarios: Adjustable policy levers and sensitivity tests, e.g., changing setback distances, slope thresholds, or performance standards to evaluate aggregate outcomes.
* 
* Outputs: Parcel-level suitability classifications with justifications, plus summary statistics and interactive maps for owner and planner audiences.



This is a multi-criteria, rule-based suitability analysis at parcel scale, implemented as a reproducible geospatial workflow with scenario capability.





How this vision guides our repo and code



Think in layers. Each layer is swappable and testable.



Data Ingestion and Standardization



Purpose: bring raw layers into a consistent CRS, schema, and tiling by county.



Inputs: parcels, cesspool points or joins, wells, soils, slope/elevation, shoreline, zoning, SMA, surface water, etc.



Outputs: standardized layers and a Master Parcel Attribute Table (MPAT) keyed by TMK.



Reuse principle: generalize loaders and reprojection utilities so any planning problem can register its own input layers and attribute recipes.



Attribute Engineering (MPAT assembly)



Purpose: compute and join all parcel attributes required by the rules engine, for example distance bands, slope area ratios by threshold, soils classes, groundwater flags.



Output: a wide table with one row per cesspool parcel and columns for every criterion.



Reuse principle: express each attribute as a function with a clear signature f(gis\_paths, params) -> pd.Series or FC and register it in a catalog.



Rules Engine (“Matrix”)



Purpose: a transparent, auditable translation of HAR 11-62 and planning considerations into code.



Implementation: tabular rules plus Python evaluators that map MPAT columns to eligibility, required treatment level, and notes.



Reuse principle: keep rules in a data-driven table or YAML so different jurisdictions or updated regulations can be swapped without rewriting code.



Scenario Management



Purpose: run the rules under different parameter sets and document impacts.



Implementation: small scenario configs (YAML or CSV) that set thresholds and weights.



Outputs: parcel results, deltas from baseline, county and region summaries, and sensitivity plots.



Reuse principle: a single scenario runner accepts any config and produces a standard results package.





Validation and QA



Unit tests for attribute functions and sample rules.



Spot checks and cross-tabs for expected relationships, for example parcels near wells should up-screen to higher treatment.



Logging of data sources, dates, and footprints.



Reporting and Export



Owner-facing extracts: parcel popups with constraint diagnostics and recommended tech classes.



Planner-facing aggregates: counts by tech class, cost ranges, maps.



Export formats: CSV for MPAT and results, FGDB feature classes for GIS, lightweight GeoJSON for web.



Web Map Integration (later step)



Public app: fixed thresholds, clear parcel diagnostics.



Planner app: thresholds as sliders or inputs, scenario compare, and batch summaries.

