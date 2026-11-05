#!/usr/bin/env python3
"""Re-theme previously patched Moza Studio/FigCraft (Rust/egui) to white + dusty rose.

No changes to FigCraft's engine, model, commands, file I/O, exporters, or Atelier.
Requires the Petal patch already applied to FigCraft. Backups are made once.
"""
from pathlib import Path
import argparse
import re
import shutil
import sys

F = 'crates/ui-egui/src/theme.rs'
HTML = 'apps/figcraft-web/index.html'

def rgb(hexcode):
    return ', '.join('0x'+hexcode[i:i+2] for i in (0,2,4))

def update(root):
    root=Path(root).expanduser().resolve()
    src=root/F
    html=root/HTML
    if not src.is_file() or not html.is_file():
        raise ValueError(f'Tidak menemukan file FigCraft di {root}. Pilih folder yang berisi Cargo.toml.')
    s=src.read_text(encoding='utf-8'); h=html.read_text(encoding='utf-8')
    if 'pub fn blush() -> Self {' not in s or ('Moza Studio' not in h and 'Petal Studio' not in h):
        raise ValueError('Dibutuhkan FigCraft yang sudah diberi patch Moza Studio sebelumnya. Script berhenti tanpa mengubah file.')
    # Browser-specific Rust constants only, leaving desktop's upstream constants untouched.
    for name,color in {'BRAND':'CC8593','ACCENT':'9F372A','ACCENT_ON':'FFFFFF'}.items():
        reg=r'(#\[cfg\(target_arch = "wasm32"\)\]\s*pub const '+name+r': Color32 = )Color32::from_rgb\([^;]+\);'
        replacement=lambda m,col=color:m.group(1)+'Color32::from_rgb('+rgb(col)+');'
        s,n=re.subn(reg,replacement,s)
        if n!=1: raise ValueError(f'Konstanta warna {name} tidak dikenali; tidak ada file yang disimpan.')
    start=s.index('    pub fn blush() -> Self {')
    end=s.find('    pub fn dark() -> Self {',start)
    if end==-1 or end-start>6000:raise ValueError('Fungsi theme blush berubah; berhenti demi keamanan.')
    tokens={
        'bg':'FFFFFF', 'panel':'FFFFFF', 'canvas':'FFF9FA', 'border':'E9D7DC', 'border_strong':'DAB6BE',
        'text':'603440', 'text_secondary':'865260', 'text_tertiary':'A3717E',
        'hover':'F8EBEE', 'pressed':'F2DCE1', 'field':'FFF9FA', 'field_hover_border':'D3A5B0',
        'accent_hover':'9F372A', 'selected_row':'F6E3E7', 'selected_row_child':'FFF5F7',
        'component':'CC8593', 'component_row':'F6E3E7', 'tab_bar':'F8EBEE','tab_active':'FFFFFF',
        'menu':'603440', 'menu_text':'FFFFFF', 'menu_hover':'B76E79', 'menu_dim':'E4C8D0','focus':'CC8593'
    }
    blush='''    /// Web theme: just white and dusty-rose colour families.\n    pub fn blush() -> Self {\n        let mut t = Self::light();\n'''
    for k,v in tokens.items():blush+=f'        t.{k} = Color32::from_rgb({rgb(v)});\n'
    blush+='''        t.icon = t.text;
        t.icon_secondary = t.text_secondary;
        t.accent = BRAND;
        t.accent_on = ACCENT_ON;
        t.accent_text = ACCENT;
        t
    }
'''
    s=s[:start]+blush+s[end:]
    # The tiny original Moza flower icon should use same two-tone palette.
    a=s.find('pub fn paint_app_icon(ui: &egui::Ui, rect: egui::Rect) {')
    b=s.find('pub fn regular(size: f32) -> FontId {',a)
    if 0<=a<b and b-a<4000:
        icon=s[a:b]
        icon=icon.replace('Color32::from_rgb(0xFA, 0xE5, 0xF1)','Color32::from_rgb(0xF8, 0xEB, 0xEE)')
        icon=icon.replace('Color32::from_rgb(0xCF, 0x73, 0xAE)','Color32::from_rgb(0xCC, 0x85, 0x93)')
        icon=icon.replace('Color32::from_rgb(0xFF, 0xDB, 0x83)','Color32::WHITE')
        s=s[:a]+icon+s[b:]
    # Rebrand only the user-facing Rust UI wordmark created by the previous patch.
    wm_old='painter.layout_no_wrap("Petal".into(), font.clone(), t.text)'
    wm_new='painter.layout_no_wrap("Moza".into(), font.clone(), t.text)'
    if wm_old in s:s=s.replace(wm_old,wm_new,1)
    # Only the web launch HTML: keep all WASM/Trunk scripts intact.
    oldcolors={'#fffafd':'#fffafa','#f7dbef':'#f5e3e8','#eee0ff':'#f7eaed','#efcfe5':'#e6cbd1','#49344d':'#603440',
               '#fae1ee':'#f6e3e7','#eedcff':'#f0d8df','#e99dc5':'#b76e79','#b59ded':'#a65f70','#8d718b':'#865260',
               '#f1deec':'#f2dce1','#a2799e':'#95616e','#733252':'#763e4c','#fff9fd':'#fffafa'}
    for old,new in oldcolors.items():h=re.sub(re.escape(old),new,h,flags=re.I)
    h=h.replace('Petal Studio','Moza Studio').replace('Petal Studio:','Moza Studio:')
    h=re.sub(r'data-wasm-opt="[^"]+"', 'data-wasm-opt="0"', h, count=1)
    for file,data,old in ((src,s,src.read_text(encoding='utf-8')),(html,h,html.read_text(encoding='utf-8'))):
        if data!=old:
            backup=file.with_name(file.name+'.before-fusion.bak')
            if not backup.exists():shutil.copy2(file,backup)
            file.write_text(data,encoding='utf-8')
            print('UPDATED',file)
        else:print('ALREADY CURRENT',file)
    print('Warna putih + dusty rose sudah diterapkan ke source. Build ulang untuk memperbarui file .wasm.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Petal x Atelier FigCraft retint tool')
    p.add_argument('figcraft',help='Path folder source FigCraft yang berisi Cargo.toml')
    args=p.parse_args()
    try:update(args.figcraft)
    except Exception as ex:print('ERROR:',ex,file=sys.stderr);sys.exit(1)
