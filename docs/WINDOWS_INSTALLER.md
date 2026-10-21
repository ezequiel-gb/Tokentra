# Windows installer maintenance

Windows 11 x64 is the tested target. Current application baseline: 1.0.0-rc.3.
These are local evaluation packages; public distribution is blocked (COMPLIANCE.md).
Setup is unsigned and may produce publisher/reputation warnings. Verify provenance
and SHA-256; do not disable security protection. MIT is approved for Tokentra;
the owner reports Community 2022 licence acceptance and approved Microsoft runtime terms
during setup. Final updated-installer verification and separate publication authorisation
remain required; see COMPLIANCE.md.

## Stable identity

- Inno Setup 6.7.3, packaging/tokentra.iss.
- AppId: 6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6.
- Per-user directory: %LOCALAPPDATA%\Programs\Tokentra; no administrator required.
- HKCU uninstall key: Software\Microsoft\Windows\CurrentVersion\Uninstall\{6CD1A9C2-CE1B-4EE2-BFB4-C8ED54D7C2A6}_is1.
- Start menu shortcut; optional desktop shortcut. AppUserModelID: Tokentra.Desktop.
- Display version 1.0.0-rc.3; PE version 1.0.0.3.
- Close Tokentra before upgrading/uninstalling. The mutex/legacy window guard refuses
  installation while running; it never terminates the app or discards unsaved text.
- In-place upgrades retain one registration and valid preferences. Uninstall removes
  tracked files/shortcuts; preserves preferences and unidentified files.

Do not change AppId or mutex for normal upgrades. Update all version fields together
(app/__init__.py, pyproject.toml, Windows version info, installer and macOS bundle metadata).
Keep earlier candidates. Never overwrite an unidentified installation during testing.

## Reproduce a local audit build

Install the pinned development requirements and supply Inno Setup 6.7.3 from its official
source. Its actual licence is retained; no purchase was made during this audit.
The example compiler path is local tooling, not a required installed application path.

```powershell
python scripts/collect_licences.py
python -m PyInstaller --noconfirm --distpath dist-audit --workpath build-audit packaging/tokentra.spec
python scripts/audit_package.py --dist-dir dist-audit --report package-audit.json
python scripts/check_packaged.py --dist-dir dist-audit --report offline.json --native-window-checks
python scripts/check_ui.py --executable dist-audit/Tokentra/Tokentra.exe --output ui-evidence
& .tools/InnoSetup6/ISCC.exe /Q '/DPayloadDir=..\dist-audit\Tokentra' '/DInstallerOutput=..\release-audit' '/DInstallerBaseName=Tokentra-1.0.0-rc.3-audit-windows-x64-setup' packaging/tokentra.iss
```

Notices are committed build inputs. To refresh Qt source evidence, run
scripts/download_compliance.ps1, then fetch_compliance_sources.py and prepare_compliance.py.
Those acquisition scripts are build-time only. Prepare_compliance also expects the local
Inno compiler licence file. Review all newly obtained terms and evidence before distribution.

## Verification scope

Earlier RC2 lifecycle checks exercised install, controlled upgrade, uninstall, preservation
of preferences/unrelated sentinel, and reinstall on the development host. RC3 checks
exercised in-place upgrade, all payload hashes, one Installed Apps registration,
shortcut targets, retained preferences and registered uninstaller. These are historical
results, not fresh-machine evidence and not proof that future packages work.

For a final approved package, use a clean Windows VM without Python/development dependencies:
install; inspect Installed Apps/version/shortcuts; launch both modes; import UTF-8 text;
initialise all encodings with empty caches and the network disconnected; upgrade from the
previous candidate; verify preferences and one registration; uninstall via its registered
command; verify tracked files/shortcuts/key removal and unrelated-file preservation;
reinstall and leave the intended version installed. Never reuse a real document as a fixture.

The current environment has no configured Windows Sandbox/Hyper-V or administrator
network isolation. Final installer lifecycle/clean-machine checks must be repeated after
redistribution gates close and final metadata is selected. Existing RC3 installation is preserved.

See the release-readiness report for exact current evidence. Native diagnostics use synthetic
text and temporary INI settings; scale-factor tests are not physical display-setting changes.

## Desktop-context correction, 21 October 2026

The earlier command-side registry checks did not establish desktop registration. Use
[the installation investigation](INSTALLATION_DISCREPANCY.md) for the completed visible
File Explorer setup and Settings uninstall/reinstall evidence. The local repair installer
is `release-registration-repair/Tokentra-1.0.0-rc.3-registration-repair-windows-x64-setup.exe`.
It explicitly enables uninstall-key creation and supplies approved publisher metadata;
AppId and application version remain unchanged. Publisher metadata alone did not fix
the discrepancy. Launch context and independent Settings verification were decisive.

Do not mark Installed Apps verified solely because scripts find a registry key. In this
environment the command runner continued to see a key after a visible desktop uninstall.
Retain real desktop evidence for install, removal and return. Public redistribution is
still blocked by licensing. This is not clean-VM or macOS/Linux verification.

## Compliance candidate

The compliance build keeps AppId/version/install directory and all application code.
It adds the owner-approved Microsoft runtime licence page, scoped to runtime DLLs,
and top-level notices/replacement guidance plus native/Rust licence material.
Use `packaging/INSTALLATION_TERMS.txt` as the Inno LicenseFile. Do not remove the page
while bundling Microsoft runtime files. A portable package needs equivalent recipient
terms acceptance; the old archive script alone does not provide that.

The new licence collection helper is `scripts/collect_native_notices.py`; its local
HTTPS inputs and hashes are recorded in docs/compliance/native-rust-notices.json.
It reads archives without executing third-party code. Large source/toolchain archives
are retained locally, not copied into the application. Exact supplier dependency
lockfiles and independently rebuilt Qt replacements remain recommended improvements.
