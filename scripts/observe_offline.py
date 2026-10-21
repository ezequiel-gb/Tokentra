"""Sample packaged-process endpoints during its isolated offline diagnostic.

This observes native endpoints too, but is not packet capture or a firewall test.
Short-lived connections can occur between samples. Requires development psutil.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import psutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    executable = args.executable.resolve()
    observations, errors = set(), set()
    samples = 0
    with tempfile.TemporaryDirectory(prefix='tokentra-endpoints-') as temporary:
        environment = os.environ.copy()
        system = Path(os.environ.get('SystemRoot', 'C:/Windows'))
        environment.update(PYTHONPATH='', PYTHONHOME='',
            PATH=os.pathsep.join((str(system / 'System32'), str(system))),
            TIKTOKEN_CACHE_DIR=str(Path(temporary) / 'empty-cache'),
            DATA_GYM_CACHE_DIR=str(Path(temporary) / 'empty-data-gym'))
        output = Path(temporary) / 'offline.json'
        process = subprocess.Popen([str(executable), '--offline-check', '--report', str(output)],
            cwd=temporary, env=environment)
        root = psutil.Process(process.pid)
        deadline = time.monotonic() + 60
        while process.poll() is None:
            if time.monotonic() > deadline:
                process.terminate()  # Only the diagnostic process created here.
                raise RuntimeError('Offline diagnostic timed out')
            try:
                for child in [root] + root.children(recursive=True):
                    try:
                        for connection in child.net_connections(kind='inet'):
                            observations.add(str((connection.type, connection.laddr, connection.raddr, connection.status)))
                    except psutil.NoSuchProcess:
                        pass
                    except psutil.AccessDenied:
                        errors.add('Endpoint inspection access denied')
                samples += 1
            except psutil.NoSuchProcess:
                pass
            time.sleep(0.005)
        diagnostic = json.loads(output.read_text('utf-8'))
        result = dict(status='passed' if process.returncode == 0 and not observations and not errors else 'review required',
            exit_code=process.returncode, samples=samples, observed_endpoints=sorted(observations),
            inspection_errors=sorted(errors), offline_diagnostic=diagnostic,
            scope='Process/child TCP and UDP endpoint sampling during explicit synthetic offline diagnostic; '
                  'Python socket/DNS audit, empty cache, external cwd, developer PATH removed. '
                  'Not physical disconnection, packet capture, clean-machine validation or proof of no transient network activity.')
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2), 'utf-8')
        print(result['status'], 'samples:', samples, 'observed endpoints:', len(observations), 'errors:', len(errors))
        if result['status'] != 'passed':
            raise SystemExit(1)


if __name__ == '__main__':
    main()
