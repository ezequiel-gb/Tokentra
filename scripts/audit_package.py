"""Inspect frozen payload hygiene, module filenames and Windows GUI metadata."""
import argparse
import hashlib
import json
from pathlib import Path
import types
import sys
from PyInstaller.archive.readers import CArchiveReader

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist-dir", type=Path, default=ROOT / "dist-stabilised")
    parser.add_argument("--report", type=Path, default=ROOT / "docs/stabilisation/package-audit.json")
    args = parser.parse_args()
    folder = args.dist_dir / "Tokentra"
    executable = folder / "Tokentra.exe"
    files = [path for path in folder.rglob("*") if path.is_file()]
    issues = []
    forbidden = {".venv", "__pycache__", ".pytest_cache", ".git", "tests", ".verification-tmp"}
    local_prefixes = [str(ROOT).lower(), str(ROOT).lower().replace("\\", "/")]
    for path in files:
        relative = path.relative_to(folder)
        if forbidden.intersection(relative.parts) or path.suffix in (".ini", ".log", ".pdb"):
            issues.append(str(relative))
        # Search data/binaries for this workspace path in UTF-8 and UTF-16.
        payload = path.read_bytes().lower()
        if any(prefix.encode("utf-8") in payload or prefix.encode("utf-16-le") in payload
               for prefix in local_prefixes):
            issues.append("local workspace path in " + str(relative))
    archive = CArchiveReader(str(executable))
    pyz = archive.open_embedded_archive("PYZ.pyz")
    filenames = set()
    def inspect_code(code):
        if isinstance(code, types.CodeType):
            filenames.add(code.co_filename)
            for constant in code.co_consts:
                inspect_code(constant)
    for name in pyz.toc:
        inspect_code(pyz.extract(name))
    leaked_modules = [name for name in filenames if any(prefix in name.lower() for prefix in local_prefixes)]
    if leaked_modules:
        issues.append("workspace paths in frozen module filenames")
    unwanted_modules = [name for name in pyz.toc if name.startswith(("pytest", "requests", "tiktoken.load",
                                                                 "tiktoken_ext.openai_public", "numpy"))]
    if unwanted_modules:
        issues.append("unexpected development/network loader modules")
    runtime_checks = {}
    for name in ('libcrypto-3-x64.dll', 'libssl-3-x64.dll', 'libffi-8.dll'):
        source = Path(sys.base_prefix) / 'DLLs' / name
        matches = [p for p in files if p.name.lower() == name]
        expected = hashlib.sha256(source.read_bytes()).hexdigest()
        runtime_checks[name] = bool(matches) and all(
            hashlib.sha256(p.read_bytes()).hexdigest() == expected for p in matches)
        if not runtime_checks[name]:
            issues.append('Runtime DLL differs from Python supplier: ' + name)
    for path in files:
        name = path.name.lower()
        if name.startswith('api-ms-') or name in ('ucrtbase.dll', 'opengl32sw.dll', 'qt6svg.dll'):
            issues.append('Unexpected system/unused DLL: ' + str(path.relative_to(folder)))
    notices = folder / '_internal/third-party-licences'
    required_notices = ('Tokentra/LICENSE', 'THIRD_PARTY_NOTICES.md', 'COMPLIANCE.md',
                        'qtbase-6.12.0/LICENSES/LGPL-3.0-only.txt',
                        'qtbase-6.12.0/LICENSES/GPL-3.0-only.txt', 'Inno-Setup-LICENSE.txt')
    required_notices += ('INSTALLATION_TERMS.txt', 'QT_REPLACEMENT.md',
                         'rust-standard-library/COPYRIGHT-library.html',
                         'native-rust-provenance.json', 'python-native/expat-COPYING.txt',
                         'python-native/mpdecimal-COPYRIGHT.txt', 'python-native/openssl-LICENSE.txt')
    for name in required_notices:
        if not (notices / name).is_file():
            issues.append('Missing required audit notice: ' + name)
    import pefile
    pe = pefile.PE(str(executable), fast_load=True)
    assert pe.OPTIONAL_HEADER.Subsystem == 2, "Normal GUI executable must not open a console"
    assets = folder / "_internal/app/assets/tokenizers"
    manifest = json.loads((assets / "manifest.json").read_text("utf-8"))
    for encoding, entry in manifest["encodings"].items():
        assert hashlib.sha256((assets / entry["file"]).read_bytes()).hexdigest() == entry["sha256"]
    result = dict(status="passed" if not issues else "failed", file_count=len(files),
                  payload_bytes=sum(p.stat().st_size for p in files),
                  gui_subsystem=True, encodings_verified=list(manifest["encodings"]),
                  frozen_modules=len(pyz.toc), module_filenames_checked=len(filenames),
                  source_path_leaks=len(leaked_modules), issues=issues,
                  python_runtime_dlls_match=runtime_checks,
                  scope="Payload paths/data and frozen code filenames; not a formal secret scan or licence certification")
    args.report.write_text(json.dumps(result, indent=2), "utf-8")
    print(json.dumps(result, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
