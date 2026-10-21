"""Create a reviewed, allowlisted source checkpoint without private build history."""
import argparse
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.publication/Tokentra')
    parser.add_argument('--report', type=Path, default=ROOT / 'docs/release-audit/source-hygiene.json')
    args = parser.parse_args()
    target = args.output.resolve()
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing source checkpoint')
    target.mkdir(parents=True)
    roots = ['README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md', 'CHANGELOG.md',
             'pyproject.toml', 'requirements.txt', 'requirements-dev.txt',
             'requirements-lock.txt', '.gitignore', '.gitattributes', 'launch.py', 'Start Tokentra.cmd',
             'Tokentra_Product_Specification.md']
    files = [ROOT / name for name in roots]
    for name in ('app', 'tests', 'packaging', '.github', 'scripts'):
        files += [p for p in (ROOT / name).rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts
                  and p.name not in ('cleanup_previous.ps1', 'verify_installer.ps1', 'upgrade_rc3.ps1')]
    for name in ('COMPLIANCE.md', 'WINDOWS_INSTALLER.md', 'WINDOWS_VALIDATION.md',
                 'PUBLICATION.md', 'RELEASE_NOTES.md', 'SOURCE_CHECKPOINT.md', 'RELEASE_READINESS.md',
                 'INSTALLATION_DISCREPANCY.md'):
        files.append(ROOT / 'docs' / name)
    files.append(ROOT / 'docs/QT_REPLACEMENT.md')
    files += [p for p in (ROOT / 'docs/compliance').glob('*') if p.suffix in ('.json', '.vsconfig')]
    files += list((ROOT / 'docs/screenshots').glob('*.png'))
    # Machine-readable evidence intentionally selected, not all private diagnostics.
    for name in ('benchmark.json', 'upstream-wheel-comparison.json', 'dependency-inventory.json'):
        files.append(ROOT / 'docs/release-audit' / name)
    findings = []
    patterns = {
        'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        'github_token': rb'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}',
        'aws_key': rb'AKIA[A-Z0-9]{16}',
        'credential_url': rb'https?://[^\s/:]+:[^\s/@]+@',
        'local_user_path': rb'(?i)[A-Z]:[\\/]Users[\\/]',
    }
    for source in sorted(set(files)):
        relative = source.relative_to(ROOT)
        content = source.read_bytes()
        if source.suffix.lower() not in ('.png', '.ico'):
            for kind, expression in patterns.items():
                if re.search(expression, content):
                    findings.append(dict(path=relative.as_posix(), kind=kind))
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    report = dict(status='passed' if not findings else 'review required', files=len(set(files)), findings=findings,
        scope='Allowlisted source and high-signal pattern scan; not a comprehensive secret/vulnerability certification',
        history='No Git repository existed in supplied workspace; curated initial history must be reviewed before publication')
    args.report.write_text(json.dumps(report, indent=2), 'utf-8')
    print(json.dumps(report, indent=2))
    if findings:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
