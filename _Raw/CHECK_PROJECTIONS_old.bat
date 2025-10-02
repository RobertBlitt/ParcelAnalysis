@echo off
echo.
echo ================================================
echo HAWAII MATRIX PROJECT - PROJECTION CHECKER
echo ================================================
echo.
echo This will check all GIS data in your downloads
echo and automatically fix any projection issues
echo.
pause

REM Change to the project directory
cd /d "C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"

REM Run the Python script using ArcGIS Pro's Python
"C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" scripts\check_projections.py

echo.
echo Script finished!
pause
