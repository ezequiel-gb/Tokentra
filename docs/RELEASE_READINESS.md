# Current compliance preparation — 21 October 2026

This section supersedes historical compliance blockers below. Feature/UI baseline
remains **1.0.0-rc.3**; no application source changed. Publication is explicitly on
hold until final validation and separate owner authorisation.

## Current findings

- Owner reports installing Visual Studio Community 2022 and accepting its terms for
  the MIT project, and approves Microsoft's unmodified runtime licence during setup.
  Community eligibility/redistribution conditions, alternatives and evidence limits
  are documented in [COMPLIANCE.md](COMPLIANCE.md). Command tooling initially cannot
  see the reported installation; exact path/component verification is pending.
- Setup now presents the approved Microsoft-only licence page. Tokentra MIT and Qt
  LGPL rights are expressly preserved. AppId, version, preferences, shortcuts,
  install directory, uninstaller architecture and all application code are unchanged.
- Added 16 crate notice sets (13 binary-evidenced versions), matching Rust 1.97.1
  library attributions, native Python dependency notices, prominent top-level notices
  and [Qt replacement/source guidance](QT_REPLACEMENT.md). Both complete Qt/PySide
  source archives are retained at `release-audit/third-party-sources`; hashes verified.
  They must accompany eventual binary downloads under GPLv3 section 6(d).
- An independent Qt rebuild and complete historical permissive dependency graph are
  recommended assurance improvements; neither is itself an identified mandatory
  licence condition. Exact libffi/xz versions and some inlined crate versions remain
  honestly unestablished. See the A/B/C/D decision matrix rather than old blanket gates.
- Current upstream security advisories were reviewed. Later Python/OpenSSL/Expat fixes
  concern functionality without an identified untrusted-input path in Tokentra.
  A tested Python 3.12 runtime refresh is recommended; no gratuitous dependency upgrade.

## New build and checks

Installer: `release-compliance/Tokentra-1.0.0-rc.3-compliance-windows-x64-setup.exe`.
Size: **25,497,734 bytes**. SHA-256:
`ac6b5e9b8f97d876021c3a89ca1f7eeead2b5854274f14067216da05ff043839`.
This is an unsigned local compliance candidate, not a published/final v1.0 installer.
Earlier RC3 and registration-repair packages are preserved.

Commands from workspace (all Python commands use `.venv/Scripts/python.exe`):

```powershell
.venv\Scripts\python.exe scripts/collect_native_notices.py
.venv\Scripts\python.exe -m pytest -q --basetemp .test-tmp-compliance --junitxml docs/compliance/tests.xml --tb=short
.venv\Scripts\python.exe -m PyInstaller --noconfirm --distpath dist-compliance --workpath build-compliance packaging/tokentra.spec
.venv\Scripts\python.exe scripts/audit_package.py --dist-dir dist-compliance --report docs/compliance/package-audit.json
.venv\Scripts\python.exe scripts/check_packaged.py --dist-dir dist-compliance --report docs/compliance/offline.json --native-window-checks
.venv\Scripts\python.exe scripts/observe_offline.py --executable dist-compliance/Tokentra/Tokentra.exe --report docs/compliance/native-endpoints.json
.venv\Scripts\python.exe scripts/prepare_compliance.py --dist-dir dist-compliance --output docs/compliance
& .tools/InnoSetup6/ISCC.exe /DPayloadDir=..\dist-compliance\Tokentra /DInstallerOutput=..\release-compliance /DInstallerBaseName=Tokentra-1.0.0-rc.3-compliance-windows-x64-setup packaging/tokentra.iss
```

**121 passed in 20.91s**, zero failures/skips. PyInstaller and Inno builds completed.
Payload audit: **353 files, 83,412,896 bytes**, no detected path/hygiene issues,
three tokeniser hashes correct, pinned Python DLL hashes correct. All **51 native
DLL/PYD files** equal the previous verified payload; application-source changes: zero.

The first packaged offline check inside the sandbox timed out after 60 seconds and
its redirected temporary-directory cleanup was denied. The same command outside
that context passed: fresh empty caches, external cwd, developer paths removed,
all three encodings, GUI startup/switching, file import, Context Planning and settings.
Native Windows transitions passed at Qt scale factors **1, 1.25, 1.5, 2**.
Endpoint observer: **56 samples, zero observed TCP/UDP endpoints, zero errors**.
This is not physical disconnection, packet capture, a clean VM or proof against
transient native activity. No expensive million-token benchmark was repeated:
application and native counting bytes are unchanged; earlier measured evidence stands.

The previous actual desktop visible install/uninstall/reinstall remains verified
for its exact registration-repair installer. **New compliance-installer visible
upgrade/licence-page verification is pending action-time confirmation.** No new
uninstall cycle is necessary. No isolated registry-only claim substitutes for Settings.
No macOS/Linux or clean-machine validation is claimed.

The current source scan passed after replacing one literal developer profile path
with `%LOCALAPPDATA%` notation. The initial finding is retained. A high-signal scan
of 269 historical text blobs found two old copies of that path and no credential
signatures. Preserve historical local commits; prepare a separate clean initial
publication branch/current-tree archive rather than publishing those parents.

## Remaining work and release decision

- Final updated-installer visible upgrade, licence-page and actual Settings check.
- Reconcile the exact Community installation path/components where accessible;
  owner acceptance is recorded separately from independent tooling verification.
- Preserve companion Qt source assets and notices when preparing a final tagged build.
- Separate final publication authorisation remains withheld; nothing was published.

Current recommendation: **Remaining owner action required** for the visible verification
and separate publication step. No paid licensing route or new application feature is
required. This is not an unconditional legal-compliance certificate. See COMPLIANCE.md
for conditions and source obligations, and release-compliance/build-manifest.json
for the exact candidate identity.

---

# Historical evidence (superseded where the current assessment differs)

# Installation verification correction

See [the current Windows installation investigation](INSTALLATION_DISCREPANCY.md).
Earlier registry-only claims did not prove Settings visibility. The rebuilt installer
was run through File Explorer; the visible Settings uninstall/reinstall cycle passed.
Exactly one entry is present and the repaired RC3 remains installed. Command-side registry
reads diverged from desktop state even with matching SID/native key names. The investigation
report supersedes the historical installation status below. Publication remains blocked by
the separate licensing requirements.

# Tokentra final release audit — blocked

21 October 2026. **Windows release blocked by specific unresolved requirements.**
No public repository, release, asset upload or push was performed. No final v1.0.0
installer/tag is approved. The owner's explicit instruction is to keep publication
blocked because Microsoft runtime redistribution entitlement cannot be confirmed.

## Application and changes

Approved feature/UI baseline: **1.0.0-rc.3** (Python 1.0.0rc3; Windows 1.0.0.3).
Windows 11 x64 build 26300; Python 3.12.14; PySide6/Qt 6.12.0; tiktoken 0.14.0;
PyInstaller 6.22.3; Inno Setup 6.7.3. Core app, geometry, workers, tokenisation and
Context Planning were preserved; no feature or visual redesign was introduced.

- Added approved MIT LICENSE: Copyright (c) 2026 Ezequiel Gomez; metadata records MIT.
- Expanded dependency inventory, GPL/LGPL/Qt/PySide/Inno notices and retained exact
  upstream source archive provenance. Added COMPLIANCE.md, PUBLICATION.md and release notes.
- Fixed real build-host contamination: RC3 Analysis resolved OpenSSL from Poppler
  and UCRT from another tool on PATH. The spec pins OpenSSL/libffi to Python's DLLs,
  removes copied Windows system UCRT/API-set libraries, and omits unused Mesa,
  optional codecs/SVG/Direct2D and translations. Final payload hashes match Python's DLLs.
- Included Tokentra's licence, notices and compliance status in the frozen distribution.
- Added focused payload assertions and endpoint observation, benchmark output selection,
  source allowlisting and Git attributes preserving exact tokeniser-table bytes.
- Finalised README, real screenshots, installation/uninstallation and publication-gate docs.
- Preserved earlier packages/reports and the existing installed RC3. The prior RC3
  report is retained locally at rc3/RELEASE_READINESS.md.

Build code checkpoint: `10fe92d9dd1fb3b4f69b58541e15b858ff40402e` in the curated local
Git repository `.publication/Tokentra`. Subsequent evidence/docs-only commits are recorded
in `release-audit/build-manifest.json` at the workspace root. No release tag exists.
The workspace originally had no Git repository, branches, tags or history.

## Tests and functional verification

Commands executed from the workspace (Python executable: .venv/Scripts/python.exe):

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .test-tmp-release-audit --junitxml docs/release-audit/tests.xml --tb=short
.venv\Scripts\python.exe -m pytest -q --basetemp .test-tmp-release-audit-final --junitxml docs/release-audit/tests-final.xml --tb=short
```

Results: **121 passed in 14.42s**, then **121 passed in 16.57s** after changes;
zero failed/skipped. From `.publication/Tokentra`, the same venv interpreter ran:
`-m pytest -q --basetemp ../../.test-tmp-curated-release --junitxml ../../docs/release-audit/tests-curated.xml --tb=short`
→ **121 passed in 18.52s**. Existing coverage includes all encodings, Unicode code
points, imports/errors, worker failures/stale results, planning/validation, settings,
geometry and contextual help. No valid tests were weakened.

```powershell
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --distpath dist-release-audit --workpath build-release-audit packaging/tokentra.spec
.venv\Scripts\python.exe -m PyInstaller --noconfirm --distpath dist-release-audit-clean --workpath build-release-audit-clean .publication/Tokentra/packaging/tokentra.spec
.venv\Scripts\python.exe scripts/audit_package.py --dist-dir dist-release-audit-clean --report docs/release-audit/package-audit-clean.json
.venv\Scripts\python.exe scripts/check_packaged.py --dist-dir dist-release-audit-clean --report docs/release-audit/offline-clean.json --native-window-checks
.venv\Scripts\python.exe scripts/check_ui.py --executable dist-release-audit-clean/Tokentra/Tokentra.exe --output docs/release-audit/ui-clean
.venv\Scripts\python.exe scripts/observe_offline.py --executable dist-release-audit-clean/Tokentra/Tokentra.exe --report docs/release-audit/native-endpoints.json
```

Both builds completed. The initial payload audit detected upstream test fixtures in
collected notice material (retained in package-audit.json). Collection was corrected;
the clean payload audit passed with **295 files, 82,815,786 bytes**, GUI subsystem,
three verified encodings, no detected workspace paths/unwanted modules, required notices,
and matching supplier OpenSSL/libffi. Standard PyInstaller optional/other-platform
missing-import warnings remain in the private build log; checks did not conceal them.
This is not a complete vulnerability audit.

Native Windows geometry and UI diagnostics passed at **QT_SCALE_FACTOR 1, 1.25,
1.5 and 2**, for the exact final audit payload. UI diagnostics checked 25 numeric
layouts per scale (1,000 through 10,000,000 at five logical sizes), footer removal,
keyboard tooltip presentation/containment/dismissal, shared editor/result and planning
layout. Genuine widget screenshots are under release-audit/ui-clean. Token Counter
and Context Planning screenshots were inspected; 128,000 is fully visible. The
1120x820 planning dashboard had no scroll overflow. These are Qt scale-factor/logical
resize tests, not physical Windows display-setting changes or monitor disconnection.

## Performance

`python scripts/benchmark_representative.py --report docs/release-audit/benchmark.json`
completed six warm-encoding, whole-string mixed prose/Python/multilingual Unicode/CRLF
cases on this host. No token chunking was used.

| Encoding | Tokens near 100k / seconds | Tokens near 1m / seconds | 1m editor load / end edit | 1m sampled RSS |
|---|---|---|---|---|
| o200k_base | 99,968 / 0.023 | 1,000,000 / 0.309 | 0.280s / 0.898s | 180.5 MiB |
| cl100k_base | 100,035 / 0.023 | 999,970 / 0.240 | 0.161s / 0.662s | 193.7 MiB |
| p50k_base | 100,748 / 0.016 | 1,007,747 / 0.233 | 0.102s / 0.516s | 194.9 MiB |

Million-token inputs: 3,937,500 / 2,652,552 / 1,968,624 code points respectively;
UTF-8 sizes 5,125,000 / 3,452,528 / 2,562,336 bytes. Maximum GUI heartbeat gaps during
worker counting were 22.3 / 20.8 / 26.6 ms. Cumulative process peak working set reached
262.8 MiB across the sequence; sampled RSS is not an exact per-operation peak. Offscreen
Qt heartbeat timing does not prove physical interaction latency. Editor operations can
pause even when background token counting remains responsive. No universal size or
latency guarantee is made; Count file avoids editor layout overhead but still uses RAM.

## Offline evidence

All supported encodings, GUI startup/selection, strict file import and planning passed
in the frozen executable from an external temporary directory, with empty tokenizer
cache paths, Python paths removed and PATH restricted to Windows system directories.
A Python audit hook denied socket connections/DNS. Independent process/child TCP/UDP
endpoint sampling during the synthetic offline diagnostic recorded **55 samples, zero
observed endpoints, zero inspection errors**. Transient activity can evade sampling.

No configured clean VM, Windows Sandbox/Hyper-V or administrator network isolation was
available. No packet-capture/firewall-enforced or physically disconnected test was done.
This verifies cache-independent local assets and no observed diagnostic connections;
it does not prove all native process activity is absent in every workflow. No telemetry,
API connection or automatic document persistence was added; diagnostics use synthetic
text and isolated preferences.

## Windows installer and installed state

Compiled local audit installer (not cleared for distribution):
`release-audit/Tokentra-1.0.0-rc.3-audit-windows-x64-setup.exe`

- Size: **25,467,288 bytes**.
- SHA-256: `4d2726d1b441a1b4d94e1a9fcb511acdd29945d3894c9b623d54dbd012e864b2`.
- Compiled with the established Inno definition, stable AppId, per-user directory,
  shortcuts, running-app guard and uninstall architecture unchanged. Payload includes
  the notice tree and MIT licence; compile success alone is not installation verification.
- **Not installed/upgraded/uninstalled this audit.** Its new lifecycle validation remains
  pending. It is an audit build, not a final installer. No unnecessary uninstall cycle
  was performed against the existing user installation.
- Read-only current-host inspection confirms installed **1.0.0-rc.3**, one registration,
  valid Start menu target and registered uninstaller. Executable SHA-256:
  `0f0da0b1dfe21bf41e382289817b489670d516bef0bc15902b9e6e24d04f2b0b`.
- Previous RC2 lifecycle and RC3 upgrade tests are retained historical evidence, not a
  new audit-installer test. No fresh Windows VM test was performed. Unsigned status remains.

Compilation command used the curated packaging/tokentra.iss with absolute local
PayloadDir=dist-release-audit-clean/Tokentra, InstallerOutput=release-audit and
InstallerBaseName=Tokentra-1.0.0-rc.3-audit-windows-x64-setup via ISCC /Q.
Source archive, retained upstream archives and SHA256SUMS are local preparation inputs;
the external build manifest records their hashes and Git source references.

## Licensing and repository readiness

See [COMPLIANCE.md](COMPLIANCE.md), [third-party inventory](../THIRD_PARTY_NOTICES.md)
and release-audit/dependency-inventory.json. MIT is approved. Qt community LGPLv3 is
selected, not commercially licensed. Official wheel comparison: 228 PySide and 12
Shiboken native files matched. Qt/PySide source archives and 94 upstream attribution
records are retained, with GPL/LGPL and component notices included in the package.
Corresponding-source/build mapping and replacement validation remain open; external
DLL packaging by itself is not sufficient.

The curated local Git tree excludes caches, venv, binaries, tools, private historical
logs and pasted attachments. Targeted high-signal credential/private-key/local-user-path
scan reported no findings; it is not an exhaustive security certification. No prior Git
history existed to rewrite. Only new local preparation commits were created; final
Git status/source archive identity is recorded in build-manifest.json. No remote or
release tag was created. GitHub read-only inspection found no owned Tokentra repository.

## Remaining requirements

**Release blockers:** owner-confirmed applicable Microsoft redistribution basis or
reviewed alternative; complete native/Rust dependency provenance/notices; Qt matching
source/build delivery and replacement/installation-information validation; final metadata,
exact release tag/build reference and applicable final installer/security tests. All are
still prerequisites; a passing test suite does not close them.

**Non-blocking limitations:** unsigned warnings; very large editor pauses; physical
DPI/monitor hot-plug, accessibility and complete native-network isolation validation
not established here. No claim of clean-machine installation.

**Future platform work:** build and validate macOS signing/notarisation and Linux
packages/desktop environments. No macOS/Linux binaries were produced or described as verified.

Keep publication blocked. Resolve and document the mandatory gates, then build and test
an actual v1.0.0 package from a reviewed release commit before tagging or publishing.
