# Tokentra 1.0.0 Windows release verification

21 October 2026. **Final technical gates passed; public delivery authorised.**
The exact build source is `f85d47441192e0b7960435774e039572f50b155f`. Tag `v1.0.0` must
identify that commit. This evidence-only documentation commit advances main without
changing build inputs or the release tag. The source checkpoint's pending-check
statement records its build-time state; this report supplies the subsequent results.

## Final installer and desktop

- `Tokentra-1.0.0-windows-x64-setup.exe`: **25,491,664 bytes**, unsigned.
- SHA-256: `550347a1275c6c89793003326dab7f924a4067eaf9dddf3cbb7bcb91c4514e93`.
- Controlled RC3→1.0.0 upgrade through actual File Explorer completed. Scoped
  Microsoft terms matched the approved input; Next required acceptance.
- Actual **Windows Settings shows one Tokentra 1.0.0 entry**, publisher Ezequiel
  Gomez, and enabled Uninstall. Start menu AppId launch works.
- All **353 installed payload files match**, zero differences. Installed executable
  and present uninstaller report 1.0.0. Stable AppId and per-user directory retained.
- Original o200k_base/Counter mode and 128,000/8,000 scenario retained. Both modes
  passed the synthetic Hello world! check: 3 tokens, 2 words, 12 characters;
  planned 8,003 and unallocated 119,997. Restart opened a blank workspace.
- Command-runner registry observations still report RC3 in their isolated context.
  They are not desktop-registration evidence. The actual Settings view is authoritative
  here; the previously documented isolation mechanism remains unidentified.
- No new uninstall cycle was needed; historical actual desktop RC3 uninstall/reinstall
  evidence is retained for its exact package. No clean-machine claim is made.

See [build manifest](release-v1/build-manifest.json) and
[desktop evidence summary](release-v1/desktop-upgrade.json). Raw private desktop
captures remain local and are excluded from publication.

## Tests and package checks

From the exact clean build source, the full suite returned **121 passed in 15.55s**,
zero failures/skips. Exact command (working directory: curated source repository):

```powershell
../../.venv/Scripts/python.exe -m pytest -q --basetemp ../../.test-tmp-v1-release --junitxml ../../.verification-tmp/v1-tests.xml --tb=short
```

Build command: `../../.venv/Scripts/python.exe -m PyInstaller --noconfirm --distpath ../../dist-final --workpath ../../build-final packaging/tokentra.spec`.
Inno Setup 6.7.3 compiled that payload using `packaging/tokentra.iss` with absolute
PayloadDir/InstallerOutput overrides to the local final directories.

The following commands used the workspace development interpreter and curated scripts:

```powershell
.venv/Scripts/python.exe .publication/Tokentra/scripts/audit_package.py --dist-dir dist-final --report .verification-tmp/v1-package-audit.json
.venv/Scripts/python.exe .publication/Tokentra/scripts/check_packaged.py --dist-dir dist-final --report .verification-tmp/v1-offline.json --native-window-checks
.venv/Scripts/python.exe .publication/Tokentra/scripts/observe_offline.py --executable dist-final/Tokentra/Tokentra.exe --report .verification-tmp/v1-native-endpoints.json
.venv/Scripts/python.exe .publication/Tokentra/scripts/check_packaged.py --dist-dir "$env:LOCALAPPDATA/Programs" --report .verification-tmp/v1-installed-offline.json
```

Payload audit passed: 353 files, 83,414,702 bytes, GUI subsystem, 203 frozen modules,
202 module filenames checked, zero source-path leaks/issues, Python supplier DLLs
matched. **All 51 native DLL/PYD files equal RC3**, and all ten Microsoft runtime
copies match their approved inventory. Required notice trees and BPE hashes pass.
Empty-cache packaged and installed checks passed all encodings (6/8/11 reference
tokens), GUI startup, encoding switching, plain-text import and planning, outside
source with developer search paths removed and Python socket/DNS access denied.
Native window diagnostics passed Qt scale factors **1, 1.25, 1.5 and 2**.
Native process/child endpoint observation: **56 samples, zero endpoints/errors**.

## Source, licensing and limits

The clean build lineage has three commits and 400 tracked files. High-signal scanning
of 382 text blobs across its full history found no credential/private-key patterns or
developer-profile paths. Private historical branches are retained locally and excluded.
This is not a comprehensive security certification.

MIT retains Copyright (c) 2026 Ezequiel Gomez. Community entitlement, Microsoft-only
recipient acceptance, native/Rust attribution and LGPL replacement/source arrangements
are documented in COMPLIANCE.md. Both complete QtBase/PySide 6.12.0 archives must
be public companion assets alongside the installer; hashes are in QT_REPLACEMENT.md.
No portable binary is published. This is an engineering assessment, not legal certification.

No counting/UI/worker/geometry changes were made. Existing million-token benchmark
evidence remains applicable within its documented machine/input-specific scope.
No clean VM, physical network disconnection, packet capture, OS scaling changes or
multi-monitor exercise is claimed. macOS/Linux binaries remain future unverified work.
Unsigned-install warnings and large-editor layout pauses remain documented limitations.
