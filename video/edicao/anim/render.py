#!/usr/bin/env python3
"""
Renderiza uma animação HTML (pages/<nome>.html) quadro a quadro com Playwright + ffmpeg.

Uso:
  render.py <nome> <duracao_s> <saida.mp4|saida.mov> [beats_json] [opções]

  beats_json : JSON inline ('{"decidir":2.4}') ou caminho de arquivo .json, com tempos ABSOLUTOS
               em segundos. Beats omitidos são escalados proporcionalmente à nova duração.
Opções:
  --alpha          fundo transparente; saída .mov QuickTime Animation (qtrle, argb)
  --prores         com --alpha: ProRes 4444 (yuva444p10le) em vez de qtrle
  --scale 0.5      resolução reduzida (teste)
  --stills 1,4.5   não gera vídeo: grava PNGs nesses tempos em <saida> (diretório)
  --fps 30
"""
import sys, json, subprocess, pathlib, argparse, time, base64

HERE = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nome'); ap.add_argument('dur', type=float); ap.add_argument('saida')
    ap.add_argument('beats', nargs='?', default=None)
    ap.add_argument('--alpha', action='store_true'); ap.add_argument('--prores', action='store_true')
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--stills', default=None)
    ap.add_argument('--fps', type=int, default=30)
    a = ap.parse_args()

    beats = None
    if a.beats:
        p = pathlib.Path(a.beats)
        beats = json.loads(p.read_text() if p.exists() else a.beats)
    page_path = HERE / 'pages' / f'{a.nome}.html'
    if not page_path.exists():
        sys.exit(f'página não encontrada: {page_path}')
    cfg = {'dur': a.dur, 'beats': beats, 'alpha': a.alpha}

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--force-color-profile=srgb', '--font-render-hinting=none',
                                      '--disable-lcd-text', '--hide-scrollbars'])
        pg = br.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1)
        pg.add_init_script(f'window.__ANIM = {json.dumps(cfg)};')
        pg.goto(page_path.as_uri())
        pg.evaluate('document.fonts.ready')
        pg.wait_for_function('typeof window.render === "function"')
        meta = pg.evaluate('window.META')
        print('beats:', json.dumps(meta.get('beats')), flush=True)
        cdp = pg.context.new_cdp_session(pg)

        def shot():
            r = cdp.send('Page.captureScreenshot', {'format': 'png', 'fromSurface': True,
                                                     'optimizeForSpeed': True,
                                                     'clip': {'x': 0, 'y': 0, 'width': 1920, 'height': 1080,
                                                              'scale': a.scale}})
            return base64.b64decode(r['data'])

        if a.alpha:
            cdp.send('Emulation.setDefaultBackgroundColorOverride', {'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}})

        if a.stills:
            out = pathlib.Path(a.saida); out.mkdir(parents=True, exist_ok=True)
            for ts in a.stills.split(','):
                t = float(ts)
                pg.evaluate(f'render({t})')
                (out / f'{a.nome}_{t:06.2f}.png').write_bytes(shot())
            br.close(); return

        n = int(round(a.dur * a.fps))
        out = pathlib.Path(a.saida); out.parent.mkdir(parents=True, exist_ok=True)
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(a.fps), '-c:v', 'png', '-i', '-']
        if a.alpha:
            if a.prores:
                cmd += ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']
            else:
                cmd += ['-c:v', 'qtrle', '-pix_fmt', 'argb']
        else:
            cmd += ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart']
        cmd += ['-r', str(a.fps), str(out)]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        t0 = time.time()
        for i in range(n):
            pg.evaluate(f'render({i / a.fps})')
            ff.stdin.write(shot())
            if i % 60 == 0:
                print(f'  {a.nome}: {i}/{n} ({time.time() - t0:.0f}s)', flush=True)
        ff.stdin.close(); ff.wait()
        br.close()
        print(f'ok {out} {n} quadros em {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()
