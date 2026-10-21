# Command-runner lifecycle. Matching SID/native key names are necessary checks,
# not proof of the interactive desktop registry view. Always verify Settings separately.
param([ValidateSet('Snapshot','Uninstall','Reinstall')][string]$Phase)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$work=Join-Path $root '.verification-tmp\registration-repair'
$evidence=Join-Path $root 'docs\installation-discrepancy'
New-Item -ItemType Directory -Force -Path $work,$evidence | Out-Null
& (Join-Path $PSScriptRoot 'inspect_installation_context.ps1') -Report (Join-Path $evidence ('context-'+$Phase+'.json')) | Out-Null
$context=Get-Content -LiteralPath (Join-Path $evidence ('context-'+$Phase+'.json')) -Raw | ConvertFrom-Json
$sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value
if($context.package_identity -ne 'NO_PACKAGE' -or $context.native_uninstall_hive -ne ('\REGISTRY\USER\'+$sid+'\Software\Microsoft\Windows\CurrentVersion\Uninstall')) {throw 'Refusing a virtualized registry context'}
$install=[IO.Path]::GetFullPath((Join-Path ([Environment]::GetFolderPath('LocalApplicationData')) 'Programs\Tokentra'))
if($install -ne (Join-Path $env:USERPROFILE 'AppData\Local\Programs\Tokentra')){throw 'Unexpected installation directory'}
$exe=Join-Path $install 'Tokentra.exe'
$uninstaller=Join-Path $install 'unins000.exe'
$key='HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\{6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6}_is1'
$prefs='HKCU:\Software\Tokentra\Tokentra'
$stateFile=Join-Path $work 'lifecycle-state.json'
if(Get-Process -Name Tokentra -ErrorAction SilentlyContinue){throw 'Close Tokentra safely first; no user process will be stopped'}
function Preferences {if(Test-Path -LiteralPath $prefs){Get-ItemProperty -LiteralPath $prefs | Select-Object * -ExcludeProperty PS* | ConvertTo-Json -Compress -Depth 10}else{''}}
function RunSetup($path,$label){
 $log=Join-Path $work ($label+'.log')
 $p=Start-Process -FilePath $path -ArgumentList "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG=`"$log`"" -WindowStyle Hidden -Wait -PassThru
 if($p.ExitCode -ne 0){throw ($label+' exit code '+$p.ExitCode)}
}
if($Phase -eq 'Snapshot'){
 if(Test-Path -LiteralPath $stateFile){throw 'Existing lifecycle snapshot preserved; inspect before restarting'}
 $entry=Get-ItemProperty -LiteralPath $key
 if($entry.DisplayVersion -ne '1.0.0-rc.3' -or $entry.InstallLocation.TrimEnd('\') -ne $install){throw 'Unidentified existing installation'}
 if((Get-FileHash -LiteralPath $exe).Hash -ne '0F0DA0B1DFE21BF41E382289817B489670D516BEF0BC15902B9E6E24D04F2B0B'){throw 'Existing executable does not match retained RC3'}
 if($entry.UninstallString -ne ('"'+$uninstaller+'"')){throw 'Unexpected uninstaller command'}
 if(Test-Path -LiteralPath $prefs){reg.exe export 'HKCU\Software\Tokentra\Tokentra' (Join-Path $work 'preferences-before.reg') /y | Out-Null;if($LASTEXITCODE -ne 0){throw 'Preference backup failed'}}
 $sentinel=Join-Path $install 'tokentra-registration-preservation-check.txt'
 if(Test-Path -LiteralPath $sentinel){throw 'Do not overwrite a pre-existing sentinel'}
 [IO.File]::WriteAllText($sentinel,'Synthetic file created by the registration repair check. Must survive uninstall.')
 $state=[ordered]@{user=$context.user;sid=$sid;session=$context.session;install=$install;preferences=(Preferences);sentinel=$sentinel;sentinel_hash=(Get-FileHash -LiteralPath $sentinel).Hash;initial_exe_hash=(Get-FileHash -LiteralPath $exe).Hash;initial_version=$entry.DisplayVersion}
 $state | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $stateFile -Encoding utf8
 Write-Output 'Snapshot and preference backup complete; no uninstall performed.'
 exit
}
$state=Get-Content -LiteralPath $stateFile -Raw | ConvertFrom-Json
if($state.sid -ne $sid -or $state.install -ne $install -or $state.session -ne $context.session){throw 'Target identity/session changed'}
if((Preferences) -ne $state.preferences){throw 'Preferences changed since snapshot; inspect before continuing'}
if($Phase -eq 'Uninstall'){
 RunSetup $uninstaller 'actual-user-uninstall'
 $start=Join-Path ([Environment]::GetFolderPath('Programs')) 'Tokentra.lnk'
 $desktop=Join-Path ([Environment]::GetFolderPath('Desktop')) 'Tokentra.lnk'
 if((Test-Path -LiteralPath $key) -or (Test-Path -LiteralPath $exe) -or (Test-Path -LiteralPath $uninstaller) -or (Test-Path -LiteralPath $start) -or (Test-Path -LiteralPath $desktop)){throw 'Tracked registration/application/shortcuts remain after uninstall'}
 if((Get-FileHash -LiteralPath $state.sentinel).Hash -ne $state.sentinel_hash){throw 'Unrelated file changed'}
 if((Preferences) -ne $state.preferences){throw 'Uninstall changed preferences'}
 [ordered]@{phase='uninstalled';registry_absent=$true;exe_absent=$true;uninstaller_absent=$true;shortcuts_absent=$true;preferences_preserved=$true;unrelated_file_preserved=$true;settings_ui='Requires separate direct observation'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidence 'uninstall.json') -Encoding utf8
 Write-Output 'Command-context uninstall complete; registry/executable/uninstaller/shortcuts removed; preferences and sentinel preserved. Desktop verification is separate.'
}else{
 if((Test-Path -LiteralPath $key) -or (Test-Path -LiteralPath $exe)){throw 'Expected the confirmed uninstalled state'}
 $setup=Join-Path $root 'release-registration-repair\Tokentra-1.0.0-rc.3-registration-repair-windows-x64-setup.exe'
 RunSetup $setup 'actual-user-reinstall'
 $entry=Get-ItemProperty -LiteralPath $key
 if($entry.DisplayVersion -ne '1.0.0-rc.3' -or $entry.Publisher -ne 'Ezequiel Gomez' -or $entry.UninstallString -ne ('"'+$uninstaller+'"') -or -not(Test-Path -LiteralPath $uninstaller)){throw 'Reinstalled registration invalid'}
 $payload=Join-Path $root 'dist-release-audit-clean\Tokentra';$verified=0
 foreach($file in Get-ChildItem -LiteralPath $payload -Recurse -File){$relative=$file.FullName.Substring($payload.Length+1);if((Get-FileHash -LiteralPath (Join-Path $install $relative)).Hash -ne (Get-FileHash -LiteralPath $file.FullName).Hash){throw ('Installed payload mismatch: '+$relative)};$verified++}
 if((Preferences) -ne $state.preferences -or (Get-FileHash -LiteralPath $state.sentinel).Hash -ne $state.sentinel_hash){throw 'Preferences/unrelated file changed'}
 $shell=New-Object -ComObject WScript.Shell;$start=Join-Path ([Environment]::GetFolderPath('Programs')) 'Tokentra.lnk'
 if($shell.CreateShortcut($start).TargetPath -ne $exe){throw 'Start menu target mismatch'}
 $count=@(Get-ChildItem 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall' | Get-ItemProperty | Where-Object DisplayName -eq 'Tokentra').Count
 if($count -ne 1){throw 'Registration missing or duplicate'}
 [ordered]@{phase='reinstalled';user=$context.user;sid=$sid;session=$context.session;version=$entry.DisplayVersion;publisher=$entry.Publisher;install=$install;exe_sha256=(Get-FileHash -LiteralPath $exe).Hash;uninstaller=$uninstaller;registered_uninstaller=$entry.UninstallString;single_registry_entry=$true;payload_files_verified=$verified;start_shortcut_valid=$true;preferences_preserved=$true;unrelated_file_preserved=$true;settings_ui='Requires separate direct observation'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $evidence 'reinstall.json') -Encoding utf8
 # Remove only the exact synthetic file created by Snapshot, after verifying it.
 if((Resolve-Path -LiteralPath $state.sentinel).Path -ne (Join-Path $install 'tokentra-registration-preservation-check.txt')){throw 'Unexpected sentinel cleanup path'}
 Remove-Item -LiteralPath $state.sentinel
 Write-Output 'Command-context reinstall complete; all payload hashes match, registration/shortcut/uninstaller present, preferences preserved. Desktop verification is separate.'
}
