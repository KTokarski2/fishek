[Setup]
AppName=FISHEK Desktop
AppVersion=1.0.0
DefaultDirName={autopf}\FISHEK
DefaultGroupName=FISHEK
OutputDir=output
OutputBaseFilename=fishek-setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\fishek\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\FISHEK Desktop"; Filename: "{app}\fishek.exe"; IconFilename: "{app}\_internal\assets\icon.ico"
Name: "{commondesktop}\FISHEK Desktop"; Filename: "{app}\fishek.exe"; IconFilename: "{app}\_internal\assets\icon.ico"

[Run]
Filename: "{app}\fishek.exe"; Description: "Run FISHEK Desktop"; Flags: nowait postinstall skipifsilent