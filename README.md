# Evony Gear Optimizer v1.3.0
## Build & Distribution Guide

---

## OVERVIEW

This guide walks you through building a distributable Windows installer
for the Evony Gear Optimizer. Two main steps:

  Step 1: PyInstaller  -- bundles Python + the app into a folder
  Step 2: Inno Setup   -- wraps that folder into a Windows installer .exe

Result: a single EvonyGearOptimizer_v1.3.0_Setup.exe that anyone can
run to install the app to: C:\Evony Tools\Gear Optimizer\

---

## PREREQUISITES  (do this section once only)

1. INSTALL PYTHON
   Download from https://python.org/downloads/
   IMPORTANT: tick "Add Python to PATH" during install.
   Recommended: Python 3.11 or 3.12

2. INSTALL PYTHON PACKAGES
   Open Command Prompt and run:
     pip install flask openpyxl pywebview pyinstaller

3. INSTALL INNO SETUP
   Download from https://jrsoftware.org/isinfo.php
   Run the installer with all default options.

---

## STEP 1 - BUILD WITH PYINSTALLER

1. Open Command Prompt

2. Navigate to your evony_tool folder:
     cd C:\path\to\evony_tool

3. Run:
     pyinstaller evony_tool.spec --clean

   Wait 2-5 minutes. When done you will see:
     "Building COLLECT ... completed successfully"

4. Test immediately by double-clicking:
     dist\EvonyGearOptimizer\EvonyGearOptimizer.exe
   The optimizer window should open.

COMMON ERRORS:
  "No module named webview"  ->  pip install pywebview
  "pyinstaller not found"    ->  close and reopen Command Prompt

---

## STEP 2 - BUILD INSTALLER WITH INNO SETUP

1. Open Inno Setup Compiler (search in Start menu)
2. File -> Open -> select evony_installer.iss
3. Build -> Compile  (or press F9)
4. Your installer appears at:
     evony_tool\installer_output\EvonyGearOptimizer_v1.3.0_Setup.exe

COMMON ERRORS:
  "dist\EvonyGearOptimizer not found"  ->  complete Step 1 first

---

## WHAT THE INSTALLER DOES

Installs to:       C:\Evony Tools\Gear Optimizer\
Start Menu:        Evony Tools > Evony Gear Optimizer
Desktop shortcut:  Optional (checkbox during install)
Uninstall:         Windows Add/Remove Programs

Files in install folder:
  EvonyGearOptimizer.exe   <- launch this
  evony_data.xlsx     <- gear data (editable by user)
  settings.json            <- user preferences (auto-created)
  (many runtime files)     <- do not edit

---

## WINDOWS SMARTSCREEN WARNING

First run of unsigned installers shows:
  "Windows protected your PC"

Recipients should click "More info" then "Run anyway".
This is normal. It does not mean the app is harmful.

---

## DISTRIBUTING TO OTHERS

Share only:  EvonyGearOptimizer_v1.3.0_Setup.exe

Requirements for recipients:
  - Windows 10 or later
  - Nothing else (Python is bundled inside)

---

## RUNNING IN DEVELOPMENT (no build required)

Normal mode (embedded window):
  python app.py

Browser mode (for debugging):
  python app.py --browser

---

## RELEASING FUTURE VERSIONS

### One-time setup
Install the release script dependencies:
    py -3.11 -m pip install requests PyGithub

The first time you run the script it will prompt for a GitHub Personal
Access Token and save it to token.txt (which is gitignored — never shared).

### Every release

1. Update version strings (Claude handles this):
     templates/index.html     (2 places)
     app.py                   (APP_VERSION constant + window title)
     evony_installer.iss      (AppVersion + OutputBaseFilename)
     README.md                (title + changelog)

2. Build with PyInstaller:
     py -3.11 -m PyInstaller evony_tool.spec --clean

3. Build installer with Inno Setup:
     Open evony_installer.iss → Build → Compile

4. Run the release script:
     py -3.11 github_release.py

   This script automatically:
     - Creates a GitHub Release with the correct version tag
     - Uploads the installer .exe as a downloadable asset
     - Uploads evony_data.xlsx to the main branch (for silent data sync)
     - Prints the release URL when done

### What users see
   - Installed apps check for updates every 7 days or 10 startups
   - If a newer version is found, a dialog offers to open the download page
   - evony_data.xlsx updates happen silently on every startup

## RELEASING FUTURE VERSIONS (old)

1. Update version string in:
     templates/index.html     (title tag + h1 span, two places)
     evony_installer.iss      (AppVersion and OutputBaseFilename lines)

2. Repeat Step 1 and Step 2 above.

The new installer preserves the user's existing evony_data.xlsx
and settings.json -- they are not overwritten on upgrade.

---

## TROUBLESHOOTING

App won't open after install:
  - Right-click .exe -> Run as administrator
  - Check antivirus quarantine; add exception for install folder
  - Ensure evony_data.xlsx is in same folder as .exe

"Port already in use" error:
  - Open Task Manager, find EvonyGearOptimizer.exe, End Task, retry

---

## VERSION HISTORY

  v1.3.0   Initial distribution release
  v0.9.x   Pre-release development builds
