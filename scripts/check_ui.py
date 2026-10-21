"""Run the frozen synthetic UI diagnostic outside the source tree at four Qt scales."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    executable, output = args.executable.resolve(), args.output.resolve()
    environment = os.environ.copy()
    environment.update(PYTHONPATH='', PYTHONHOME='', QT_QPA_PLATFORM='windows')
    system = Path(os.environ.get('SystemRoot', 'C:/Windows'))
    environment['PATH'] = os.pathsep.join((str(system / 'System32'), str(system)))
    with tempfile.TemporaryDirectory(prefix='tokentra-ui-') as folder:
        environment.update(TEMP=folder, TMP=folder, TMPDIR=folder,
                           TIKTOKEN_CACHE_DIR=str(Path(folder) / 'empty-token-cache'),
                           DATA_GYM_CACHE_DIR=str(Path(folder) / 'empty-data-gym'))
        for scale in ('1', '1.25', '1.5', '2'):
            environment['QT_SCALE_FACTOR'] = scale
            report = output / ('scale-' + scale) / 'ui.json'
            report.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run([str(executable), '--ui-check', '--report', str(report)],
                                    cwd=folder, env=environment, timeout=60)
            data = json.loads(report.read_text('utf-8'))
            assert result.returncode == 0 and data['status'] == 'passed', data
            assert data['version'] == '1.0.0' and data['platform'] == 'windows'
            print(f'Native frozen UI scale {scale}: passed; {len(data["numeric_layouts"])} numeric layouts; screenshots saved', flush=True)


if __name__ == '__main__':
    main()
