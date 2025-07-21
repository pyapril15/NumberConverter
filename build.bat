@echo off
echo ============================================
echo   Professional Number System Converter
echo              Build Script v2.0
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python 3.7 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available!
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

echo Installing/Updating dependencies...
echo This may take a few minutes for first-time installation...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies!
    echo Please check your internet connection and try again.
    echo.
    echo Trying to install core dependencies individually...
    pip install pyinstaller>=5.13.0

    if errorlevel 1 (
        echo Error: Could not install PyInstaller!
        pause
        exit /b 1
    )
)

echo.
echo Dependencies installed successfully!
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo Error: main.py not found!
    echo Please ensure you are running this script from the project directory.
    echo Current directory: %cd%
    echo.
    pause
    exit /b 1
)

REM Create assets directory structure if it doesn't exist
if not exist "assets" (
    echo Creating assets directory structure...
    mkdir assets
    mkdir assets\icon
    echo Please place your conversion.ico file in assets\icon\ directory
    echo.
)

if not exist "assets\icon" mkdir assets\icon

REM Check for icon file
if not exist "assets\icon\conversion.ico" (
    echo Warning: Icon file not found at assets\icon\conversion.ico
    echo The executable will be built without a custom icon.
    echo You can add the icon file later and rebuild.
    echo.
)

REM Test the application before building
echo Testing the application...
python -c "import main; print('Application import test: OK')"
if errorlevel 1 (
    echo Error: Application failed import test!
    echo Please check for syntax errors in main.py
    echo.
    pause
    exit /b 1
)

echo Application test passed!
echo.

echo Cleaning previous build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "Professional_Number_Converter.spec" del "Professional_Number_Converter.spec"
echo.

echo ============================================
echo     Building Number System Converter
echo ============================================
echo.
echo This process will:
echo • Create a standalone executable (.exe)
echo • Include all dependencies
echo • Optimize for performance
echo • Create distribution files
echo.
echo Please wait... This may take 3-7 minutes
echo.

REM Build using Python setup script
python setup.py
if errorlevel 1 (
    echo.
    echo Error: Build failed!
    echo Trying alternative build method...
    echo.

    REM Alternative build using direct PyInstaller command
    pyinstaller --onefile ^
                --windowed ^
                --name=Professional_Number_Converter ^
                --icon=assets/icon/conversion.ico ^
                --distpath=dist ^
                --workpath=build ^
                --clean ^
                --noconfirm ^
                --optimize=2 ^
                --noupx ^
                --hidden-import=tkinter ^
                --hidden-import=tkinter.ttk ^
                --hidden-import=tkinter.messagebox ^
                --hidden-import=tkinter.filedialog ^
                --hidden-import=tkinter.scrolledtext ^
                --hidden-import=struct ^
                --hidden-import=math ^
                --hidden-import=json ^
                --hidden-import=csv ^
                --hidden-import=datetime ^
                main.py

    if errorlevel 1 (
        echo.
        echo Error: Both build methods failed!
        echo Please check the error messages above and try the following:
        echo 1. Ensure all dependencies are installed correctly
        echo 2. Check that main.py has no syntax errors
        echo 3. Verify that PyInstaller is properly installed
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo           Build Completed Successfully!
echo ============================================
echo.

REM Check if executable was created
if not exist "dist\Professional_Number_Converter.exe" (
    echo Error: Executable was not created!
    echo Please check the build logs above for errors.
    echo.
    pause
    exit /b 1
)

REM Get file size
for %%A in ("dist\Professional_Number_Converter.exe") do set SIZE=%%~zA
set /a SIZE_MB=%SIZE%/1024/1024

echo Build Summary:
echo • Executable: dist\Professional_Number_Converter.exe
echo • File size: %SIZE_MB% MB
echo • Build date: %date% %time%
echo.

echo Distribution files created:
if exist "dist\README_DIST.txt" echo • README_DIST.txt - User documentation
if exist "dist\LICENSE.txt" echo • LICENSE.txt - License information
if exist "dist\install.bat" echo • install.bat - Optional installer script
echo.

REM Ask if user wants to test the executable
set /p test="Test the executable now? (y/n): "
if /i "%test%"=="y" (
    echo Launching Professional Number System Converter for testing...
    echo The application should start in a few seconds...
    echo Close it when you're satisfied with the test.
    echo.
    start "" "dist\Professional_Number_Converter.exe"

    REM Wait a moment then check if it's running
    timeout /t 3 /nobreak >nul
    tasklist /FI "IMAGENAME eq Professional_Number_Converter.exe" 2>NUL | find /I /N "Professional_Number_Converter.exe">NUL
    if errorlevel 1 (
        echo Warning: Application may not have started correctly.
        echo Please manually test the executable in the dist folder.
    ) else (
        echo ✓ Application started successfully!
    )
    echo.
)

REM Ask about cleanup
set /p cleanup="Clean up build files? (y/n): "
if /i "%cleanup%"=="y" (
    echo Cleaning up temporary build files...
    if exist "build" rmdir /s /q "build"
    if exist "Professional_Number_Converter.spec" del "Professional_Number_Converter.spec"
    if exist "__pycache__" rmdir /s /q "__pycache__"
    echo Cleanup completed.
    echo.
)

echo ============================================
echo            Build Process Complete!
echo ============================================
echo.
echo Your Professional Number System Converter is ready!
echo.
echo 📁 Location: %cd%\dist\Professional_Number_Converter.exe
echo 💾 Size: %SIZE_MB% MB
echo 🎯 Status: Ready for distribution
echo.
echo Distribution Options:
echo 1. Share the 'dist' folder containing all files
echo 2. Use the install.bat script for automatic installation
echo 3. Simply share the .exe file for portable use
echo.
echo Features included in your build:
echo ✓ Multi-base number conversion (2-36 bases)
echo ✓ Batch conversion capabilities
echo ✓ Multi-base calculator
echo ✓ IEEE 754 floating point converter
echo ✓ Programming tools (Two's complement, bitwise ops)
echo ✓ Educational number systems guide
echo ✓ Conversion history tracking
echo ✓ Professional user interface
echo.
echo Next Steps:
echo • Test the executable thoroughly
echo • Share with users or students
echo • Gather feedback for improvements
echo • Consider code signing for wider distribution
echo.

REM Create a simple batch file to run the application
echo @echo off > "Run_Number_Converter.bat"
echo cd /d "%~dp0" >> "Run_Number_Converter.bat"
echo start "" "dist\Professional_Number_Converter.exe" >> "Run_Number_Converter.bat"

echo Created Run_Number_Converter.bat for easy launching.
echo.

echo Thank you for using the Professional Number System Converter build system!
echo.
echo Press any key to exit...
pause >nul