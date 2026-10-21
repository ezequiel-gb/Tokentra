# Third-party notices and redistribution inventory

Tokentra code is MIT licensed, Copyright (c) 2026 Ezequiel Gomez. Third-party software
retains its own licences. **Publication remains on hold pending final validation and separate authorisation**; see
[COMPLIANCE.md](docs/COMPLIANCE.md). The owner reports accepting Visual Studio Community
2022 terms and approved Microsoft runtime terms during setup. MIT does not satisfy
Qt or other dependency obligations. See top-level INSTALLATION_TERMS.txt and QT_REPLACEMENT.md
in the Windows package. Microsoft terms apply only to Microsoft runtime files.

Full retained texts are in `packaging/third-party`, installed under
`_internal/third-party-licences`. The audit dependency-inventory.json records installed
metadata, declared dependencies, 94 Qt source attributions and the audited payload manifest.
Installed dependencies and bundled packages are distinguished.

| Component | Version | Licence / obligations | Bundled and status |
|---|---|---|---|
| Python | 3.12.14 | PSF-2.0 and historical/incorporated notices | Yes; supplied and supplemental native notices retained; exact supplier libffi/xz versions unestablished |
| PySide6 Essentials, Shiboken6, Qt | 6.12.0 | LGPLv3 selected; copyright, GPL/LGPL texts, corresponding source, replacement rights | Yes; external DLLs; official wheel identity verified; compatible replacement rights preserved; full source archives must accompany eventual downloads |
| Qt incorporated components | See source attribution records | BSD/MIT, Apache, Unicode, zlib, libpng, FTL and component-specific alternatives | Conservative upstream notice superset retained; runtime QtBase module mapping in docs/compliance/qt-correspondence.json |
| tiktoken | 0.14.0 | MIT; OpenAI/Shantanu Jain notice retained | Yes; 13 binary-evidenced crate versions; full notices and Rust standard-library attribution retained; no complete supplier lockfile claimed |
| Encoding tables | o200k_base, cl100k_base, p50k_base | Official constructor provenance/hashes in manifest; tiktoken notice retained | Yes; local assets |
| regex | 2026.9.29 | Apache-2.0 AND CNRI-Python; both texts retained | Yes |
| OpenSSL | 3.5.8, runtime reported | Apache-2.0; Apache licence and retained incorporated notices | Yes; Python DLLs pinned; supplemental notices retained |
| zlib | 1.3.2, runtime reported | Zlib | Yes, Python incorporated; applicable upstream notice retained |
| Expat | 2.8.3, runtime reported | MIT | Yes, pyexpat; applicable upstream notice retained |
| mpdecimal | 2.5.1, runtime reported | BSD-2-Clause | Yes, _decimal; applicable upstream notice retained |
| bzip2 | 1.0.8, binary string | bzip2 licence, retained in Python licence | Yes, _bz2 |
| libffi | ABI 8, semantic version unknown | MIT-style; upstream MIT notice superset retained; exact version not claimed | Yes; exact supplier version not established; no full-source duty identified |
| xz/LZMA | Exact version unknown | liblzma public-domain / modern 0BSD; upstream statements retained | Yes, _lzma; exact version unestablished, licence-family notices retained |
| Microsoft C/C++ runtime | 14.44.35211.0 | Microsoft Distributable Code terms, entitlement required | Yes; Community route owner-attested; scoped Microsoft licence accepted during setup; final installer verification pending |
| Windows UCRT/ICU | OS supplied | Windows system components | Not copied in revised payload |
| PyInstaller | 6.22.3 | GPL-2.0-or-later with bootloader exception, full texts retained | Bootloader/runtime hooks; exception permits independent app licensing |
| Inno Setup | 6.7.3 | Inno licence, retain copyright/terms, no misrepresentation | Setup/uninstaller; full licence retained |
| requests | 2.34.2 | Apache-2.0 | Installed but excluded; notice retained |
| urllib3 | 2.8.0 | MIT | Excluded requests chain; notice retained |
| certifi | 2026.10.19 | MPL-2.0 | Excluded requests chain; notice retained |
| charset-normalizer | 3.5.2 | MIT | Excluded requests chain; notice retained |
| idna | 3.20 | BSD-3-Clause | Excluded requests chain; notice retained |
| Icon | Project-generated geometry | Tokentra MIT, scripts/make_icon.py | PNG/ICO; no external artwork |
| Fonts | System-selected | Host font terms | No font files bundled |

Build/test-only installed tools: pytest 9.1.1, pytest-qt 4.5.0, pluggy 1.7.0,
iniconfig 2.3.1, setuptools 84.2.1, altgraph 0.17.5, pefile 2024.8.26 (MIT);
colorama 0.4.6 (BSD); Pygments 2.21.0 (BSD-2-Clause); psutil 7.2.2 and
pywin32-ctypes 0.2.3 (BSD-3-Clause); packaging 26.3 (Apache-2.0 OR BSD-2-Clause);
typing_extensions 4.16.0 (PSF-2.0); pyinstaller-hooks-contrib 2026.9
(Apache/GPL terms vary by file). Package bodies are not application requirements;
bundled hooks/bootloader contributions retain upstream terms. Installed extra PySide
Addons/PDF/WebEngine packages are not application requirements; inspect the payload
manifest rather than inferring shipment from the build environment.

This software is based in part on the work of the FreeType Team, where incorporated
by Qt. FTL is the selected alternative for FreeType; full upstream attribution and
licence material is retained. The Qt tree also includes source-only/unbundled notices.
No commercial Qt licence is claimed.

Primary references: [Qt obligations](https://www.qt.io/development/open-source-lgpl-obligations),
[Qt for Python licences](https://doc.qt.io/qtforpython-6/licenses.html),
[Microsoft redistribution](https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution),
[OpenSSL licence](https://openssl-library.org/source/license/index.html),
[tiktoken source](https://github.com/openai/tiktoken),
[Inno licence](https://github.com/jrsoftware/issrc/blob/is-6_7_3/license.txt).


Rust crate and native notice file inventories, source URLs and hashes are in
`packaging/third-party/native-rust-provenance.json`. Rust crates select MIT where
available; nested Unicode notices and the matching Rust 1.97.1 standard-library
attribution document are retained in `rust-crates` and `rust-standard-library`.
Supplemental candidate crate versions are labelled and must not be presented as an
exact resolved wheel SBOM. Corresponding-source delivery is required for redistributed
LGPL libraries; a complete source archive is not required merely because a
permissively licensed dependency is native or statically incorporated.
