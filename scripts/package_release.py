"""Create the tested Windows portable and source archives with checksums."""
import hashlib
from pathlib import Path
import sys
import zipfile
import argparse

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--label", default="1.0.0-rc.3")
    args = parser.parse_args()
    if sys.platform != "win32":
        raise SystemExit("This archive script is for the Windows delivery. Use native packaging on other platforms.")
    output = args.dist_dir.resolve()
    if not args.label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-" for c in args.label):
        raise SystemExit("Use a simple version label without path separators.")
    windows_zip = output / f"Tokentra-{args.label}-windows-x64-Portable.zip"
    source_zip = output / f"Tokentra-{args.label}-source.zip"
    if windows_zip.exists() or source_zip.exists():
        raise SystemExit("Archive already exists. Choose a new label; previous releases are preserved.")
    portable = output / "Tokentra"
    if not (portable / "Tokentra.exe").is_file():
        raise SystemExit("Build Tokentra first.")
    (portable / "README.txt").write_text(
        f"Tokentra {args.label} | Precision Token Counter and Context Planning\n\n"
        "Run Tokentra.exe. Keep the whole folder, including _internal, together.\n"
        "No Python installation, account, API key or internet connection is required.\n"
        "All three OpenAI tokenisers are bundled locally. No user text is automatically saved.\n\n"
        "Import: Ctrl+O | Clear: Ctrl+L | Copy count: Ctrl+Shift+C | Full-screen: F11\n"
        "Count file avoids editor layout overhead for large documents, but requires RAM.\n\n"
        "This optional Portable archive is an unsigned Windows release candidate. macOS/Linux validation, physical\n"
        "offline and DPI checks, and the public redistribution licence audit remain outstanding.\n"
        "Dependency notices are in _internal/third-party-licences. See the source README and docs\n"
        "for measured performance, exact text policies and the full release status.\n", encoding="utf-8")
    with zipfile.ZipFile(windows_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(portable.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(portable.parent))
    source_files = [ROOT / name for name in ("README.md", "LICENSE", "pyproject.toml", "requirements.txt", "requirements-dev.txt",
                   "requirements-lock.txt", ".gitignore", ".gitattributes", "launch.py", "Tokentra_Product_Specification.md", "Start Tokentra.cmd",
                   "CHANGELOG.md", "THIRD_PARTY_NOTICES.md")]
    for folder in ("app", "tests", "scripts", "packaging", "docs", ".github"):
        source_files += [p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    with zipfile.ZipFile(source_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_files):
            archive.write(path, Path("Tokentra") / path.relative_to(ROOT))
    for archive in (windows_zip, source_zip):
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        archive.with_suffix(archive.suffix + ".sha256").write_text(f"{digest}  {archive.name}\n", "ascii")
        print(f"Created {archive.name}: {archive.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
