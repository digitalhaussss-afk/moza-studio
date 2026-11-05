#!/usr/bin/env python3
"""Copy an existing FigCraft Trunk build under /web and produce a deployable ZIP.
Doesn't alter the editor binary or the separate Atelier editor.
"""
from pathlib import Path
import argparse,shutil,zipfile,sys

HERE=Path(__file__).resolve().parent.parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('dist',help='FigCraft build output folder e.g. figcraft/dist/web')
    p.add_argument('--output',default=None,help='Optional output zip path')
    args=p.parse_args()
    src=Path(args.dist).expanduser().resolve()
    if not src.is_dir() or not (src/'index.html').exists() or not list(src.glob('*.wasm')) or not list(src.glob('*.js')):
        print('ERROR: pilih folder dist/web yang berisi index.html, *.wasm, *.js',file=sys.stderr);return 2
    dest=HERE/'web'
    if src==dest or dest in src.parents:
        print('ERROR: folder sumber/destinasi tidak boleh sama/bersarang',file=sys.stderr);return 2
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(src,dest,ignore=shutil.ignore_patterns('.trunk-lock'))
    if 'figcraft_canvas' not in (dest/'index.html').read_text(encoding='utf-8',errors='replace'):
        print('WARNING: index.html tidak memuat marker canvas FigCraft; cek kompatibilitas build.')
    output=Path(args.output).expanduser().resolve() if args.output else HERE.parent/'Moza_Studio_Complete_Deploy.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for f in HERE.rglob('*'):
            if not f.is_file() or '.bak' in f.name:continue
            z.write(f,f.relative_to(HERE).as_posix())
    print('SUCCESS: FigCraft + Atelier assembled at:',output)
    print('Upload extracted contents of ZIP to GitHub Pages root/Netlify.')
    return 0
if __name__=='__main__':sys.exit(main())
