"""Assemble local audit evidence; this does not clear redistribution gates."""
import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import shutil
import ssl
import sys
import zlib
import pyexpat
import decimal

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist-dir', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/compliance')
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    source = ROOT / '.tools/compliance'
    destination = ROOT / 'packaging/third-party'
    for name in ('qtbase', 'pyside-setup'):
        extracted = source / 'extracted' / name
        if not extracted.is_dir():
            raise SystemExit('Run fetch_compliance_sources.py first')
        shutil.copytree(extracted, destination / (name + '-6.12.0'), dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('tests', 'README.md', '*.ini'))
    shutil.copyfile(ROOT / '.tools/InnoSetup6/license.txt', destination / 'Inno-Setup-LICENSE.txt')
    shutil.copyfile(source / 'sources.json', destination / 'qt-source-provenance.json')
    shutil.copyfile(source / 'pypi-artifacts.json', destination / 'pypi-artifacts.json')
    packages = []
    for dist in metadata.distributions():
        name = dist.metadata['Name']
        normalized = name.lower().replace('_', '-')
        if normalized in {'pyside6-essentials', 'shiboken6', 'tiktoken', 'regex'}:
            role = 'Bundled application runtime'
        elif normalized == 'pyinstaller':
            role = 'Build tool; bootloader and runtime hooks bundled'
        else:
            role = 'Build/development or installed dependency; not collected as an application package'
        packages.append(dict(name=name, version=dist.version,
            declared_license=dist.metadata.get('License-Expression') or dist.metadata.get('License'),
            license_classifiers=[v for v in dist.metadata.get_all('Classifier', []) if v.startswith('License ::')],
            requires=dist.requires or [], role=role))
    qt_entries = []
    for component in ('qtbase', 'pyside-setup'):
        for path in (source / 'extracted' / component).rglob('qt_attribution.json'):
            if 'tests' in path.relative_to(source / 'extracted').parts:
                continue
            data = json.loads(path.read_text('utf-8'), strict=False)
            for entry in data if isinstance(data, list) else [data]:
                qt_entries.append(dict(source=component, file=path.relative_to(source / 'extracted').as_posix(), **entry))
    report = dict(status='Inventory generated; consult docs/COMPLIANCE.md for the reviewed release decision',
        python=sys.version, openssl=ssl.OPENSSL_VERSION, zlib=zlib.ZLIB_RUNTIME_VERSION,
        expat=pyexpat.EXPAT_VERSION, mpdecimal=decimal.__libmpdec_version__,
        packages=sorted(packages, key=lambda p:p['name'].lower()), qt_source_attributions=qt_entries,
        qt_attribution_scope='Conservative upstream source superset, not a claim that every item is compiled into Windows binaries',
        unresolved=['Separate publication authorisation remains withheld; reviewed release gates are in COMPLIANCE.md'],
        documented_conditions=['Microsoft developer entitlement must remain satisfied; verified product evidence is in community-components.json',
                               'Retain approved scoped Microsoft runtime licence acceptance during setup',
                               'Full Qt/PySide source archives must accompany every eventual binary download'],
        recommended_verification=['Exact supplier Rust lockfile and libffi/xz semantic versions',
                                  'Independent compatible modified Qt library test; not an additional legal rebuild requirement'],
        native_rust_inventory='native-rust-notices.json', qt_correspondence='qt-correspondence.json')
    if args.dist_dir:
        folder = args.dist_dir / 'Tokentra'
        report['payload'] = [dict(path=p.relative_to(folder).as_posix(), bytes=p.stat().st_size,
            sha256=hashlib.file_digest(p.open('rb'), 'sha256').hexdigest())
            for p in sorted(folder.rglob('*')) if p.is_file()]
    (output / 'dependency-inventory.json').write_text(json.dumps(report, indent=2), 'utf-8')
    print(len(packages), 'installed packages;', len(qt_entries), 'upstream Qt attribution records')


if __name__ == '__main__':
    main()
