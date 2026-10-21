# Redistribution assessment — Windows candidate verified; publication held

21 October 2026; functional baseline **1.0.0-rc.3**. Publication remains on hold by
owner instruction. This engineering assessment is not a formal legal opinion.
It supersedes earlier blanket requirements for an independent Qt rebuild and
complete historical native build reconstruction.

Classification: **A** mandatory licence/contract requirement; **B** engineering
verification; **C** conservative recommendation; **D** unresolved interpretation.
A recommended engineering test is not independently a legal obligation.

## Decision matrix

| Component or issue | Applicable requirement | Evidence | Current status | Required action | Release blocker? |
|---|---|---|---|---|---|
| Tokentra | A: MIT notice and licence | Owner approval; root LICENSE | Resolved | Retain Copyright (c) 2026 Ezequiel Gomez | No |
| Microsoft developer entitlement | A: Community 2022 §§1,4 and redistribution list | Owner licence acceptance; independently verified Community 17.14.42, complete/launchable; MSBuild usable | Resolved subject to documented conditions | Retain MIT eligibility and Community/redistribution conditions | No identified entitlement gap remains |
| Microsoft recipients | A: Community §4(b) protective terms; §4(c) restrictions | Approved scoped licence page observed in actual desktop wizard; Next disabled until acceptance; installed text matches approved input | Resolved | Preserve scoped acceptance in every installer | No; setup acceptance verified |
| Qt/PySide/Shiboken | A: LGPLv3 §4(a,b,d1), GPLv3 §6 | External shared libraries; full notices; official wheel identity; complete source archives | Resolved subject to documented conditions | Deliver both source archives beside eventual binaries with equivalent access | Source delivery is a release condition |
| Independent modified Qt build | B/C: replacement assurance | Dynamic build metadata; external files; no Qt hash/signature gate | Additional verification recommended | Optional independent build/replacement exercise | No clause requires performing a full rebuild |
| Exact supplier Qt flags | B; A if necessary custom build scripts/patches are missing | Complete upstream sources contain build scripts; no Tokentra patches; official wheel bytes match | Additional verification recommended | Retain supplier flags if obtained; do not claim independent reproducibility | No missing custom script/patch identified |
| Rust notices | A: MIT/Apache/Unicode/incorporated-code notices | 13 binary-evidenced crate versions; 16 notice sets; matching Rust library attribution | Resolved subject to documented conditions | Include notices in new payload | No complete historical lockfile obligation identified |
| Python native notices | A: PSF/historical, Apache, MIT, BSD/bzip2 | Actual versions/hashes; supplied Python licence; supplemental notices | Resolved subject to documented conditions | Retain all original and supplemental notices | No complete source archive obligation identified |
| libffi/xz exact versions | B/C: provenance precision | ABI 8 and static liblzma; no supplier manifest; applicable licence families documented | Additional verification recommended | Obtain supplier manifest on runtime refresh; do not assign upstream default pins to custom binaries | No: MIT/public-domain/0BSD do not require full build histories |
| Security | B: deployed attack-surface review | Advisory review below; plain-text input; fixed tokeniser regexes; no online service | Resolved subject to documented conditions | Recheck advisories before publication | No exploitable application input path established in this review |
| Desktop installation | B: actual Settings visibility and lifecycle | New exact-installer desktop upgrade, one Settings entry, 353 matching files, restart and installed offline check; previous visible uninstall/reinstall retained | Resolved | Retain exact evidence; repeat applicable checks after future binary changes | No; no unnecessary new uninstall cycle |
| Publication | Owner instruction | Explicit hold in current request | Unresolved mandatory requirement | Separate final publication authorisation after gates pass | Yes; no public action in this pass |

## Microsoft runtime: files and no-cost deployment options

The audited payload has **10 copies, five filenames**, all **14.44.35211.0**:
VCRUNTIME140.dll, VCRUNTIME140_1.dll, MSVCP140.dll, MSVCP140_1.dll, MSVCP140_2.dll.
`docs/compliance/microsoft-runtime.json` records paths, SHA-256 and PE importers.
All signatures are valid (`microsoft-signatures.json`). Root VCRUNTIME copies come
from the Python runtime; others match official PySide/Shiboken wheels. Some copies
carry Qt's valid signature. Identical version numbers do not imply identical hashes.
Python/native modules, tiktoken, regex, Qt, PySide and Shiboken require these files.
Windows UCRT/API-set libraries and ICU are OS-supplied and are not redistributed.

**Option A — selected, no cost.** [Community 2022 terms](https://visualstudio.microsoft.com/license-terms/vs2022-ga-community/)
§1(a) permits individuals working on their own applications, including sale.
§1(b) separately permits organisational development under OSI-approved licences;
Tokentra's approved MIT project qualifies. The non-open-source organisational
fallback has five-user/non-enterprise limits; an enterprise has over 250 PCs/users
or over US$1m annual revenue. This project uses the MIT route. Owner reports
Community installed and applicable terms accepted. No commercial licence was purchased.

Community §4(a) permits listed object code in applications developed by the licensee.
§4(b) requires significant primary functionality and protective recipient terms.
§4(c) restricts prerelease Microsoft code, misleading branding and imposing excluded
source/modification terms on Microsoft code. Tokentra adds substantial functionality;
its RC label does not make the release Microsoft runtime files prerelease code.
The [redistribution list](https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution)
includes these runtime families for validly licensed Visual Studio users including
Community, subject to terms. A DLL in a wheel alone is not proof of entitlement.

Owner approved Microsoft's unmodified [runtime licence](https://visualstudio.microsoft.com/license-terms/vs2022-cruntime/)
for setup acceptance. `packaging/MICROSOFT_RUNTIME_TERMS.txt` retains it;
`INSTALLATION_TERMS.txt` explains that it applies only to Microsoft files, preserving
Tokentra MIT and Qt LGPL rights. Keep the page in setup and installed materials.
Any future portable distribution also needs appropriate recipient acceptance;
this pass does not approve publishing a portable archive.

**Option B — fallback.** Users can obtain and install Microsoft's official x64
redistributable themselves. Its licence grants installation/use, not unrestricted
redistribution by Tokentra. Bundling that installer still needs developer entitlement.
A separate user-installed prerequisite avoids conveying Microsoft files only if all
app-local runtime copies are removed. Operation stays offline; installation requires
a preinstalled runtime or separately obtained offline prerequisite.

**Option C — alternative deployment.** A shared-runtime prerequisite variant would
need prerequisite/version handling and clean-machine testing; it was not built here.
It is unnecessary if the selected Community route is completed. Replacing Python/Qt
or compilers would be disproportionate. The [Build Tools terms](https://visualstudio.microsoft.com/license-terms/vs2022-ga-diagnosticbuildtools/)
§1(d) permit certain open-source dependency builds without a Visual Studio licence,
but that is not itself Community §4 redistribution permission.

The owner completed Community 2022 installation and accepted its terms. A new
`vswhere` probe independently confirms **17.14.42**, installation version
17.14.37806.7, complete/launchable/non-prerelease, no reboot required, at the
supplied standard Community directory. Core Editor is registered. MSBuild
17.14.60.43110 is present and successfully ran the installed-package offline check.
The optional `Microsoft.Component.MSBuild` and `VC.Redist.14.Latest` component-ID
queries are false; this does not negate the working MSBuild executable or the
valid Community product. A C++ compiler/redist workload is not a separate condition
in Community §4 for distributing the already inventoried release runtime files.
No replacement DLL download, paid licence or full C++ workload is needed here.
`community-components.json` records these distinctions rather than claiming all
requested component IDs were installed.

The initially absent product/permission prompt is resolved. No security prompt was
automated; the owner handled it. The exact approved installer was then launched
through File Explorer. The actual wizard displayed the approved Microsoft-only
terms, with Next disabled until acceptance. Its accessibility document matches the
approved input after whitespace normalisation. The upgrade completed; Windows
Settings shows exactly one Tokentra RC3 entry and an enabled Uninstall action.
All 353 payload files match, the registered shortcut works, and installed offline
checks pass with empty caches. See desktop-upgrade.json and the genuine local
screenshots. This is desktop evidence, not a command-registry-only inference.

## Qt/PySide6 LGPLv3 route

[LGPLv3](https://raw.githubusercontent.com/qt/qtbase/v6.12.0/LICENSES/LGPL-3.0-only.txt)
§4 requires application terms to preserve modification and reverse-engineering rights
for debugging library modifications. §4(a,b) require library notices and GPL/LGPL
copies. §4(d)(1) allows a suitable shared-library mechanism accepting compatible
modified replacements; §4(d)(0) relink/object kits are an alternative, not an extra
requirement on this dynamic deployment. Library source obligations remain applicable.

The payload contains QtBase Core/Gui/Widgets/Network/OpenGL and related plugins,
PySide bindings and Shiboken. No GPL-only Qt Addons, Quick/QML, SVG or WebEngine
libraries are collected. Full texts and incorporated-component material are included
under `_internal/third-party-licences`, with top-level notices. The retained 94 Qt
attributions are a conservative source superset, not a claim every item is compiled.
For FreeType the FTL alternative is selected: **This software is based in part on
the work of the FreeType Team.**

[GPLv3](https://raw.githubusercontent.com/qt/qtbase/v6.12.0/LICENSES/GPL-3.0-only.txt)
§6(d) is the planned download/source delivery method: complete matching QtBase and
PySide archives alongside each eventual binary, with equivalent access and clear
instructions. The source archives include upstream build/configuration scripts;
Tokentra applies no patches. Exact official wheel comparison establishes supplier
release identity, not an independent reproducible build. No missing supplier-specific
patch is identified. Retain additional supplier build configuration if obtained.

No hardware or locked device is conveyed by this software-only download; no User
Product possession-transfer transaction is identified. Reassess §6 installation
information if distributing with hardware or adding technical restrictions.
[QT_REPLACEMENT.md](QT_REPLACEMENT.md) supplies archive hashes, observed configuration,
replacement steps and rebuild guidance. The ordinary external libraries are writable
by the installing user and have no Tokentra signature/hash gate. Tokeniser checks
cover BPE data only. An independently modified Qt build was not tested; doing one
is B/C assurance, not a separate mandatory licence condition. No formal written
source offer or upstream-homepage-only delivery scheme is used. Archives remain
local until publication is separately authorised.

## Native and Rust notice/provenance resolution

`docs/compliance/native-rust-notices.json` records exact downloaded notice hashes
and evidence categories. Actual binary paths identify aho-corasick 1.1.5,
bit-set/bit-vec 0.8.0, bstr 1.13.1, fancy-regex 0.19.0, hashbrown 0.17.1, memchr 2.8.3,
once_cell 1.21.4, pyo3/pyo3-ffi 0.29.2, regex-automata 0.4.18, regex-syntax 0.8.11,
rustc-demangle 0.1.27. Compiler commit 8bab26f4f68e0e26f0bb7960be334d5b520ea452
identifies Rust 1.97.1. The official toolchain archive supplies generated
COPYRIGHT-library.html covering standard-library incorporated components.

Full crate licences include nested Unicode notices. MIT is selected where an
alternative exists. Supplemental regex 1.13.1, rustc-hash 2.1.1 and libc 0.2.186
notices are explicitly NOT exact wheel-version proof. Build-only macros are not
separate shipped libraries. The supplier sdist has no Cargo.lock; no complete
resolved wheel SBOM is claimed. These permissive notice terms do not independently
require a historical lockfile or whole source archive. A lockfile-backed rebuild is
recommended on a future native refresh if supplier provenance stays unavailable.

Python reports OpenSSL 3.5.8, zlib 1.3.2, Expat 2.8.3, mpdecimal 2.5.1; bzip2
identifies 1.0.8 in its binary. libffi ABI 8 and static liblzma are present, with
exact semantic versions unestablished. CPython's default build pins differ from
this custom runtime and are not assigned to these binaries. New retained materials:
supplied PSF/historical/bzip2 terms, CPython 3.12.14 incorporated notices, OpenSSL
Apache-2.0, zlib, Expat MIT, mpdecimal BSD, libffi 3.4.4/3.5.2 MIT notice superset,
and old liblzma public-domain/modern 0BSD terms. XZ utilities/build-script GPL terms
do not turn separately licensed liblzma into GPL. These native library licences
require applicable notices, not complete corresponding-source delivery. No evidence
of a different supplier-specific licence/patch was found; reopen if one is identified.
The requested OpenSSL NOTICE URL returned 404; no invented notice is supplied.
Native source URLs and hash records accompany the retained texts.

PyInstaller's bootloader GPL exception and Inno Setup's permissive terms remain
included. No external fonts are bundled; icon geometry is project-generated MIT.
Installed requests/certifi/urllib3 packages are excluded from the application; the
retained superset notices do not imply their shipment or add MPL source obligations
for absent certifi files. Actual payload files, not installed-package lists, define scope.

## Security and verification limits

Review date: 21 October 2026. This is an advisory/attack-surface review, not a
vulnerability-free certification. No network service, archive/XML import or
user-supplied regex patterns are implemented; imports are plain text.

- Qt [CVE-2026-96432](https://www.qt.io/blog/security-advisory-cve-2026-96432),
  [CVE-2026-101201](https://www.qt.io/blog/security-advisory-cve-2026-101201),
  [CVE-2026-105923](https://www.qt.io/blog/security-advisory-cve-2026-105923):
  affected ranges end before deployed 6.12.0; Quick/SVG are also excluded.
- [Python 3.12.15 security changes](https://www.python.org/downloads/release/python-31215/)
  postdate 3.12.14: TLS callbacks/BIO, tar/zip extraction, URL credentials,
  StringPrep and extreme float precision lack an application input path here.
  A patched 3.12 refresh is recommended, with regression testing; no major upgrade.
- [Expat 2.8.5](https://github.com/libexpat/libexpat/releases/tag/R_2_8_5) fixes
  CVE-2026-93990 after deployed 2.8.3. Tokentra does not parse user text as XML;
  track this with the runtime refresh rather than claiming the old library is current.
- [OpenSSL 3.5.9 notes](https://openssl-library.org/news/openssl-3.5-notes/) list
  fixes after 3.5.8 affecting DTLS/QUIC, certificate processing and specialised crypto.
  These services are not exposed; hashlib SHA-256 tokeniser integrity checks remain.
- [RustSec](https://rustsec.org/advisories/), upstream
  [tiktoken](https://github.com/openai/tiktoken/security/advisories) and
  [regex](https://github.com/mrabarnett/mrab-regex/security/advisories) were reviewed.
  Specific Rust version findings are retained in security-review.json. The incomplete
  supplier lockfile limits exhaustive automated Rust auditing; do not claim one ran.

The new compliance installer passed actual desktop upgrade/licence-page/Settings
and installed payload/offline checks. Prior actual desktop uninstall/reinstall
evidence remains valid for its exact earlier installer; that destructive cycle was
not unnecessarily repeated for licence-only changes.
Do not substitute command registry observations for desktop verification. No clean
VM, physically disconnected test or process-wide packet capture is claimed.
No final v1.0 tag, public release, push or asset upload is authorised by this assessment.

## Current decision

All identified mandatory redistribution requirements have documented resolutions
for the tested Windows candidate. No unresolved owner licensing decision remains.
This is a reasoned release-engineering assessment, not a legal-compliance certificate.
The setup-only candidate is ready for final publication authorisation, **subject to
actual delivery of the retained complete Qt/PySide source archives and notices with
any authorised binary download**, retention of the Microsoft acceptance page, and
ordinary final version/tag/asset review. Publication remains expressly on hold.
A future portable binary still needs an equivalent Microsoft recipient-acceptance
arrangement and is not approved merely by this installer result.
