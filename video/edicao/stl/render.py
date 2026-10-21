import sys, os, math, subprocess, threading, http.server, functools
from playwright.sync_api import sync_playwright

WORK = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/edit/stl/out'
mode = sys.argv[1]  # 'stills' | 'video' | 'test'

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WORK)
class Q(handler.func):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=WORK))
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

def ease(t):  # cosine ease in/out
    return 0.5 - 0.5 * math.cos(math.pi * t)

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.on('console', lambda m: print('console:', m.text))
    pg.goto(f'http://127.0.0.1:{port}/index.html')
    pg.wait_for_function('window.ready===true', timeout=60000)
    pg.evaluate('document.fonts.ready')

    def shot(path, theta, elev=17, dist=300):
        pg.evaluate(f'setView({theta},{elev},{dist})')
        pg.screenshot(path=path, type='png')

    if mode == 'test':
        for th in [0, 45, 90, 180, 270]:
            shot(f'{WORK}/test_{th}.png', th, 17, 320)
    elif mode == 'stills':
        shot(f'{OUT}/suporte_vista_frontal.png', -10, 16, 315)
        shot(f'{OUT}/suporte_vista_3-4.png', -38, 22, 320)
    elif mode == 'video':
        fps, dur = 30, 10.0
        n = int(fps * dur)
        hold = 0.6  # s parado no início e no fim
        th0, sweep = -35.0, 240.0
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-i', '-',
                               '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(fps),
                               '-movflags', '+faststart', f'{OUT}/suporte_turntable.mp4'], stdin=subprocess.PIPE)
        for i in range(n):
            t = i / fps
            u = min(max((t - hold) / (dur - 2 * hold), 0), 1)
            th = th0 + sweep * ease(u)
            d = abs(((th + 180) % 360) - 180)
            op = min(max((110 - d) / 30, 0), 1)
            pg.evaluate(f'setLegend({op:.3f});setView({th},17,320)')
            ff.stdin.write(pg.screenshot(type='png'))
            if i % 30 == 0: print('frame', i, round(th, 1), flush=True)
        ff.stdin.close(); ff.wait()
    b.close()
srv.shutdown()
