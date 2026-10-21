"""Build-time only: acquire exact-version upstream source and attribution evidence.

Never imported by Tokentra. Downloaded archives are private build inputs until
their source correspondence and redistribution set have been reviewed.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import tarfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / '.tools/compliance'
SOURCES = {
    'qtbase': 'https://download.qt.io/official_releases/qt/6.12/6.12.0/submodules/qtbase-everywhere-src-6.12.0.tar.xz',
    'pyside-setup': 'https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.12.0-src/pyside-setup-everywhere-src-6.12.0.tar.xz',
}


def acquire(item):
    name, url = item
    target = DESTINATION / url.rsplit('/', 1)[1]
    if not target.exists():
        # A failed download never becomes an apparently complete archive.
        temporary = target.with_suffix(target.suffix + '.part')
        with urlopen(url, timeout=120) as response, temporary.open('wb') as output:
            while data := response.read(1024 * 1024):
                output.write(data)
        temporary.rename(target)
    digest = hashlib.file_digest(target.open('rb'), 'sha256').hexdigest()
    notices = []
    with tarfile.open(target, 'r:xz') as archive:
        for member in archive.getmembers():
            parts = Path(member.name).parts
            basename = parts[-1] if parts else ''
            # Copy only attribution/licence/build metadata, preserving paths.
            wanted = ('LICENSES' in parts or basename == 'qt_attribution.json'
                      or basename.upper().startswith(('LICENSE', 'LICENCE', 'COPYING', 'NOTICE', 'COPYRIGHT'))
                      or basename.upper() in ('FTL.TXT', 'AUTHORS', 'PATENTS')
                      or basename in ('qt-configure-module.bat', 'configure.bat', 'README.md'))
            if not member.isfile() or not wanted or member.size > 4 * 1024 * 1024:
                continue
            relative = Path(*parts[1:])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe upstream path')
            output = DESTINATION / 'extracted' / name / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(archive.extractfile(member).read())
            notices.append(relative.as_posix())
    return dict(component=name, version='6.12.0', source_url=url, archive=target.name,
                sha256=digest, bytes=target.stat().st_size, extracted_notices=notices,
                verification='Exact upstream version URL; locally calculated SHA-256. Binary build correspondence still requires review.')


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(acquire, SOURCES.items()))
    (DESTINATION / 'sources.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    for item in results:
        print(item['component'], item['bytes'], item['sha256'], len(item['extracted_notices']))


if __name__ == '__main__':
    main()
