# HAWAII MATRIX PROJECT - AUTO PROJECTION MONITOR
# This PowerShell script watches for new files in gis_downloads folders
# and automatically runs the projection checker when new files are added

# Set up paths
$ProjectPath = "C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"
$WatchPath = "$ProjectPath\data\gis_downloads"
$ScriptPath = "$ProjectPath\scripts\check_projections.py"
$BatchPath = "$ProjectPath\CHECK_PROJECTIONS.bat"

Write-Host "=" * 60
Write-Host "HAWAII MATRIX PROJECT - AUTO FILE MONITOR"
Write-Host "=" * 60
Write-Host "Watching folder: $WatchPath"
Write-Host "When you add new .shp files, projection checker will run automatically"
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring"
Write-Host "=" * 60

# Create file system watcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $WatchPath
$watcher.IncludeSubdirectories = $true
$watcher.Filter = "*.shp"
$watcher.EnableRaisingEvents = $true

# Define what happens when a new file is detected
$action = {
    $path = $Event.SourceEventArgs.FullPath
    $name = $Event.SourceEventArgs.Name
    $changeType = $Event.SourceEventArgs.ChangeType
    
    if ($changeType -eq "Created") {
        Write-Host ""
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] NEW SHAPEFILE DETECTED: $name"
        Write-Host "Waiting 2 seconds for file to finish copying..."
        Start-Sleep -Seconds 2
        
        Write-Host "Running projection checker..."
        
        # Run the projection checker
        try {
            & $BatchPath
            Write-Host "✅ Projection check complete!"
        }
        catch {
            Write-Host "❌ Error running projection checker: $($_.Exception.Message)"
        }
        
        Write-Host ""
        Write-Host "Continuing to monitor for new files..."
        Write-Host "=" * 40
    }
}

# Register the event
Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action $action

try {
    # Keep the script running
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    # Clean up
    $watcher.Dispose()
    Write-Host "File monitoring stopped."
}
