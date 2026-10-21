# Windows compliance candidate verified — 21 October 2026

**All identified mandatory redistribution requirements satisfied; Windows release
ready for final publication authorisation**, for the evaluated RC3 installer and
source-delivery arrangement documented in [COMPLIANCE.md](COMPLIANCE.md). This is
an engineering assessment, not a formal legal opinion. Publication remains on hold
by explicit owner instruction. No final v1.0.0 installer/tag or public upload exists;
version promotion, an exact final build and asset review remain normal final-release
steps in a separately authorised workflow.

## Microsoft entitlement and conditions

Owner accepted Visual Studio Community 2022 terms for the approved MIT project.
Independent `vswhere` inspection now confirms **Community 17.14.42**, installation
version 17.14.37806.7, complete/launchable/non-prerelease, no reboot required, in
`C:\Program Files\Microsoft Visual Studio\2022\Community`.
Core Editor is registered. MSBuild **17.14.60.43110** is present and successfully
ran the installed-package verification target. The optional MSBuild and VC.Redist
component-ID queries are false; their registration is not a separate Community §4
redistribution condition for the inventoried release DLLs. No paid licence, compiler
workload or runtime substitution was necessary. Earlier absent-product/security-prompt
findings are resolved; the owner handled Windows permission prompts.

All ten redistributed runtime DLL copies (five names, 14.44.35211.0) remain inventoried
with identities/signatures/importers. The owner-approved, Microsoft-only runtime
licence page was read from the actual desktop wizard. Next was disabled until
acceptance; the displayed document equals the approved build input after whitespace
normalisation. Tokentra MIT and Qt LGPL rights are expressly preserved.

## Exact installer and installed state

`release-compliance/Tokentra-1.0.0-rc.3-compliance-windows-x64-setup.exe`

- Size: **25,497,734 bytes**; unsigned, local compliance candidate.
- SHA-256: `ac6b5e9b8f97d876021c3a89ca1f7eeead2b5854274f14067216da05ff043839`.
- Launched by actual File Explorer; one approved in-place upgrade completed.
- **Windows Settings independently shows exactly one Tokentra 1.0.0-rc.3 entry**,
  publisher Ezequiel Gomez, 84.5 MB, with enabled Uninstall action.
- Installed directory: `%LOCALAPPDATA%\Programs\Tokentra`.
- All **353 payload files match** the approved build; zero mismatches.
- Installed executable and `unins000.exe` report product version 1.0.0-rc.3.
- Executable SHA-256: `0741bc3cb5169b9a8a7cdbd7d373a324798c0a3fb33d320142ff9afb9238f7a4`.
- HKCU uninstall metadata and per-user Start menu target were checked as supplemental
  evidence. They do not substitute for actual Settings visibility.
- Registered `Tokentra.Desktop` launch works. The newest candidate remains installed
  and reopened in Token Counter, blank workspace, o200k_base.

App source, AppId, geometry, worker/tokenisation logic, install directory and uninstaller
architecture are unchanged. All **51 native DLL/PYD files** equal the prior verified
payload. The previous actual desktop uninstall/reinstall cycle is retained for its
exact earlier installer; no unnecessary destructive cycle was repeated for legal-file
changes. Uninstaller presence/version/action are verified here, not a newly executed
uninstall of this package.

## Functional and offline evidence

The actual installed GUI counted synthetic `Hello world!` as **3 tokens, 2 words,
12 Unicode characters**. Context Planning retained the shared text and displayed
**128,000** capacity, **8,000** allowance, **8,003** planned allocation, **119,997**
unallocated. All digits are visible in the genuine screenshot. Original Counter
mode was restored before normal close/reopen; the workspace reopened empty, with
expected encoding/mode. No user document was imported, modified or saved. Scenario
inputs were not edited. No byte-for-byte pre-upgrade registry snapshot is claimed.

Installed empty-cache verification passed through Community MSBuild:

```powershell
& 'C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe' .verification-tmp/verify-installed.proj /nologo /v:minimal
```

The local target invokes this reproducible equivalent:

```powershell
.venv\Scripts\python.exe scripts/check_packaged.py --dist-dir "$env:LOCALAPPDATA\Programs" --report docs/compliance/offline-installed.json
```

Results: GUI startup, all three encodings (reference counts 6/8/11), encoding changes,
plain-text import, Context Planning and isolated settings passed, with empty caches,
external cwd, developer paths removed and Python socket/DNS denied.

Completed prior checks were not repeated without purpose: **121 passed in 20.91s**,
zero failures/skips; payload audit passed (353 files, 83,412,896 bytes); four native
Qt scale factors 1/1.25/1.5/2 passed; native endpoint observation had **56 samples,
zero endpoints, zero errors**. The initial sandboxed offline attempt timed out with
a temporary-directory permission error; its outside-sandbox retry passed. No failure
was concealed. No expensive benchmark was repeated: application/native counting bytes
are unchanged. Prior measured performance remains applicable within its documented scope.

Exact previous commands/results remain in the preparation source checkpoint and
machine-readable evidence. In particular:

```powershell
.venv\Scripts\python.exe -m pytest -q --basetemp .test-tmp-compliance --junitxml docs/compliance/tests.xml --tb=short
.venv\Scripts\python.exe -m PyInstaller --noconfirm --distpath dist-compliance --workpath build-compliance packaging/tokentra.spec
.venv\Scripts\python.exe scripts/audit_package.py --dist-dir dist-compliance --report docs/compliance/package-audit.json
.venv\Scripts\python.exe scripts/check_packaged.py --dist-dir dist-compliance --report docs/compliance/offline.json --native-window-checks
.venv\Scripts\python.exe scripts/observe_offline.py --executable dist-compliance/Tokentra/Tokentra.exe --report docs/compliance/native-endpoints.json
```

Genuine local desktop evidence is in `docs/compliance/desktop`: setup completion,
installed Counter/Planning, Settings entry/uninstall action and blank restart images.
`desktop-upgrade.json`, `installed-payload.json`, `setup-licence-comparison.json`,
`community-components.json` and `offline-installed.json` provide structured evidence.
No clean VM, physical network disconnection, native packet capture or macOS/Linux
verification is claimed. Endpoint sampling does not rule out transient connections.

## Licensing materials and source readiness

The actual installer includes full native/Rust notices, 16 crate notice sets (13
binary-evidenced versions), Rust 1.97.1 library attribution, approved MIT, GPL/LGPL/
Qt notices, scoped Microsoft terms and top-level Qt replacement guidance. Both full
Qt/PySide corresponding-source archives are retained at
`release-audit/third-party-sources`, with verified hashes. **They must accompany
any authorised binary download with equivalent access**, alongside the notices.
This source-delivery condition is not replaced by a homepage URL or by passing tests.

Exact libffi/xz supplier semantic versions, some inlined Rust versions, supplier
Qt configure flags and an independent modified Qt build remain documented provenance/
assurance improvements. No additional full-source/rebuild duty was identified merely
because a permissively licensed library is native. No unresolved owner licensing
choice remains for this installer. A future portable binary needs equivalent Microsoft
recipient acceptance and is not automatically approved by the setup result.

Later Python/OpenSSL/Expat advisories were assessed against deployed input paths;
a tested Python 3.12 patch refresh is recommended. No application-exploitable path
was established in that review. No vulnerability-free or formal legal certificate
is claimed.

The allowlisted source scan passes. Historical local commits with two old developer
profile-path document blobs are preserved on `main` at `4b62fdd`; a separate clean
`publication-preparation` branch avoids those historical parents. No shared history
was rewritten. Source checkpoints/archives and SHA-256 are recorded in
`release-compliance/build-manifest.json`; the earlier preparation archive is preserved.
Documentation/evidence updated after binary build is distinguished from its packaged
build-time snapshot. Final v1.0 promotion must build from its exact reviewed commit.

## Remaining conditions

- Maintain applicable Microsoft terms/eligibility and the installer acceptance page.
- Deliver the complete companion Qt/PySide sources and required notices with binaries.
- Complete final version/tag/build/asset review before an eventual public v1.0 release.
- Obtain **separate final publication authorisation**. No GitHub action was performed.

The compliance candidate is installed and verified; the earlier desktop/tooling
handoffs are closed. macOS/Linux, clean-machine and optional provenance improvements
remain clearly separated from Windows redistribution blockers.

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
