#!/usr/bin/env python3
"""Gera rótulos (pílulas) PNG com alfa, cada um recortado no tamanho do conteúdo.
Variantes: <nome>.png (sem seta), <nome>_seta_baixo.png, <nome>_seta_cima.png,
<nome>_seta_esq.png, <nome>_seta_dir.png (seta aponta para fora da pílula).
Uso: rotulos.py [saida_dir]"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent / 'out' / 'rotulos')
OUT.mkdir(parents=True, exist_ok=True)
# (arquivo, texto, cor de destaque (bolinha) ou None, estilo)
R = [
    ('tcrt5000', 'TCRT5000', '#2478C8', 'claro'),
    ('esp32', 'ESP32', '#C66A16', 'claro'),
    ('irlz44n', 'IRLZ44N', '#8656B9', 'claro'),
    ('ventoinha_12v_2fios', 'Ventoinha 12 V · 2 fios', None, 'claro'),
    ('pa_marcada', 'Pá marcada', None, 'claro'),
    ('suporte_3d', 'Suporte impresso em 3D', None, 'claro'),
    ('modo_percentual', 'Modo Percentual', '#8656B9', 'claro'),
    ('modo_rpm', 'Modo RPM', '#C66A16', 'claro'),
    ('acelerado_2x', 'Trecho acelerado 2×', None, 'escuro'),
    ('exemplo_didatico', 'Exemplo didático', None, 'cinza'),
]
CSS = """
html,body{margin:0;background:transparent;font-family:Inter,sans-serif}
#w{display:inline-flex;align-items:center;padding:28px;}
#w.v{flex-direction:column} #w.h{flex-direction:row}
.p{display:inline-flex;align-items:center;gap:18px;padding:16px 36px;border-radius:999px;font-size:48px;font-weight:700;
   white-space:nowrap;box-shadow:0 6px 22px rgba(15,25,40,.28)}
.claro{background:#fff;color:#1B2A41;border:2px solid #D8E0EB}
.escuro{background:rgba(15,25,40,.85);color:#fff}
.cinza{background:#E2E7EE;color:#5B6B80;letter-spacing:.04em}
.d{width:22px;height:22px;border-radius:50%}
svg{display:block;filter:drop-shadow(0 4px 10px rgba(15,25,40,.3))}
"""
def arrow(direc, col):
    if direc in ('baixo', 'cima'):
        d = 'M30 4 V78 M10 58 L30 80 L50 58' if direc == 'baixo' else 'M30 86 V12 M10 32 L30 10 L50 32'
        return f'<svg width="60" height="90"><path d="{d}" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    d = 'M86 30 H12 M32 10 L10 30 L32 50' if direc == 'esq' else 'M4 30 H78 M58 10 L80 30 L58 50'
    return f'<svg width="90" height="60"><path d="{d}" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

with sync_playwright() as pw:
    br = pw.chromium.launch(args=['--force-color-profile=srgb'])
    pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    lista = []
    for nome, txt, cor, est in R:
        dot = f'<span class="d" style="background:{cor}"></span>' if cor else ''
        pill = f'<span class="p {est}">{dot}{txt}</span>'
        acol = '#FFFFFF' if est == 'escuro' else '#1B2A41'
        variantes = {'': pill,
                     '_seta_baixo': pill + arrow('baixo', '#FFFFFF'),
                     '_seta_cima': arrow('cima', '#FFFFFF') + pill,
                     '_seta_esq': arrow('esq', '#FFFFFF') + pill,
                     '_seta_dir': pill + arrow('dir', '#FFFFFF')}
        for suf, html in variantes.items():
            cls = 'v' if suf in ('_seta_baixo', '_seta_cima') else 'h'
            pg.set_content(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="w" class="{cls}">{html}</div></body></html>')
            pg.evaluate('document.fonts.ready')
            f = OUT / f'{nome}{suf}.png'
            pg.locator('#w').screenshot(path=str(f), omit_background=True)
            lista.append(f.name)
    br.close()
print(json.dumps(lista, ensure_ascii=False))
