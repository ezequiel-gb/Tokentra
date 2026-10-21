# LGPL library source, replacement and rebuilding

Tokentra uses Qt, PySide6 Essentials and Shiboken6 6.12.0 under LGPLv3.
Tokentra's own code remains MIT. You may modify these libraries and reverse
engineer the combined work to debug those modifications. No Tokentra term
restricts those rights. Microsoft-only setup terms do not apply to these libraries.

## Source delivery

Every eventual binary download must be accompanied, in the same release and with
equivalent download access, by these **complete** archives (GPLv3 section 6(d),
as incorporated by LGPLv3). A link to an upstream homepage alone is not our delivery:

| Archive | SHA-256 |
|---|---|
| qtbase-everywhere-src-6.12.0.tar.xz | a951bd163c7b80fc6b8c88d7668fb56abf91c152373e13c10666763238131307 |
| pyside-setup-everywhere-src-6.12.0.tar.xz | 099c1a597cf33c1b000e11cf68a0b82d216fb802bf81726efc720394f10c7751 |

The release-preparation copies are retained in `release-audit/third-party-sources`.
Their upstream locations and hashes are also in `packaging/third-party/qt-source-provenance.json`.
Reuse these archives; do not duplicate them for every local trial build. Include
this document, the manifests, Tokentra source/build scripts and licence texts in
the release. Do not upload an installer alone.

Qt Core, Gui, Widgets, Network, OpenGL and the collected Windows platform/style,
image, touch, network-information and TLS plugins are QtBase components. PySide
bindings and Shiboken are covered by the second archive. Qt Quick/QML, WebEngine,
PDF, SVG and Addons libraries are not in the audited payload. The source archives
contain their upstream CMake/configuration and binding-generation scripts.

`docs/compliance/qt-correspondence.json` records actual runtime build information:
Windows x64, shared release Qt 6.12.0, MSVC 2022, PySide limited API. Exact native
files were compared with official release wheels (228 PySide and 12 Shiboken
files, all identical). Tokentra applies no source patches. This establishes supplier
release identity, not byte-for-byte independent reproducibility. Supplier-specific
configure command lines were not supplied; retain any additional supplier build
metadata when available. No claim is made that the examples below reproduce their
exact binary hashes.

## Replace compatible libraries

1. Close Tokentra. Copy the **whole** installed or portable directory to a writable
   test folder and keep an unchanged backup. Preferences and documents need not be deleted.
2. Replace compatible files beneath `_internal/PySide6` and `_internal/shiboken6`.
   Replace DLLs, Python extensions and dependent plugins as a mutually compatible
   set when your change requires it. Keep Windows x64 architecture, Python 3.12 /
   compatible limited API, Qt 6.12 ABI, module names and runtime dependencies.
3. Start the copied `Tokentra.exe`. Try text counting, every encoding, file import,
   both modes and window controls. Restore the backup if a replacement is incompatible.
4. Do not overwrite Windows system DLLs. Replacing Qt does not require a Tokentra
   signing key, activation, network service or application executable rebuild.

The package is an onedir shared-library deployment: these files are ordinary external
files, not embedded in a self-extracting executable. Tokeniser-table checks cover
only tokeniser data, not Qt/PySide/Shiboken libraries. The normal per-user installation
directory is writable by its owner. No independently modified Qt build has been
tested here; such a test is recommended engineering assurance, not an additional
licence requirement to perform a full rebuild before distribution.

## Build compatible replacements

Use the retained source archives and their build documentation. Install a properly
licensed MSVC 2022 x64 toolchain, Windows SDK, CMake, Ninja and Python. Binding
generation also requires the supported LLVM/libclang tooling described in PySide's
source documentation. Those general-purpose build tools are not bundled runtimes.

In an MSVC x64 development shell, a starting QtBase shared release build is:

```powershell
mkdir qt-build
cd qt-build
..\qtbase-everywhere-src-6.12.0\configure.bat -opensource -confirm-license -release -shared -nomake examples -nomake tests -prefix C:\qt-replacement
cmake --build . --parallel
cmake --install .
```

Then, from the matching PySide setup source with its prerequisites available:

```powershell
python setup.py build --qtpaths=C:\qt-replacement\bin\qtpaths.exe --module-subset=Core,Gui,Widgets,Network --limited-api=yes --parallel=4
```

Follow upstream packaging instructions for the resulting bindings and Shiboken;
do not mix incompatible generated bindings with a different Qt configuration.
Record your flags, patches and external dependencies. These are starting instructions,
not a tested independent rebuild or a promise of ABI compatibility for arbitrary changes.
See [Qt Windows builds](https://doc.qt.io/qt-6/windows-building.html) and
[PySide source builds](https://doc.qt.io/qtforpython-6/building_from_source/index.html).

No hardware or locked device is conveyed with Tokentra. The GPLv3 section 6
User Product transaction condition is not identified for this software-only download;
nevertheless all replacement steps require no secrets or vendor authorisation.
If distributing Tokentra with hardware, reassess installation-information obligations.
The applicable texts remain authoritative: `_internal/third-party-licences/qtbase-6.12.0/LICENSES`.
