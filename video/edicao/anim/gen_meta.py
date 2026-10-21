#!/usr/bin/env python3
"""Gera anim.json lendo os beats padrão diretamente de cada página (window.META)."""
import json, pathlib
from playwright.sync_api import sync_playwright
H = pathlib.Path(__file__).resolve().parent
A = [
 ('A1', 'sistema', 'Três cartões MEDIR/DECIDIR/ACIONAR e seta de realimentação', None, ['out/sistema.mp4']),
 ('A2', 'esquema', 'Esquema GPIO4/GPIO21 com destaque por etapas e zoom (restante esmaecido a 25%)', None, ['out/esquema.mp4']),
 ('A3', 'marca', 'Rotor de 9 pás com 1 pá marcada, pulsos e contador; depois 30 × 60 = 1800 RPM', 'ILUSTRAÇÃO → EXEMPLO DIDÁTICO no beat "exemplo"', ['out/marca.mp4']),
 ('A4', 'limiares', 'Sinal analógico idealizado com limites 1300/2350, contagem, rearme e ruído ignorado', 'ILUSTRAÇÃO', ['out/limiares.mp4']),
 ('A5', 'codigo_leitura', 'Linha 120 (analogRead) e bloco 123–130 com LIMITE_ENTRADA/LIMITE_SAIDA destacados', None, ['out/codigo_leitura.mp4']),
 ('A6', 'compensacao', 'Desejado − medido = erro; PWM ↑; 400 × 0,005 = +2 p.p.; acumula; erro negativo; margem ±60 / máx ±5 p.p./s', 'EXEMPLO DIDÁTICO', ['out/compensacao.mp4']),
 ('A7', 'codigo_controle', 'controlarRPM() linhas 35–53 com destaque 38 → 43 → 48–49 → 41 → 45–46', None, ['out/codigo_controle.mp4']),
 ('A8', 'legenda', 'Legenda das cores do gráfico (fundo cheio e versão com alfa sem título)', None, ['out/legenda.mp4', 'out/legenda_alpha.mov']),
 ('A9', 'titulo', 'Cartão de abertura translúcido para sobrepor ao vídeo (canto inferior esquerdo, acima de y=900)', None, ['out/titulo_alpha.mov', 'out/titulo_alpha.png']),
]
res = {'formato': '1920x1080, 30 fps; .mp4 = H.264 crf 18 yuv420p; .mov alfa = QuickTime Animation (qtrle, argb)',
       'rerender': {
           'comando': 'python3 render.py <nome> <duracao_s> <saida.mp4> [beats_json] [--alpha [--prores]]',
           'beats': 'beats omitidos são escalados proporcionalmente (beat_padrao × duracao/duracao_padrao); beats passados no JSON são tempos ABSOLUTOS em segundos. Ex.: python3 render.py sistema 10.4 out/sistema.mp4 \'{"decidir":2.1,"acionar":4.6,"realimentacao":7.0}\'',
           'teste_rapido': 'python3 render.py <nome> <dur> pasta/ --stills 1,5,9 --scale 0.5',
           'todas': './todas.sh  (ou ./todas.sh marca limiares)'},
       'animacoes': []}
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1920, 'height': 1080})
    for cod, nome, desc, selo, arqs in A:
        pg.goto((H / 'pages' / f'{nome}.html').as_uri()); pg.wait_for_function('window.META')
        m = pg.evaluate('window.META')
        res['animacoes'].append({'id': cod, 'nome': nome, 'arquivos': arqs, 'duracao_padrao_s': m['defDur'],
                                 'beats_padrao_s': m['defBeats'], 'selo': selo, 'descricao': desc,
                                 'alfa': any(a.endswith('.mov') for a in arqs)})
    br.close()
res['animacoes'].append({'id': 'A10', 'nome': 'rotulos', 'arquivos': 'out/rotulos/*.png (50 arquivos)',
    'descricao': 'Pílulas PNG RGBA recortadas no tamanho do conteúdo; para cada rótulo: <nome>.png, <nome>_seta_baixo/_seta_cima/_seta_esq/_seta_dir.png (seta branca com sombra apontando para fora)',
    'rotulos': ['tcrt5000', 'esp32', 'irlz44n', 'ventoinha_12v_2fios', 'pa_marcada', 'suporte_3d', 'modo_percentual', 'modo_rpm', 'acelerado_2x', 'exemplo_didatico'],
    'rerender': 'python3 rotulos.py out/rotulos'})
(H / 'anim.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
print('ok')
