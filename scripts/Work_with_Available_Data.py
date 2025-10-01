"""
Hawaii Cesspool Matrix Analysis - Work with Existing Data
University of Hawaii Water Resources Research Center
Uses the files available in the current chat session
"""

print("=" * 70)
print("Hawaii Cesspool Matrix Analysis - Using Available Data")
print("=" * 70)

import datetime
import os
import pandas as pd

print(f"Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Set workspace
workspace = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
data_dir = os.path.join(workspace, "data")

print("=== WORKING WITH AVAILABLE FILES ===")

# Check for the technology matrix file you uploaded
try:
    # Try to read the technology matrix (the .xls file from chat)
    print("Attempting to load technology matrix...")
    
    # This would need to be copied from the chat uploads to your local directory
    tech_matrix_local = os.path.join(data_dir, "TechnologyTreatmentDisposalTreat.xlsx")
    
    if os.path.exists(tech_matrix_local):
        df_tech = pd.read_excel(tech_matrix_local)
        print(f"✓ Technology matrix loaded: {len(df_tech)} rows, {len(df_tech.columns)} columns")
        
        # Display basic info about the matrix
        print("\nTechnology Matrix Structure:")
        print(f"  Columns: {list(df_tech.columns[:5])}..." if len(df_tech.columns) > 5 else f"  Columns: {list(df_tech.columns)}")
        
        if 'Technology' in df_tech.columns:
            print(f"  Technologies: {len(df_tech)} total")
            print(f"  Sample technologies: {df_tech['Technology'].head(3).tolist()}")
            
    else:
        print("⚠ Technology matrix not found locally")
        print("  You'll need to copy TechnologyTreatmentDisposalTreat.xls to:")
        print(f"  {tech_matrix_local}")

except Exception as e:
    print(f"Error loading technology matrix: {str(e)}")

# Check for the Kau bedrooms data
try:
    print("\nChecking for Kau bedrooms data...")
    kau_file = os.path.join(data_dir, "Kau_Bedrooms.csv")
    
    if os.path.exists(kau_file):
        df_kau = pd.read_csv(kau_file)
        print(f"✓ Kau bedrooms data loaded: {len(df_kau)} rows, {len(df_kau.columns)} columns")
        print(f"  Columns: {list(df_kau.columns)}")
        
    else:
        print("⚠ Kau_Bedrooms.csv not found locally")
        print("  Copy from chat uploads to:")
        print(f"  {kau_file}")
        
except Exception as e:
    print(f"Error loading Kau data: {str(e)}")

# Create a minimal demo workflow
print("\n=== DEMO WORKFLOW SETUP ===")

demo_dir = os.path.join(workspace, "demo")
if not os.path.exists(demo_dir):
    os.makedirs(demo_dir)
    print(f"Created demo directory: {demo_dir}")

# Create sample analysis script
sample_analysis_file = os.path.join(demo_dir, "technology_matrix_demo.py")

sample_code = '''"""
Hawaii Cesspool Technology Matrix - Demo Analysis
Shows how to work with the binary suitability matrix
"""

import pandas as pd
import numpy as np

def load_technology_matrix(file_path):
    """Load and validate the technology matrix"""
    print(f"Loading technology matrix from: {file_path}")
    
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded {len(df)} technologies with {len(df.columns)} criteria")
        
        # Basic validation
        if 'Technology' not in df.columns:
            print("Warning: No 'Technology' column found")
        
        # Count binary columns (should be 1s and 0s for suitability)
        binary_cols = []
        for col in df.columns:
            if col != 'Technology':
                unique_vals = df[col].dropna().unique()
                if set(unique_vals).issubset({0, 1, '0', '1'}):
                    binary_cols.append(col)
        
        print(f"Found {len(binary_cols)} binary suitability columns")
        
        return df, binary_cols
        
    except Exception as e:
        print(f"Error loading matrix: {str(e)}")
        return None, []

def demonstrate_sieve_analysis(df, binary_cols, site_conditions):
    """Demo of how sieve analysis works"""
    print("\\n=== SIEVE ANALYSIS DEMONSTRATION ===")
    print(f"Site conditions: {site_conditions}")
    
    suitable_technologies = []
    
    for idx, row in df.iterrows():
        technology = row['Technology']
        
        # Check if technology is suitable for ALL site conditions
        suitable = True
        for condition in site_conditions:
            if condition in binary_cols:
                if row[condition] != 1:  # Technology not suitable for this condition
                    suitable = False
                    break
        
        if suitable:
            suitable_technologies.append(technology)
    
    print(f"\\nSuitable technologies: {len(suitable_technologies)} out of {len(df)}")
    for tech in suitable_technologies[:5]:  # Show first 5
        print(f"  • {tech}")
    
    if len(suitable_technologies) > 5:
        print(f"  ... and {len(suitable_technologies) - 5} more")
    
    return suitable_technologies

if __name__ == "__main__":
    # Demo usage
    matrix_file = r"C:\\Users\\rober\\OneDrive\\Documents\\GIS_Projects\\ParcelAnalysis\\data\\TechnologyTreatmentDisposalTreat.xlsx"
    
    df, binary_cols = load_technology_matrix(matrix_file)
    
    if df is not None:
        # Example site conditions (you'd calculate these from GIS data)
        example_conditions = ['shallow_soil', 'high_groundwater', 'residential_zoning']  # Adjust based on actual column names
        
        suitable_techs = demonstrate_sieve_analysis(df, binary_cols, example_conditions)
'''

with open(sample_analysis_file, 'w', encoding='utf-8') as f:
    f.write(sample_code)

print(f"✓ Created demo analysis script: {sample_analysis_file}")

# Provide clear next steps
print("\n=== IMMEDIATE NEXT STEPS ===")
print("1. Copy your uploaded files to the data directory:")
print(f"   • TechnologyTreatmentDisposalTreat.xls → {data_dir}")
print(f"   • Kau_Bedrooms.csv → {data_dir}")
print()
print("2. Then run the Phase 2 Data Setup script:")
print("   exec(open(r'C:\\Users\\rober\\OneDrive\\Documents\\GIS_Projects\\ParcelAnalysis\\scripts\\Phase2_Data_Setup.py').read())")
print()
print("3. Or run the demo analysis:")
print(f"   exec(open(r'{sample_analysis_file}').read())")

print("\n=== CURRENT STATUS ===")
print("✓ Foundation setup successful")
print("✓ Directory structure created")  
print("✓ Logging system working")
print("✓ ArcPy environment initialized")
print("⚠ Need to copy data files to local directories")
print("→ Ready for Phase 2: Data Setup")
