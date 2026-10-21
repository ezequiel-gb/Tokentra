# Read-only diagnostic. A matching user SID alone does not establish a native hive.
param([string]$Report = 'docs/installation-discrepancy/context.json')
$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class TokentraContextProbe {
 [DllImport("ntdll.dll")] static extern int NtQueryKey(IntPtr key, int kind, IntPtr data, int size, out int result);
 [DllImport("kernel32.dll", CharSet=CharSet.Unicode)] static extern int GetCurrentPackageFullName(ref uint size, System.Text.StringBuilder name);
 public static string KeyName(IntPtr key) {
  int size; NtQueryKey(key,3,IntPtr.Zero,0,out size);
  IntPtr data=Marshal.AllocHGlobal(size);
  try { int status=NtQueryKey(key,3,data,size,out size); if(status<0) throw new Exception("NtQueryKey status: "+status);
   return Marshal.PtrToStringUni(IntPtr.Add(data,4),Marshal.ReadInt32(data)/2);
  } finally { Marshal.FreeHGlobal(data); }
 }
 public static string Package() {
  uint size=0; int status=GetCurrentPackageFullName(ref size,null);
  if(status==15700) return "NO_PACKAGE";
  var name=new System.Text.StringBuilder((int)size);
  status=GetCurrentPackageFullName(ref size,name);
  return status==0 ? name.ToString() : "ERROR_"+status;
 }
}
'@
$identity=[System.Security.Principal.WindowsIdentity]::GetCurrent()
$key=[Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Software\Microsoft\Windows\CurrentVersion\Uninstall')
$native=[TokentraContextProbe]::KeyName($key.Handle.DangerousGetHandle())
$entry=$key.OpenSubKey('{6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6}_is1')
$registration=$null
if($entry) {
 $registration=[ordered]@{display_name=$entry.GetValue('DisplayName');version=$entry.GetValue('DisplayVersion');
   location=$entry.GetValue('InstallLocation');uninstall=$entry.GetValue('UninstallString');
   native_key=[TokentraContextProbe]::KeyName($entry.Handle.DangerousGetHandle())}
 $entry.Dispose()
}
$key.Dispose()
$result=[ordered]@{time=[DateTimeOffset]::Now.ToString('o');computer=$env:COMPUTERNAME;
 user=$identity.Name;sid=$identity.User.Value;session=[Diagnostics.Process]::GetCurrentProcess().SessionId;
 user_profile=$env:USERPROFILE;local_appdata=[Environment]::GetFolderPath('LocalApplicationData');
 package_identity=[TokentraContextProbe]::Package();native_uninstall_hive=$native;registration=$registration;
 installed_executable=[IO.File]::Exists((Join-Path $env:LOCALAPPDATA 'Programs\Tokentra\Tokentra.exe'))}
$parent=Split-Path -Parent $Report
if($parent){New-Item -ItemType Directory -Force -Path $parent | Out-Null}
$result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $Report -Encoding utf8
$result | ConvertTo-Json -Depth 5
