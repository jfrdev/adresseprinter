; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{FB135B94-8672-44B6-B98D-2954F55F248D}
AppName=Adresseprinter
AppVersion=0.4
;AppVerName=Adresseprinter 0.4
AppPublisher=jfrdev
AppPublisherURL=https://github.com/jfrdev/adresseprinter/
AppSupportURL=https://github.com/jfrdev/adresseprinter/
AppUpdatesURL=https://github.com/jfrdev/adresseprinter/
DefaultDirName={pf}\Adresseprinter
DefaultGroupName=Adresseprinter
OutputBaseFilename=setup_v0.4
Compression=lzma
SolidCompression=yes

[Languages]
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "\\admcifs02\users\chw752\Documents\Dropbox\adresseprinter\build\exe.win32-3.2\wrapper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "\\admcifs02\users\chw752\Documents\Dropbox\adresseprinter\build\exe.win32-3.2\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Adresseprinter"; Filename: "{app}\wrapper.exe"
Name: "{group}\{cm:UninstallProgram,Adresseprinter}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Adresseprinter"; Filename: "{app}\wrapper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\wrapper.exe"; Description: "{cm:LaunchProgram,Adresseprinter}"; Flags: nowait postinstall skipifsilent

