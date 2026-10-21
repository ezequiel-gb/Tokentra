# Build on the target OS: python -m PyInstaller packaging/tokentra.spec --noconfirm
from pathlib import Path
import sys
import os
import shutil
from PyInstaller.utils.hooks import collect_data_files

root = Path(SPECPATH).parent
datas = [(str(root / 'app/assets'), 'app/assets')]
datas += [(str(root / 'packaging/third-party'), 'third-party-licences')]
datas += [(str(root / 'LICENSE'), 'third-party-licences/Tokentra'),
          (str(root / 'THIRD_PARTY_NOTICES.md'), 'third-party-licences'),
          (str(root / 'packaging/INSTALLATION_TERMS.txt'), 'third-party-licences'),
          (str(root / 'docs/QT_REPLACEMENT.md'), 'third-party-licences'),
          (str(root / 'docs/COMPLIANCE.md'), 'third-party-licences')]
datas += collect_data_files('tiktoken', includes=['**/LICENSE*'])
a = Analysis([str(root / 'launch.py')], pathex=[str(root)], datas=datas,
             excludes=['PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets',
                       'tiktoken_ext.openai_public', 'tiktoken.load', 'requests',
                       'tkinter', 'pytest', 'numpy'])
# QPlainTextEdit and PNG branding do not use PDF image loading or the Qt
# virtual keyboard. Those optional plugins pull in unrelated PDF/QML runtimes.
a.binaries = [entry for entry in a.binaries if not any(part in entry[0].replace('\\', '/').lower()
              for part in ('imageformats/qpdf', 'platforminputcontexts/qtvirtualkeyboard'))]
if sys.platform == 'win32':
    # Qt 6.12 uses the Windows system ICU ABI. On this host PyInstaller found a
    # different ICU 78 DLL via the bundled development runtime's PATH. Never
    # shadow the system DLL with that incompatible same-named library.
    a.binaries = [entry for entry in a.binaries
                  if not Path(entry[0]).name.lower().startswith(('icuuc', 'icudt', 'icuin',
                      'qt6pdf', 'qt6qml', 'qt6quick', 'qt6virtualkeyboard'))]
    # A broad developer PATH can resolve Python's OpenSSL dependencies from an
    # unrelated tool (observed: Poppler). Bind the exact runtime's own DLLs.
    python_dlls = Path(sys.base_prefix) / 'DLLs'
    pinned = {'libcrypto-3-x64.dll', 'libssl-3-x64.dll', 'libffi-8.dll'}
    a.binaries = [(dest, str(python_dlls / Path(dest).name), kind)
                  if Path(dest).name.lower() in pinned else (dest, source, kind)
                  for dest, source, kind in a.binaries]
    for name in pinned:
        if not (python_dlls / name).is_file():
            raise RuntimeError('Missing Python runtime dependency: ' + name)
    # Windows 11 supplies UCRT/API-set libraries. Do not copy unrelated SDK/tool
    # versions discovered through PATH. This raster, PNG-based application also
    # needs no Mesa software OpenGL, SVG, optional image codecs or translations.
    def needed_windows_binary(entry):
        path = entry[0].replace('\\', '/').lower()
        name = path.rsplit('/', 1)[-1]
        if name.startswith('api-ms-') or name in ('ucrtbase.dll', 'opengl32sw.dll', 'qt6svg.dll'):
            return False
        if '/imageformats/' in path and name != 'qico.dll':
            return False
        if '/iconengines/' in path or name == 'qdirect2d.dll':
            return False
        return True
    a.binaries = [entry for entry in a.binaries if needed_windows_binary(entry)]
    a.datas = [entry for entry in a.datas if '/translations/' not in entry[0].replace('\\', '/').lower()]
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='Tokentra',
          console=bool(os.environ.get('TOKENTRA_BUILD_CONSOLE')),
          version=str(root / 'packaging/windows-version-info.txt') if sys.platform == 'win32' else None,
          icon=str(root / 'app/assets/icon.ico') if sys.platform == 'win32' else None)
bundle = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name='Tokentra')
# Prominent documentation also travels at the top level of the installed/portable
# directory. The full component notice trees remain under _internal.
for source, name in ((root / 'LICENSE', 'LICENSE.txt'),
                     (root / 'THIRD_PARTY_NOTICES.md', 'THIRD_PARTY_NOTICES.md'),
                     (root / 'docs/QT_REPLACEMENT.md', 'QT_REPLACEMENT.md'),
                     (root / 'packaging/INSTALLATION_TERMS.txt', 'INSTALLATION_TERMS.txt')):
    shutil.copyfile(source, Path(DISTPATH) / 'Tokentra' / name)
if sys.platform == 'darwin':
    app = BUNDLE(bundle, name='Tokentra.app', bundle_identifier='app.tokentra.desktop',
                 info_plist={'CFBundleShortVersionString': '1.0.0', 'CFBundleVersion': '1.0.0', 'NSHighResolutionCapable': True})
