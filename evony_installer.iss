; Evony Gear Optimizer - Inno Setup Script
; Version 1.3.0
;
; HOW TO USE:
;   1. Download and install Inno Setup from https://jrsoftware.org/isinfo.php
;   2. Open Inno Setup Compiler
;   3. File -> Open -> select this file (evony_installer.iss)
;   4. Build -> Compile
;   5. The installer .exe will appear in the installer_output\ folder
;
; PREREQUISITES:
;   - PyInstaller build must be complete first
;   - dist\EvonyGearOptimizer\ folder must exist alongside this script

#define AppName "Evony Gear Optimizer"
#define AppVersion "1.3.0"
#define AppPublisher "Evony Tools"
#define AppExeName "EvonyGearOptimizer.exe"
#define InstallDir "C:\Evony Tools\Gear Optimizer"

[Setup]
AppId={{A3F7C2D1-8E4B-4F9A-B6C3-D2E1F0A9B8C7}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={#InstallDir}
DefaultGroupName=Evony Tools
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=EvonyGearOptimizer_v1.3.0_Setup
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableDirPage=no
DisableProgramGroupPage=yes
PrivilegesRequired=admin
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
; Minimum Windows 10
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &Desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Main application — everything bundled by PyInstaller
Source: "dist\EvonyGearOptimizer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; App icon
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Data file sourced directly from the project folder (not from dist).
; onlyifdoesntexist preserves any edits the user has made on upgrade.
; uninsneveruninstall means uninstalling the app won't delete their data file.
Source: "evony_data.xlsx"; DestDir: "{app}"; Flags: onlyifdoesntexist uninsneveruninstall

[Icons]
; Start Menu shortcut
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
; Desktop shortcut (optional, user must tick the box)
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Offer to launch the app after install
Filename: "{app}\{#AppExeName}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove settings.json on uninstall (optional — comment out to preserve user settings)
Type: files; Name: "{app}\settings.json"


