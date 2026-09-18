"""Restore and check the exact four PDF bytes used by the final benchmark.

Downloads D1 from arXiv; D2/D3/D4 are retained snapshots with reuse notices.
A changed upstream file is rejected, never silently used as the original corpus.
"""
import argparse
import hashlib
import json
from pathlib import Path
import ssl
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--corpus-dir', type=Path, default=ROOT/'corpus')
    args = parser.parse_args()
    records = json.loads((ROOT/'corpus/manifest.json').read_text())
    args.corpus_dir.mkdir(parents=True, exist_ok=True)
    for r in sorted(records,key=lambda r:r['source_id']):
        path=args.corpus_dir/r['output']
        if not path.exists():
            if args.check_only:
                raise SystemExit(f'MISSING: {path}')
            if r['download_url']:
                print(f"Downloading {r['source_id']} from {r['download_url']}",flush=True)
                req=urllib.request.Request(r['download_url'],headers={'User-Agent':'Dissertation-reproduction/1.0'})
                with urllib.request.urlopen(req,timeout=90,context=ssl.create_default_context()) as response:
                    data=response.read()
            else:
                data=(ROOT/'corpus'/r['output']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=r['sha256']:
                raise SystemExit(f"HASH MISMATCH: {r['source_id']}; upstream differs from the retained benchmark. Do not substitute it for the original.")
            path.write_bytes(data)
        if hashlib.sha256(path.read_bytes()).hexdigest()!=r['sha256']:
            raise SystemExit(f'HASH MISMATCH: {path}; preserve it and inspect the provenance before rerunning.')
        print(f"PASS {r['source_id']}: {r['sha256']}")


if __name__=='__main__':
    main()
