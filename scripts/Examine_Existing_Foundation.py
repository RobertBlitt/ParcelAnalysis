"""
Hawaii Cesspool Matrix Analysis - Examine Existing Foundation Table
University of Hawaii Water Resources Research Center
Analyzes the existing TMK_Foundation_Master.shp to determine if it's useful
"""

import arcpy
import os

print("=" * 70)
print("Examining Existing TMK Foundation Table")
print("=" * 70)

# Set path to existing foundation file
workspace = r"C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
foundation_path = os.path.join(workspace, "Outputs", "TMK_Foundation", "TMK_Foundation_Master.shp")

print(f"Examining: {foundation_path}")

if arcpy.Exists(foundation_path):
    print("✅ Foundation file exists")
    
    # Get basic info
    record_count = int(arcpy.management.GetCount(foundation_path)[0])
    print(f"📊 Record count: {record_count:,}")
    
    # List all fields with details
    print("\n🔍 ALL FIELDS IN TABLE:")
    print("-" * 50)
    
    fields = arcpy.ListFields(foundation_path)
    useful_fields = []
    confusing_fields = []
    
    for i, field in enumerate(fields, 1):
        field_info = f"{i:2d}. {field.name:<15} ({field.type:<10}) {field.length if field.length else ''}"
        
        # Categorize fields as useful or confusing
        field_name_lower = field.name.lower()
        
        if any(keyword in field_name_lower for keyword in ['tmk', 'island', 'county', 'dist', 'municipal', 'domestic', 'well']):
            useful_fields.append(field.name)
            print(f"✅ {field_info}")
        elif any(keyword in field_name_lower for keyword in ['soil', 'slope', 'perc', 'drain', 'septic', 'atu', 'seepage', 'join_log']):
            useful_fields.append(field.name)
            print(f"🎯 {field_info} <- Matrix field")
        elif field.name in ['FID', 'Shape']:
            print(f"⚪ {field_info} <- System field")
        else:
            confusing_fields.append(field.name)
            print(f"❓ {field_info} <- Unclear purpose")
    
    # Summary analysis
    print(f"\n📋 FIELD ANALYSIS SUMMARY:")
    print(f"   Total fields: {len(fields)}")
    print(f"   ✅ Clearly useful: {len(useful_fields)}")
    print(f"   ❓ Unclear/confusing: {len(confusing_fields)}")
    
    if confusing_fields:
        print(f"\n❓ CONFUSING FIELDS:")
        for field in confusing_fields:
            print(f"   - {field}")
    
    # Sample some data to see what's populated
    print(f"\n📋 SAMPLE DATA (first 3 records):")
    print("-" * 50)
    
    # Get key fields for sampling
    sample_fields = ['TMK', 'Island']
    
    # Add distance fields if they exist
    for field in fields:
        if 'dist' in field.name.lower() and field.name not in sample_fields:
            sample_fields.append(field.name)
            if len(sample_fields) >= 5:  # Limit to 5 fields for readability
                break
    
    # Add tracking fields if they exist
    tracking_fields = ['SOIL_JOIN', 'JOIN_LOG', 'PERC_CLASS']
    for field in tracking_fields:
        if field in [f.name for f in fields] and field not in sample_fields:
            sample_fields.append(field)
            if len(sample_fields) >= 8:  # Don't show too many
                break
    
    print(f"Showing fields: {sample_fields}")
    print()
    
    with arcpy.da.SearchCursor(foundation_path, sample_fields) as cursor:
        for i, row in enumerate(cursor):
            if i < 3:  # Show first 3 records
                record_display = []
                for j, value in enumerate(row):
                    field_name = sample_fields[j]
                    # Truncate long values for display
                    display_value = str(value)[:30] if value else "NULL"
                    record_display.append(f"{field_name}: {display_value}")
                
                print(f"Record {i+1}: {' | '.join(record_display)}")
            if i >= 2:
                break
    
    # Recommendation
    print(f"\n🎯 RECOMMENDATION:")
    
    if len(confusing_fields) > 5:
        print("❌ This table has too many confusing/unclear fields")
        print("💡 SUGGEST: Start fresh with our clean Step 1 approach")
        print("   - Create new master table with only needed fields")
        print("   - Clear field names and purposes")
        print("   - Better documentation")
        
    elif len(useful_fields) >= 8:
        print("✅ This table has good foundation fields")
        print("💡 SUGGEST: Clean up and use this table")
        print("   - Remove confusing fields if possible")
        print("   - Proceed with Step 2 (soil processing)")
        print("   - Add any missing Matrix fields as needed")
        
    else:
        print("⚪ This table is partially useful but incomplete")
        print("💡 SUGGEST: Evaluate case-by-case")
        print("   - Option A: Clean and enhance this table") 
        print("   - Option B: Start fresh with Step 1")
    
    print(f"\n📝 NEXT STEPS:")
    print("1. Review the field list above")
    print("2. Decide: Clean this table OR start fresh")
    print("3. Let me know your preference")
    print("4. Proceed with soil processing")

else:
    print("❌ Foundation file not found")
    print("💡 Need to run Step 1 to create foundation table")

print(f"\n" + "=" * 70)
