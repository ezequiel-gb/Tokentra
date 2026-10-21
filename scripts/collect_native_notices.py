"""Collect upstream notices without executing or extracting third-party source code.

Inputs are local HTTPS downloads in .tools/compliance. Crate versions evidenced
by binary paths are distinguished from supplemental notices, not a wheel SBOM.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tarfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    source = ROOT / '.tools/compliance'
    output = ROOT / 'packaging/third-party'
    evidence = ROOT / 'docs/compliance'
    rust = json.loads((evidence / 'rust-components.json').read_text())
    rows = []
    for path in sorted(source.glob('*.crate')):
        with tarfile.open(path) as archive:
            members = [m for m in archive.getmembers() if m.isfile()]
            manifest = next(m for m in members if m.name.count('/') == 1 and m.name.endswith('/Cargo.toml'))
            package = tomllib.loads(archive.extractfile(manifest).read().decode())['package']
            name, version = package['name'], package['version']
            notice_files = []
            for member in members:
                relative = Path(member.name.split('/', 1)[1])
                if relative.is_absolute() or '..' in relative.parts:
                    raise ValueError('Unsafe archive member')
                if not re.search(r'^(LICENSE|LICENCE|COPYING|COPYRIGHT|NOTICE|UNLICENSE)', relative.name, re.I):
                    continue
                target = output / 'rust-crates' / f'{name}-{version}' / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
                notice_files.append(target.relative_to(output).as_posix())
            if not notice_files:
                raise ValueError('No notices: ' + name)
        matched = next((r for r in rust['components'] if r['name'] == name and r['version'] == version), None)
        rows.append(dict(name=name, version=version, license=package.get('license'),
                         evidence=matched['evidence'] if matched else 'supplemental notice; exact binary version unestablished',
                         url=f'https://static.crates.io/crates/{name}/{name}-{version}.crate',
                         sha256=digest(path), notices=notice_files))
    # Rust's generated library-only attribution document covers the standard
    # library's incorporated code, rather than inferring it from rustc's Cargo.lock.
    toolchain = source / 'rustc-1.97.1-windows.tar.xz'
    with tarfile.open(toolchain) as archive:
        for name in ('COPYRIGHT-library.html', 'LICENSE-MIT', 'LICENSE-APACHE', 'COPYRIGHT'):
            member = next(m for m in archive.getmembers() if m.isfile() and Path(m.name).name == name)
            target = output / 'rust-standard-library' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    native = output / 'python-native'
    native.mkdir(exist_ok=True)
    names = ['openssl-LICENSE.txt', 'zlib-LICENSE.txt', 'expat-COPYING.txt',
             'libffi-LICENSE.txt', 'libffi-latest-LICENSE.txt', 'xz-5.2.5-COPYING.txt',
             'xz-5.8.1-COPYING.txt', 'xz-5.8.1-COPYING.0BSD.txt', 'python-3.12.14-license.rst']
    for name in names:
        shutil.copyfile(source / name, native / name)
    header = (source / 'mpdecimal-header.h').read_text()
    # Preserve the complete upstream copyright/permission/disclaimer header.
    block = re.search(r'/\*.*?\*/', header, re.S).group()
    if 'Stefan Krah' not in block or 'Redistribution' not in block:
        raise ValueError('Unexpected mpdecimal copyright header')
    (native / 'mpdecimal-COPYRIGHT.txt').write_text(block + '\n', encoding='utf8')
    report = dict(rust_compiler_commit=rust['compiler_commit'], rust_compiler='1.97.1',
                  rust_standard_library_archive_sha256=digest(toolchain),
                  rust_standard_library_url='https://static.rust-lang.org/dist/rustc-1.97.1-x86_64-pc-windows-msvc.tar.xz',
                  rust_components=rows,
                  scope='Binary-evidenced crates plus labelled permissive notice superset; not a complete supplier lockfile or independently reproduced wheel',
                  native_notice_files=[dict(path=p.relative_to(output).as_posix(),sha256=digest(p)) for p in sorted(native.iterdir())])
    downloads = json.loads((source / 'supplement-downloads.json').read_text())
    downloads += [dict(name='mpdecimal-header.h', url='https://raw.githubusercontent.com/python/cpython/v3.12.14/Modules/_decimal/libmpdec/mpdecimal.h'),
                  dict(name='python-3.12.14-license.rst', url='https://raw.githubusercontent.com/python/cpython/v3.12.14/Doc/license.rst'),
                  dict(name='libffi-latest-LICENSE.txt', url='https://raw.githubusercontent.com/libffi/libffi/v3.5.2/LICENSE')]
    downloads = list({r['name']: r for r in downloads}.values())
    report['native_source_downloads'] = [dict(**{k: r[k] for k in ('name', 'url')}, sha256=digest(source / r['name'])) for r in downloads
                                       if not r['name'].endswith('.crate') and (source / r['name']).is_file()]
    (evidence / 'native-rust-notices.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    shutil.copyfile(evidence / 'native-rust-notices.json', output / 'native-rust-provenance.json')
    print(f'{len(rows)} crate notice sets; Rust library attribution; {len(list(native.iterdir()))} Python native notices')


if __name__ == '__main__':
    main()
