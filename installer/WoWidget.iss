#define MyAppName "WoWidget"
#define MyAppVersion "1.0.1"
#define MyAppPublisher "WoWidget"
#define MyAppExeName "WoWidget.exe"

[Setup]
AppId={{E2583329-C8D3-4F71-B0FA-EF97D68A8D85}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\WoWidget
DefaultGroupName=WoWidget
DisableProgramGroupPage=yes
UsePreviousAppDir=yes
CloseApplications=yes
RestartApplications=no
SetupLogging=yes
OutputDir=Output
OutputBaseFilename=WoWidgetSetup-{#MyAppVersion}
SetupIconFile=..\wowidget\assets\icons\wowidget.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
VersionInfoVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; \
    GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\WoWidget\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WoWidget"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\WoWidget"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch WoWidget"; \
    Flags: nowait postinstall skipifsilent
