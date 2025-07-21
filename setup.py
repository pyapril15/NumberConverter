"""
Setup script for building the Professional Number System Converter executable
Author: Praveen Yadav
Version: 2.0.0
"""

import os
import shutil
import sys

import PyInstaller.__main__


def build_executable():
    """Build the executable using PyInstaller"""

    # Application information
    APP_NAME = 'Professional_Number_Converter'
    APP_VERSION = '2.0.0'
    APP_DESCRIPTION = 'Professional Number System Converter with Advanced Features'
    APP_AUTHOR = 'Your Name'

    # Define the build arguments
    args = [
        '--onefile',  # Create a one-file bundled executable
        '--windowed',  # Hide console window (GUI app)
        '--name=' + APP_NAME,  # Name of the executable
        '--distpath=dist',  # Output directory
        '--workpath=build',  # Temporary build directory
        '--specpath=.',  # Spec file location
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without asking
        '--optimize=2',  # Optimize bytecode
        '--noupx',  # Don't use UPX compression

        # Icon (if available)
        '--icon=assets/icon/conversion.ico',

        # Hidden imports for modules PyInstaller might miss
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=struct',
        '--hidden-import=math',
        '--hidden-import=json',
        '--hidden-import=csv',
        '--hidden-import=datetime',
        '--hidden-import=os',
        '--hidden-import=re',
        '--hidden-import=typing',

        # Add data files
        '--add-data=assets;assets',

        # Main Python file
        'main.py'
    ]

    print("=" * 60)
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    print(f"Platform: {sys.platform}")
    print(f"Python version: {sys.version}")
    print()

    try:
        # Check if icon exists
        if not os.path.exists('assets/icon/conversion.ico'):
            print("Warning: Icon file not found. Building without icon.")
            # Remove icon argument
            args = [arg for arg in args if not arg.startswith('--icon=')]

        # Run PyInstaller
        print("Starting build process...")
        PyInstaller.__main__.run(args)

        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print(f"Executable location: {os.path.abspath('dist/' + APP_NAME + '.exe')}")

        # Create distribution files
        create_distribution_files(APP_NAME, APP_VERSION, APP_AUTHOR)

        print("\nDistribution files created successfully!")
        print("\nYour Professional Number System Converter is ready to distribute!")

    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)


def create_distribution_files(app_name, app_version, app_author):
    """Create additional distribution files"""

    # Create README for distribution
    dist_readme = f"""Professional Number System Converter - Distribution Package

Application: {app_name}
Version: {app_version}
Author: {app_author}
Build Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FEATURES:
✓ Multi-Base Number Conversion (2-36 bases)
✓ Advanced Conversion Algorithms
✓ Batch Conversion Capabilities
✓ Multi-Base Calculator
✓ IEEE 754 Floating Point Converter
✓ Programming Tools (Two's Complement, Bitwise Operations)
✓ Educational Number Systems Guide
✓ Conversion History Tracking
✓ Professional User Interface
✓ Export Capabilities (CSV, Text)

CONTENTS:
- {app_name}.exe         : Main application executable
- README_DIST.txt        : This file
- LICENSE.txt            : License information
- User_Guide.pdf         : Detailed user manual (if available)

SYSTEM REQUIREMENTS:
- Windows 7/8/10/11 (64-bit recommended)
- Minimum 2GB RAM
- 50MB free disk space
- No additional dependencies required

INSTALLATION:
1. Simply run {app_name}.exe
2. No installation required - portable application
3. Application will create config files automatically

FIRST TIME SETUP:
1. Launch the application
2. Go to Settings → Preferences to configure defaults
3. Explore the educational content in the Number Systems Guide tab
4. Start converting numbers between different bases

FEATURES OVERVIEW:

🔢 NUMBER CONVERTER TAB:
• Convert between 16 different number bases (2-36)
• Real-time input validation
• Detailed conversion process explanation
• Quick conversion to common bases (Binary, Octal, Decimal, Hex)
• Swap bases feature for quick reverse conversion

📊 BATCH CONVERTER TAB:
• Convert multiple numbers simultaneously
• Load numbers from files (TXT, CSV)
• Export results to files
• Progress tracking and error reporting

🧮 MULTI-BASE CALCULATOR TAB:
• Perform arithmetic in different bases
• Support for Binary, Octal, Decimal, and Hexadecimal
• Memory functions and operation history
• Visual button layout adapts to current base

🔬 IEEE 754 CONVERTER TAB:
• Convert decimal numbers to IEEE 754 format
• Support for single (32-bit) and double (64-bit) precision
• Detailed breakdown of sign, exponent, and mantissa
• Binary and hexadecimal representations

💻 PROGRAMMING TOOLS TAB:
• Two's complement calculator with bit width selection
• Comprehensive bitwise operations (AND, OR, XOR, NOT)
• Bit shift operations
• Binary representation analysis

📚 NUMBER SYSTEMS GUIDE TAB:
• Interactive educational content
• Comprehensive explanations of different number systems
• Conversion methods and techniques
• Examples and practice problems

📋 HISTORY TAB:
• Automatic conversion history tracking
• Export history to CSV format
• Search and filter capabilities
• Configurable history size

🔧 ADVANCED FEATURES:
• Professional tabbed interface
• Customizable preferences and defaults
• Comprehensive help system
• Error handling and input validation
• Context-sensitive tooltips

USAGE EXAMPLES:

Basic Conversion:
1. Enter number in "Input" field
2. Select source base (From Base)
3. Select target base (To Base)
4. Click "Convert" to see results

Batch Conversion:
1. Go to "Batch Converter" tab
2. Enter multiple numbers (one per line)
3. Set source and target bases
4. Click "Convert All"

Calculator Usage:
1. Go to "Multi-Base Calculator" tab
2. Select desired base (2, 8, 10, or 16)
3. Use calculator buttons for arithmetic
4. Results shown in selected base

EDUCATIONAL CONTENT:
• Number Systems Overview
• Binary, Octal, Hexadecimal explanations
• Conversion methods and algorithms
• Computer number representation
• IEEE 754 floating point standard

SUPPORT:
For technical support or feature requests:
• Email: support@example.com
• GitHub: https://github.com/yourusername/number-converter
• Documentation: See built-in help system

COPYRIGHT:
© 2025 {app_author}. All rights reserved.
Licensed under MIT License - see LICENSE.txt for details.

DISCLAIMER:
This software is provided for educational and professional purposes.
Always verify critical calculations independently.
The software is provided "as is" without warranty of any kind.
"""

    try:
        with open('dist/README_DIST.txt', 'w') as f:
            f.write(dist_readme)
    except Exception as e:
        print(f"Warning: Could not create dist README: {e}")

    # Copy additional files to dist
    files_to_copy = [
        ('LICENSE', 'LICENSE.txt'),
        ('README.md', 'README.md'),
    ]

    for src, dst in files_to_copy:
        try:
            if os.path.exists(src):
                shutil.copy2(src, f'dist/{dst}')
        except Exception as e:
            print(f"Warning: Could not copy {src}: {e}")

    # Create a simple installer batch file
    installer_content = f"""@echo off
echo ============================================
echo   Professional Number System Converter
echo              Installer v{app_version}
echo ============================================
echo.

echo Installing Professional Number System Converter...
echo.

set INSTALL_DIR=%PROGRAMFILES%\\Professional Number Converter

echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying application files...
copy "{app_name}.exe" "%INSTALL_DIR%\\"
copy "README_DIST.txt" "%INSTALL_DIR%\\"
copy "LICENSE.txt" "%INSTALL_DIR%\\"

echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\Number System Converter.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\{app_name}.exe" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Professional Number System Converter" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo Creating start menu entry...
set START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
if not exist "%START_MENU%\\Professional Number Converter" mkdir "%START_MENU%\\Professional Number Converter"

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateStartMenu.vbs
echo sLinkFile = "%START_MENU%\\Professional Number Converter\\Number System Converter.lnk" >> CreateStartMenu.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateStartMenu.vbs
echo oLink.TargetPath = "%INSTALL_DIR%\\{app_name}.exe" >> CreateStartMenu.vbs
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> CreateStartMenu.vbs
echo oLink.Description = "Professional Number System Converter" >> CreateStartMenu.vbs
echo oLink.Save >> CreateStartMenu.vbs
cscript CreateStartMenu.vbs
del CreateStartMenu.vbs

echo.
echo ============================================
echo     Installation Completed Successfully!
echo ============================================
echo.
echo Professional Number System Converter has been installed to:
echo %INSTALL_DIR%
echo.
echo Shortcuts created:
echo • Desktop shortcut
echo • Start Menu entry
echo.
echo You can now launch the application from:
echo 1. Desktop shortcut
echo 2. Start Menu → Professional Number Converter
echo 3. Direct execution from: %INSTALL_DIR%
echo.

set /p launch="Launch Number System Converter now? (y/n): "
if /i "%launch%"=="y" (
    echo Launching Professional Number System Converter...
    start "" "%INSTALL_DIR%\\{app_name}.exe"
)

echo.
echo Thank you for using Professional Number System Converter!
echo.
pause
"""

    try:
        with open('dist/install.bat', 'w') as f:
            f.write(installer_content)
        print("Installer script created: dist/install.bat")
    except Exception as e:
        print(f"Warning: Could not create installer script: {e}")


def clean_build_files():
    """Clean up build files"""
    dirs_to_remove = ['build', '__pycache__']
    files_to_remove = ['Professional_Number_Converter.spec']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Cleaned up: {dir_name}")
            except Exception as e:
                print(f"Warning: Could not remove {dir_name}: {e}")

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"Cleaned up: {file_name}")
            except Exception as e:
                print(f"Warning: Could not remove {file_name}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Build Professional Number System Converter executable')
    parser.add_argument('--clean', action='store_true', help='Clean build files after building')
    parser.add_argument('--test', action='store_true', help='Test the built executable')

    args = parser.parse_args()

    # Check if required files exist
    if not os.path.exists('main.py'):
        print("Error: main.py not found!")
        print("Please ensure you are running this script from the project directory.")
        sys.exit(1)

    # Check for assets directory
    if not os.path.exists('assets'):
        print("Warning: assets directory not found. Creating assets structure...")
        os.makedirs('assets/icon', exist_ok=True)
        print("Please place your conversion.ico file in assets/icon/ directory")

    # Build the executable
    build_executable()

    # Test the executable if requested
    if args.test:
        print("\nTesting the executable...")
        try:
            import subprocess

            exe_path = 'dist/Professional_Number_Converter.exe'
            if os.path.exists(exe_path):
                print(f"Launching {exe_path} for testing...")
                subprocess.Popen([exe_path])
                print("Executable launched successfully!")
            else:
                print("Error: Executable not found for testing.")
        except Exception as e:
            print(f"Error testing executable: {e}")

    # Clean up if requested
    if args.clean:
        print("\nCleaning up build files...")
        clean_build_files()

    print("\n" + "=" * 60)
    print("Build process completed!")
    print("=" * 60)
    print("\nFiles created in 'dist' directory:")
    print("• Professional_Number_Converter.exe - Main application")
    print("• README_DIST.txt - User documentation")
    print("• LICENSE.txt - License information")
    print("• install.bat - Optional installer script")
    print("\nYour Professional Number System Converter is ready for distribution!")
