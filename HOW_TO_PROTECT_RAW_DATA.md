# How to Properly Protect 00_raw Folder

## Method 1: PowerShell (Recommended - Actually Works)

Open PowerShell and run this to make all files in 00_raw truly read-only:

```powershell
# Navigate to your project
cd "C:\GIS_Projects\ParcelAnalysis"

# Make all files in 00_raw and subdirectories read-only
Get-ChildItem -Path "data\00_raw" -Recurse -File | ForEach-Object {
    Set-ItemProperty -Path $_.FullName -Name IsReadOnly -Value $true
}

Write-Host "All files in 00_raw are now read-only"
```

### To verify it worked:
```powershell
# Check status of files
Get-ChildItem -Path "data\00_raw" -Recurse -File | Select-Object Name, IsReadOnly | Format-Table
```

### To undo if needed (make files writable again):
```powershell
Get-ChildItem -Path "data\00_raw" -Recurse -File | ForEach-Object {
    Set-ItemProperty -Path $_.FullName -Name IsReadOnly -Value $false
}
```

---

## Method 2: Windows Security Permissions (Most Restrictive)

This actually prevents modifications at the permissions level:

1. Right-click `data\00_raw` folder
2. Properties → Security tab
3. Click "Edit" → Select your username
4. **Uncheck "Write"** permission (keep "Read" and "List folder contents")
5. Check "Replace all child object permissions"
6. Apply → Yes to warning → OK

**Warning**: This is more restrictive - you won't be able to add new files to 00_raw without changing permissions back.

---

## Method 3: Simple File-by-File (As You Download)

After downloading each dataset:

1. Right-click the file (not the folder)
2. Properties → General tab
3. Check "Read-only" attribute
4. OK

This protects individual files without restricting the folder.

---

## Recommended Approach for This Project:

**Use Method 1 (PowerShell)** because:
- ✓ Actually works (unlike folder checkbox)
- ✓ Applies to all files recursively
- ✓ Easy to undo if you need to add more data
- ✓ Doesn't prevent adding new files to 00_raw
- ✓ Only prevents editing/deleting existing files
- ✓ Scripts can still read the files

**Run this after you download your first batch of data** (not on empty folders).

---

## What About Other Folders?

**Leave them as-is!** The checkmarks you see on other folders are harmless:

- `01_interim/` - Need to be writable (working files)
- `02_processed/` - Need to be writable (outputs)
- `scripts/` - Need to be writable (editing code)
- `configs/` - Need to be writable (paths.yaml)
- `outputs/` - Need to be writable (maps, reports)

**Don't set these to read-only** - you need to write to them constantly.

---

## Testing If 00_raw Is Actually Protected:

After applying Method 1, test it:

```powershell
# Try to create a test file (should succeed - folder not protected)
New-Item -Path "data\00_raw\test.txt" -ItemType File -Force
Write-Output "Test content" | Out-File "data\00_raw\test.txt"

# Try to modify it (should fail - file is protected)
Write-Output "Modified" | Out-File "data\00_raw\test.txt"
# You should see an error: "Access to the path is denied"

# Clean up
Remove-Item "data\00_raw\test.txt" -Force
# This will also fail because file is read-only - need to unprotect first
```

---

## Summary:

**What you noticed**: Folders showing "read-only" checkbox  
**What it means**: Basically nothing for folders  
**What to do**: Ignore it for most folders  
**For 00_raw specifically**: Use PowerShell Method 1 after downloading data  
**Why**: Protects source files from accidental edits while allowing new additions

---

**The bottom line**: Don't worry about those checkmarks on other folders. They're a Windows UI quirk that doesn't actually protect anything. For `00_raw`, use the PowerShell script above once you have data in there.
