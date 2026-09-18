"""Verify the six locally acquired GGUF model files against Appendix A."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models-dir',type=Path,default=ROOT/'.runtime/rag-app/models')
    args=parser.parse_args()
    records=json.loads((ROOT/'provenance/models.json').read_text())
    failures=[]
    for r in records:
        path=args.models_dir/r['filename']
        if not path.is_file():
            failures.append(r['config']);print(f"MISSING {r['config']}: {path}\nSource: {r['url']}");continue
        digest=hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''):digest.update(block)
        ok=digest.hexdigest()==r['sha256']
        print(f"{'PASS' if ok else 'HASH MISMATCH'} {r['config']}: {path.name}")
        if not ok:failures.append(r['config'])
    if failures:raise SystemExit('Not ready: '+', '.join(failures))


if __name__=='__main__':main()
