; One maintained per-user installer definition. ISCC 6.7.3 is the tested compiler.
; Owner-approved application copyright holder; no code-signing identity is claimed.
#ifndef AppRelease
  #define AppRelease "1.0.0"
#endif
#ifndef AppNumericVersion
  #define AppNumericVersion "1.0.0.0"
#endif
#ifndef PayloadDir
  #define PayloadDir "..\dist-final\Tokentra"
#endif
#ifndef InstallerOutput
  #define InstallerOutput "..\release-final"
#endif
#ifndef InstallerBaseName
  #define InstallerBaseName "Tokentra-" + AppRelease + "-windows-x64-setup"
#endif

[Setup]
AppId={{6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6}
AppName=Tokentra
AppPublisher=Ezequiel Gomez
AppCopyright=Copyright (c) 2026 Ezequiel Gomez
AppVersion={#AppRelease}
AppVerName=Tokentra {#AppRelease}
AppComments=Precision Token Counter and offline Context Planning
VersionInfoVersion={#AppNumericVersion}
VersionInfoTextVersion={#AppRelease}
VersionInfoDescription=Tokentra Setup
DefaultDirName={localappdata}\Programs\Tokentra
DefaultGroupName=Tokentra
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.22000
WizardStyle=modern dynamic
SetupIconFile=..\app\assets\icon.ico
; Microsoft runtime recipient terms approved by the owner. The introductory
; scope preserves Tokentra MIT and third-party LGPL rights.
LicenseFile=INSTALLATION_TERMS.txt
UninstallDisplayName=Tokentra
UninstallDisplayIcon={app}\Tokentra.exe
OutputDir={#InstallerOutput}
OutputBaseFilename={#InstallerBaseName}
Compression=lzma2/normal
SolidCompression=yes
AppMutex=Local\Tokentra.Desktop.6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6
SetupMutex=Local\Tokentra.Setup.6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6
CloseApplications=no
RestartApplications=no
Uninstallable=yes
CreateUninstallRegKey=yes
UninstallLogMode=append
UsePreviousAppDir=yes
UsePreviousTasks=yes
DisableWelcomePage=no
DisableReadyPage=no
ChangesAssociations=no

[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
Source: "{#PayloadDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Tokentra"; Filename: "{app}\Tokentra.exe"; WorkingDir: "{app}"; AppUserModelID: "Tokentra.Desktop"
Name: "{autodesktop}\Tokentra"; Filename: "{app}\Tokentra.exe"; WorkingDir: "{app}"; AppUserModelID: "Tokentra.Desktop"; Tasks: desktopicon

[Run]
Filename: "{app}\Tokentra.exe"; Description: "Launch Tokentra"; Flags: nowait postinstall skipifsilent

[Code]
function LegacyWindowRunning: Boolean;
begin
  Result := FindWindowByWindowName('Tokentra | Precision Token Counter') <> 0;
end;

function InitializeSetup: Boolean;
begin
  Result := not LegacyWindowRunning;
  if not Result then
    SuppressibleMsgBox('Close Tokentra before installing or upgrading. Your unsaved text remains in its existing window.', mbInformation, MB_OK, IDOK);
end;

function InitializeUninstall: Boolean;
begin
  Result := not LegacyWindowRunning;
  if not Result then
    SuppressibleMsgBox('Close Tokentra before uninstalling. Your unsaved text remains in its existing window.', mbInformation, MB_OK, IDOK);
end;
// No recursive UninstallDelete and no preference/document deletion. Inno removes
// its tracked files/shortcuts and empty directories; unidentified files survive.
