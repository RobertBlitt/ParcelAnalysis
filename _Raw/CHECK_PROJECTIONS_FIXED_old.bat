@echo off
echo.
echo ================================================
echo HAWAII MATRIX PROJECT - PROJECTION CHECKER
echo ================================================
echo.

REM Change to the project directory
cd /d "C:\Users\rober\OneDrive\Documents\GIS_Projects\ParcelAnalysis"

echo Checking for ArcGIS Pro Python...

REM Try multiple possible ArcGIS Pro Python paths
set ARCGIS_PYTHON=""

if exist "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" (
    set ARCGIS_PYTHON="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"
    echo Found ArcGIS Pro Python at: %ARCGIS_PYTHON%
) else if exist "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" (
    set ARCGIS_PYTHON="C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat"
    echo Found ArcGIS Pro propy at: %ARCGIS_PYTHON%
) else (
    echo ERROR: Could not find ArcGIS Pro Python
    echo.
    echo Please make sure ArcGIS Pro is installed
    echo Or run this from ArcGIS Pro Python command prompt instead
    echo.
    pause
    exit /b 1
)

echo.
echo Running projection checker with ArcGIS Python...
echo.

REM Run the Python script
%ARCGIS_PYTHON% scripts\check_projections.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Script failed to run
    echo Error code: %ERRORLEVEL%
    echo.
)

echo.
echo Press any key to close...
pause > nul
