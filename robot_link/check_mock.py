#!/usr/bin/env python3
"""Exercise the real UDP CLI without site packages, devices or runtime copies."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile

from esrobo_link.client import RobotClient


def main():
    package = Path(__file__).resolve().parent
    env = dict(os.environ, PYTHONPATH=str(package))
    with tempfile.TemporaryDirectory(prefix='esrobo-link-check-') as folder:
        root = Path(folder)
        key = root / 'key'
        key.write_text(secrets.token_hex(32))
        base = [sys.executable, '-S', '-m', 'esrobo_link.gateway',
                '--key-file', str(key), '--port', '0']
        for side, hand_only in [('left', False), ('right', True), ('both', False)]:
            args = base + ['--side', side, '--with-hand', '--log-file', str(root / (side+'.jsonl'))]
            if hand_only:
                args.append('--hand-only')
            proc = subprocess.Popen(args, cwd=folder, env=env, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            client = None
            try:
                first = proc.stdout.readline()
                if not first:
                    raise RuntimeError(proc.stderr.read())
                listening = json.loads(first)['listening']
                client = RobotClient('127.0.0.1', listening[1], key)
                state = client.connect(timeout=3)
                assert state['mode'] == 'IDLE', state['mode']
                assert state['contract']['side'] == side
                proc.stdin.write('q\n')
                proc.stdin.flush()
                stdout, stderr = proc.communicate(timeout=5)
                assert proc.returncode == 0, stderr
                assert (root / (side+'.jsonl')).exists()
                print(f'PASS {side}: authenticated UDP handshake, IDLE, clean exit')
            finally:
                if client is not None:
                    client.socket.close()
                if proc.poll() is None:
                    proc.kill()
                    proc.communicate(timeout=5)
        missing = subprocess.run(base + ['--hardware', '--config', str(root/'unused.yaml')],
                                 cwd=folder, env=env, capture_output=True, text=True, timeout=5)
        assert missing.returncode == 2 and 'RUNTIME.md' in missing.stderr, missing.stderr
        assert not missing.stdout
        print('PASS missing hardware runtime: rejected before device initialization')


if __name__ == '__main__':
    main()
