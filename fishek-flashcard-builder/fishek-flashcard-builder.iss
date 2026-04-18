[Setup]
AppName=FISHEK Flashcard Builder
AppVersion=1.0.0
DefaultDirName={autopf}\FISHEK Flashcard Builder
DefaultGroupName=FISHEK
OutputDir=output
OutputBaseFilename=fishek-flashcard-builder-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\fishek-flashcard-builder\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\FISHEK Flashcard Builder"; Filename: "{app}\fishek-flashcard-builder.exe"
Name: "{commondesktop}\FISHEK Flashcard Builder"; Filename: "{app}\fishek-flashcard-builder.exe"

[Run]
Filename: "{app}\fishek-flashcard-builder.exe"; Description: "Run FISHEK Flashcard Builder"; Flags: nowait postinstall skipifsilent
