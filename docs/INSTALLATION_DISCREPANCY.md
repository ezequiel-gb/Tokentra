# Windows installation discrepancy investigation

21 October 2026. **Resolved on the visible Windows desktop; this is historical RC3 evidence. Final-release checks are recorded separately in RELEASE_READINESS.md.** This report supersedes earlier
claims that registry checks alone established Windows Installed Apps visibility.

## Established findings

The missing entry was reproduced in the actual Windows 11 Settings page, including
a fresh page enumeration. Earlier test reports had checked an uninstall key and
files from the command runner; they had not inspected Windows Settings. That was
an insufficient end-to-end installation check.

The retained RC3 setup log records 21 October 2026 at 14:37 (Europe/Paris),
Windows 10.0.26300 x64, non-administrative per-user mode, HKEY_CURRENT_USER,
user name Ezequiel Gomez and the normal LocalAppData installation directory.
It does not record the historical process SID, package identity or native hive
backing context. Those missing historical facts cannot be reconstructed with
certainty from the old success JSON. Current identity probes do not supply
retroactive proof of the earlier execution context.

The command runner reports DESKTOP-N7TM76M\Ezequiel Gomez, user SID ending -1002,
session 1. Full identity evidence is retained privately under installation-discrepancy.
Normal sandbox execution redirects LocalAppData into a sandbox package directory.
Approved unsandboxed commands report the normal user profile, NO_PACKAGE and the
native uninstall-key path under REGISTRY\USER\<that SID>. Settings, Explorer and
Seelen desktop processes report the same SID/session. A different account is not
established by this evidence.

Despite these matching identifiers, command-launched installation and even a
Shell.Application launch did not make Tokentra visible to the desktop inventory.
Classic Programs and Features also omitted Tokentra. A publisher-only metadata
change and reopening Settings did not fix it. These outcomes must not be reported
as proof that installation was absent or present in the desktop's registry context.

The exact same rebuilt installer was then launched by double-clicking it in the
actual File Explorer window, with owner approval. The visible wizard installed to
%LOCALAPPDATA%\Programs\Tokentra, completed successfully and
launched Tokentra. Windows Settings then visibly showed ONE Tokentra entry,
version 1.0.0-rc.3, publisher Ezequiel Gomez, 84.0 MB. Screenshot:
installation-discrepancy/settings-visible-installed.jpg.

A subsequent approved VISIBLE uninstall/reinstall cycle established the discrepancy more directly: the desktop uninstaller reported successful removal, Settings showed no Tokentra, and the executable/uninstaller disappeared, while the command runner STILL read a Tokentra uninstall key. This proves that command-side registry observations did not represent the desktop registration state.

After reinstalling again through File Explorer, Settings showed exactly ONE Tokentra entry and the app launched. This establishes a launch/execution-context discrepancy and a verified desktop installation path. The exact underlying registry isolation/brokering mechanism is
not established; native key names, SID and GetCurrentPackageFullName alone proved
insufficient to identify it. Do not invent a specific package hive or claim the
initial missing registry query has been reproduced by command-side reads.

## Changes and artefacts

- packaging/tokentra.iss: explicitly enable CreateUninstallRegKey; supply the
  already approved copyright-holder/publisher metadata. Preserve AppId, per-user
  directory, native application payload, shortcuts and uninstall architecture.
- scripts/inspect_installation_context.ps1: read-only SID/session/package/native
  registry-name evidence. Its checks are not a substitute for desktop verification.
- scripts/repair_registration.ps1: guarded command-side backup/uninstall/reinstall,
  payload hashes, shortcut, preference and unrelated-file checks. Explicitly labels
  desktop verification as separate. Never stops a user process or deletes directories.
- No app, tokeniser, worker, planning, editor, geometry or UI implementation changes.

Installer: release-registration-repair/Tokentra-1.0.0-rc.3-registration-repair-windows-x64-setup.exe
Size: 25,467,321 bytes. SHA-256:
7cb99900874d9df0eed372587fa1b5389eb48aebc518ef0788eb363c53603020
Unsigned; local evaluation only. Earlier RCs and audit packages are preserved.

## Verification

121 tests passed in 24.43s:
`python -m pytest -q --basetemp .test-tmp-registration-repair --junitxml docs/installation-discrepancy/tests.xml --tb=short`.

The command-side uninstall/reinstall completed: its uninstall key, managed files,
uninstaller and shortcuts disappeared and returned; all 295 payload hashes matched;
preferences and a synthetic unrelated file survived. This is command-context evidence,
not proof of desktop lifecycle behaviour. Registry/prefs backups and logs are retained
under .verification-tmp/registration-repair. Source files were not uninstalled/deleted.

Installed application version: 1.0.0-rc.3. Executable SHA-256:
c1fa4c93490c4d667106afd6e82c5c6d5ef28c36b6e90c84f80149f032d399fd.
Registered command-side uninstaller: the same installation directory's unins000.exe.
Frozen offline checks from an external directory with empty caches passed for all
three encodings, import, GUI startup and planning. No Python installation/API key is
needed to run the installed payload. No network-isolation claim is added by this work.

The approved visible desktop cycle PASSED:

1. File Explorer launched the exact verified installer; the visible wizard completed.
2. Settings > Apps > Installed apps showed one Tokentra 1.0.0-rc.3 entry.
3. The empty app was closed safely. The uninstaller was launched THROUGH that Settings entry.
4. Its confirmation and successful-removal dialog were observed. Settings then showed no result.
5. Physical file checks found no executable or uninstaller; only the exact synthetic unrelated
   preservation file remained in the installation directory.
6. The same installer was double-clicked in File Explorer and its visible wizard completed again.
7. Settings showed one Tokentra entry again; the application launched from setup.
8. All 295 installed payload hashes matched, PE version was 1.0.0-rc.3, both Start and
   desktop shortcuts targeted the installed executable, and unins000.exe was present.
9. The unrelated synthetic file survived and was then removed by exact path/hash, without
   recursive deletion. No source files or unrelated user files were removed.

Command-context preference values were unchanged and were backed up. The visible app retained
Token Counter and o200k_base, and setup/uninstall contains no deletion of application settings.
Because registry contexts diverge, the raw command-side preference comparison is not an
independent exhaustive desktop-registry audit. No user document was used as a test fixture.

Genuine desktop evidence (private local files):

- Before correction: installation-discrepancy/settings-before.jpg.
- First confirmed registration: installation-discrepancy/settings-visible-installed.jpg.
- Successful visible uninstall: installation-discrepancy/visible-uninstall-success.jpg.
- Entry disappeared: installation-discrepancy/settings-visible-after-uninstall.jpg.
- Reinstall completed: installation-discrepancy/visible-reinstall-success.jpg.
- Final entry returned: installation-discrepancy/settings-final-reinstalled.jpg.

Final state: the repaired local RC3 build is installed and running. Windows Settings visibly
lists exactly one entry. The registered desktop uninstaller was functionally verified by
actually invoking it through Settings, independently of command-side registry queries.

## Reproducible manual verification

1. Close Tokentra after copying any unsaved editor text. Do not clear/delete preferences.
2. In ordinary File Explorer, open release-registration-repair and double-click the
   exact installer above. Verify its checksum from the supplied SHA256SUMS first.
   Avoid using Codex's command runner as the sole installation/registration evidence.
3. Retain the existing per-user folder and complete the wizard. Check Start menu launch.
4. Open Settings > Apps > Installed apps, search Tokentra, and record the visible
   name/version/publisher. Reopen Settings if needed. Compare ordinary interactive
   PowerShell's HKCU uninstall entry, installed executable and uninstaller path.
5. Close the app; uninstall through Installed Apps, confirm the visible entry and
   managed files disappear while preferences and unrelated files remain.
6. Reinstall through File Explorer, confirm the entry returns, launch both modes,
   and leave the verified newest local candidate installed.

Expected uninstall key:
HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6}_is1
HKLM absence is expected for this per-user installer. Do not manually copy an uninstall
key from an isolated context or create duplicate machine/user registrations.

Desktop installation visibility and the visible lifecycle cycle are now verified. The exact
automation registry-isolation mechanism remains undetermined; future release checks must use
independent desktop observation. Microsoft runtime entitlement and the separate Qt/native/Rust
redistribution requirements remain open. No GitHub repository, push or release was created.
