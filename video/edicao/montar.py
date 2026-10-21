"""Montagem do vídeo AeroLab (FFmpeg).

Uso: python3 montar.py [segmentos|audio|final|tudo] [--so N,M]
Cada plano vira um segmento 1920x1080/30 fps sem áudio; depois concatena,
junta a narração e queima as legendas.
Tempos de vídeo (V) = tempos da narração editada nas cenas 1-6; cena 7 é
reconstruída sobre a demonstração e a cena 8 é deslocada em SHIFT8 s.
"""
import json, os, subprocess, sys

E = "/home/claude/edit"
P = f"{E}/proj/video/entrada"
OUT = f"{E}/build"
os.makedirs(f"{OUT}/seg", exist_ok=True)
BG = "0xF4F6FA"

TELA = {
    "A": f"{P}/cideo mostrando a ventoinha sendo contraolada pela PWM colocando em 100%.mp4",
    "B": f"{P}/gravação tela controlando temperatura (video q mostra eu controlando a temperatura q sincroniza com o video gravado do celular).mp4",
    "C": f"{P}/video mostrando a ventoinha a 1600 RPM e indo para 2000 RPM e dps indo para 100 RMP.mp4",
}
CEL = {
    "084854": f"{P}/20261021_084854.mp4",
    "091353": f"{P}/20261021_091353.mp4",
    "091629": f"{P}/20261021_091629.mp4",
}
# crops das telas (x,y,w,h); C tem layout 6 px acima
CROP = {
    "dados": (272, 262, 1578, 888),
    "grafico": (269, 450, 1244, 700),
    "controle": (1080, 540, 816, 459),
}
DY = {"A": 0, "B": 0, "C": -6}
# regiões a desfocar (barra do navegador com caminho de usuário e barra de tarefas) nos planos do celular
BLUR = {
    "091629": [(920, 110, 1000, 95), (920, 690, 1000, 105)],
    "091353": [(860, 160, 1060, 70), (860, 715, 1060, 85)],
}
# recorte da ventoinha para o PiP (4:3) e offset celular_t = tela_t + off
PIP = {
    "A": ("091629", 0.68, (180, 756, 432, 324)),
    "B": ("084854", 0.68, (700, 440, 720, 540)),
    "C": ("091353", 0.31, (120, 740, 432, 324)),
}
ROT = f"{E}/anim/out/rotulos"
AF = f"{E}/anim/final"
OV = f"{E}/src/ov"


def cel(nome, t):
    """Fonte e tempo para clipes do celular (085323 só existe em duas metades)."""
    if nome == "085323":
        return (f"{P}/proxy/085323_p0.mp4", t) if t < 65 else (f"{P}/proxy/085323_p1.mp4", t - 65)
    return CEL[nome], t


# ---------------- TIMELINE ----------------
# tipos: cel (clipe do celular), tela (crop em tela cheia), demo (tela + PiP + painel lateral),
#        anim (trecho de animação renderizada), stl (turntable), still (imagem com zoom lento)
T = []


def add(v0, v1, **kw):
    T.append(dict(v0=v0, v1=v1, **kw))


# CENA 1 — resultado primeiro
add(0.00, 5.30, tipo="cel", src="084854", i=39.8, ov=[("TITULO", 0.3, None)])
add(5.30, 10.31, tipo="tela", src="A", i=14.4, crop="grafico")
add(10.31, 16.00, tipo="cel", src="084854", i=13.0)
add(16.00, 22.17, tipo="cel", src="091629", i=13.0, blur=True)
# CENA 2 — mede, decide, aciona
add(22.17, 27.15, tipo="anim", nome="sistema", a0=22.17)
add(27.15, 32.95, tipo="cel", src="085323", i=91.9, ov=[("tcrt5000", 0.3, 5.5)])
add(32.95, 37.20, tipo="cel", src="085323", i=0.5, ov=[("ventoinha_12v_2fios", 0.3, 4.0)])
add(37.20, 39.96, tipo="cel", src="085323", i=69.5, ov=[("esp32", 0.2, 2.6)])
add(39.96, 42.46, tipo="cel", src="085323", i=78.9, ov=[("irlz44n", 0.2, 2.5)])
add(42.46, 44.06, tipo="cel", src="085323", i=82.3, ov=[("irlz44n", 0.0, 1.5)])
add(44.06, 48.68, tipo="cel", src="084854", i=67.0)
add(48.68, 62.45, tipo="anim", nome="esquema", a0=48.68)
# CENA 3 — marca vira volta
add(62.45, 66.06, tipo="cel", src="085323", i=39.5, ov=[("pa_marcada", 0.3, 3.5)])
add(66.06, 69.50, tipo="cel", src="085323", i=55.5, ov=[("pa_marcada", 0.0, 3.3)])
add(69.50, 90.36, tipo="anim", nome="marca", a0=69.50)
add(90.36, 95.30, tipo="cel", src="091629", i=20.0, blur=True)
# CENA 4 — suporte e leitura
add(95.30, 101.30, tipo="cel", src="085323", i=20.0, ov=[("suporte_3d", 0.3, 5.8)])
add(101.30, 110.96, tipo="stl")
add(110.96, 119.13, tipo="anim", nome="codigo_leitura", a0=110.96)
add(119.13, 134.51, tipo="anim", nome="limiares", a0=119.13)
# CENA 5 — dois modos
add(134.51, 137.66, tipo="cel", src="091353", i=20.0, blur=True)
add(137.66, 144.20, tipo="tela", src="A", i=3.0, crop="controle", ov=[("modo_percentual", 0.3, 6.3)])
add(144.20, 150.39, tipo="tela", src="A", i=14.0, crop="dados")
add(150.39, 157.77, tipo="tela", src="C", i=15.6, crop="controle", ov=[("modo_rpm", 0.3, 7.2)])
# CENA 6 — compensação (dois arquivos renderizados sobre a mesma janela 157.77–209.27)
add(157.77, 171.30, tipo="anim", nome="compensacao", a0=157.77)
add(171.30, 178.38, tipo="anim", nome="codigo_controle", a0=157.77)
add(178.38, 203.58, tipo="anim", nome="compensacao", a0=157.77)
add(203.58, 209.27, tipo="anim", nome="codigo_controle", a0=157.77)
# CENA 7 — demonstração real (tempos em 1x)
add(209.27, 212.27, tipo="cel", src="091629", i=11.0, blur=True)
add(212.27, 219.97, tipo="demo", src="A", i=13.0)
add(219.97, 234.97, tipo="demo", src="B", i=39.0)
add(234.97, 244.97, tipo="demo", src="B", i=56.0)
add(244.97, 259.97, tipo="demo", src="C", i=45.0)
# CENA 8 — encerramento
add(259.97, 266.57, tipo="cel", src="084854", i=80.5)
add(266.57, 274.85, tipo="tela", src="B", i=66.0, crop="grafico")
add(274.85, 280.17, tipo="still", img=f"{E}/stl/out/suporte_vista_3-4.png", ov=[("REPO", 0.4, None)])
add(280.17, 284.60, tipo="cel", src="091353", i=55.0, fadeout=1.2)

INS = [(12, 62.45, 8.0, dict(v0=0, v1=8.0, tipo="img", img=f"{OV}/circuito.png"))]
DUR = T[-1]["v1"]
SHIFT8 = 16.85
C7 = [("c7_01", 209.77), ("c7_02", 212.60), ("c7_03", 220.00), ("c7_04", 224.00),
      ("c7_05", 235.60), ("c7_06", 245.30), ("c7_07", 250.60)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(cmd)[:3000]); print(r.stderr[-3000:]); raise SystemExit(1)


def label_inputs(ov, dur, inputs, chain, base):
    """Sobreposições com fade de alfa. Retorna o rótulo final do stream."""
    cur = base
    for k, (nome, t0, t1) in enumerate(ov or []):
        idx = inputs.count("-i")
        if nome == "TITULO":
            inputs += ["-i", f"{E}/anim/out/titulo_alpha.mov"]
            chain.append(f"[{idx}:v]format=rgba,setpts=PTS+{t0}/TB[o{k}]")
            chain.append(f"[{cur}][o{k}]overlay=0:0:eof_action=pass[v{k}]")
        elif nome == "REPO":
            inputs += ["-loop", "1", "-t", f"{dur}", "-i", f"{OV}/repo_card.png"]
            chain.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0}:d=0.4:alpha=1[o{k}]")
            chain.append(f"[{cur}][o{k}]overlay=0:0[v{k}]")
        else:
            t1 = min(t1, dur - 0.05)
            inputs += ["-loop", "1", "-t", f"{dur}", "-i", f"{ROT}/{nome}.png"]
            chain.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0}:d=0.3:alpha=1,"
                         f"fade=t=out:st={max(t0 + 0.3, t1 - 0.3)}:d=0.3:alpha=1[o{k}]")
            chain.append(f"[{cur}][o{k}]overlay=56:52:shortest=1[v{k}]")
        cur = f"v{k}"
    return cur


def blur_chain(src_key, chain, cur):
    for k, (x, y, w, h) in enumerate(BLUR.get(src_key, [])):
        chain.append(f"[{cur}]split[bA{k}][bB{k}]")
        chain.append(f"[bB{k}]crop={w}:{h}:{x}:{y},boxblur=lr=30:lp=3:cr=15:cp=3[bC{k}]")
        chain.append(f"[bA{k}][bC{k}]overlay={x}:{y}[bD{k}]")
        cur = f"bD{k}"
    return cur


def segmento(n, s):
    dur = round(s["v1"] - s["v0"], 3)
    out = f"{OUT}/seg/{n:03d}.mp4"
    inputs, chain = [], []
    t = s["tipo"]
    if t == "cel":
        f, i = cel(s["src"], s["i"])
        inputs += ["-ss", f"{i}", "-t", f"{dur + 0.2}", "-i", f]
        chain.append(f"[0:v]fps=30,scale=1920:1080:flags=lanczos,setsar=1[b0]")
        cur = blur_chain(s["src"], chain, "b0") if s.get("blur") else "b0"
    elif t == "tela":
        x, y, w, h = CROP[s["crop"]]; y += DY[s["src"]]
        inputs += ["-ss", f"{s['i']}", "-t", f"{dur + 0.2}", "-i", TELA[s["src"]]]
        chain.append(f"[0:v]fps=30,crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,setsar=1[b0]")
        cur = "b0"
    elif t == "demo":
        x, y, w, h = CROP["dados"]; y += DY[s["src"]]
        cn, off, (px, py, pw, ph) = PIP[s["src"]]
        f, ci = cel(cn, s["i"] + off)
        inputs += ["-ss", f"{s['i']}", "-t", f"{dur + 0.2}", "-i", TELA[s["src"]],
                   "-ss", f"{ci}", "-t", f"{dur + 0.2}", "-i", f,
                   "-loop", "1", "-t", f"{dur + 0.2}", "-i", f"{OV}/demo_lateral.png"]
        chain.append(f"color=c={BG}:s=1920x1080:r=30:d={dur + 0.2}[bg]")
        chain.append(f"[0:v]fps=30,crop={w}:{h}:{x}:{y},scale=1480:833:flags=lanczos,setsar=1,"
                     f"pad=1484:837:2:2:color=0xD5DCE6[sc]")
        chain.append(f"[1:v]fps=30,crop={pw}:{ph}:{px}:{py},scale=368:276:flags=lanczos,setsar=1,"
                     f"pad=372:280:2:2:color=0xD5DCE6[pp]")
        chain.append("[bg][sc]overlay=22:38[t1]")
        chain.append("[t1][pp]overlay=1526:38[t2]")
        chain.append("[2:v]format=rgba[lat]")
        chain.append("[t2][lat]overlay=0:0[b0]")
        cur = "b0"
    elif t == "anim":
        inputs += ["-ss", f"{s['v0'] - s['a0']}", "-t", f"{dur + 0.2}", "-i", f"{AF}/{s['nome']}.mp4"]
        chain.append("[0:v]fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1[b0]")
        cur = "b0"
    elif t == "stl":
        inputs += ["-i", f"{E}/stl/out/suporte_turntable.mp4"]
        chain.append(f"[0:v]setpts=PTS*{dur / 10.0},fps=30,setsar=1,tpad=stop_mode=clone:stop_duration=1[b0]")
        cur = "b0"
    elif t == "img":
        inputs += ["-loop", "1", "-t", f"{dur + 0.2}", "-i", s["img"]]
        chain.append("[0:v]fps=30,scale=1920:1080,setsar=1[b0]")
        cur = "b0"
    elif t == "still":
        fr = int(dur * 30) + 6
        inputs += ["-loop", "1", "-t", f"{dur + 0.2}", "-i", s["img"]]
        chain.append(f"[0:v]scale=3840:2160,zoompan=z='1+0.05*on/{fr}':x='iw/2-(iw/zoom/2)-iw*0.12*on/{fr}':"
                     f"y='ih/2-(ih/zoom/2)':d={fr}:s=1920x1080:fps=30,setsar=1[b0]")
        cur = "b0"
    cur = label_inputs(s.get("ov"), dur, inputs, chain, cur)
    fo = s.get("fadeout")
    tail = f",fade=t=out:st={dur - fo}:d={fo}" if fo else ""
    if n == 0:
        tail += ",fade=t=in:st=0:d=0.4"
    chain.append(f"[{cur}]trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p{tail}[out]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(chain),
           "-map", "[out]", "-an", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
           "-pix_fmt", "yuv420p", "-video_track_timescale", "15360", out]
    run(cmd)
    return out


def segmentos(so=None):
    for n, s in enumerate(T):
        if so and n not in so:
            continue
        segmento(n, s)
        print(f"seg {n:03d} {s['tipo']:6s} {s['v0']:7.2f}-{s['v1']:7.2f} ok", flush=True)
    for k, (_, _, _, seg) in enumerate(INS):
        if so and (900 + k) not in so:
            continue
        segmento(900 + k, seg); print(f"ins {k} ok", flush=True)
    with open(f"{OUT}/lista.txt", "w") as fh:
        for n in range(len(T)):
            for k, (antes, _, _, _) in enumerate(INS):
                if antes == n:
                    fh.write(f"file 'seg/{900 + k:03d}.mp4'\n")
            fh.write(f"file 'seg/{n:03d}.mp4'\n")


def audio():
    A = f"{E}/audio"
    rt = f"{A}/roomtone_30s.wav"
    # base: narração até 209.27; cena 7 = room tone + frases; cena 8 deslocada; cauda room tone
    inputs = ["-i", f"{A}/narracao_editada_rt.wav", "-stream_loop", "-1", "-i", rt]
    ch = [f"[0:a]atrim=0:209.27,asetpts=PTS-STARTPTS[p1]",
          f"[1:a]atrim=0:{DUR - 209.27 + 1},asetpts=PTS-STARTPTS,volume=1[bed]",
          f"[0:a]atrim=start=243.62,asetpts=PTS-STARTPTS[p8]"]
    mix = ["[bed]"]
    for k, (nome, v) in enumerate(C7):
        inputs += ["-i", f"{A}/frases/{nome}.wav"]
        d = int((v - 209.27) * 1000)
        ch.append(f"[{k + 2}:a]adelay={d}:all=1[f{k}]")
        mix.append(f"[f{k}]")
    # trecho da cena 8 sobre o leito (substitui o room tone no mesmo nível)
    d8 = int((243.62 + SHIFT8 - 209.27) * 1000)
    ch.append(f"[p8]adelay={d8}:all=1[p8d]")
    # silenciar o leito onde entra p8 para não somar ruído
    ch.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first[m7]")
    ch.append(f"[m7]volume='if(gte(t,{(243.62 + SHIFT8 - 209.27):.3f}),0,1)':eval=frame[m7b]")
    ch.append("[m7b][p8d]amix=inputs=2:normalize=0:duration=first[m78]")
    ch.append(f"[p1][m78]concat=n=2:v=0:a=1,atrim=0:{DUR},afade=t=out:st={DUR - 1.2}:d=1.2,"
              f"aformat=sample_rates=48000:channel_layouts=stereo[a]")
    run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(ch),
         "-map", "[a]", "-c:a", "pcm_s16le", f"{OUT}/audio_base.wav"])
    # inserções: room tone no ponto de cada inserção (sem narração)
    ch, ins, ini = [], ["-i", f"{OUT}/audio_base.wav", "-stream_loop", "-1", "-i", rt], 0.0
    partes = []
    for k, (_, at, d, _) in enumerate(INS):
        ch.append(f"[0:a]atrim={ini}:{at},asetpts=PTS-STARTPTS[a{k}]")
        ch.append(f"[1:a]atrim=0:{d},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[r{k}]")
        partes += [f"[a{k}]", f"[r{k}]"]; ini = at
    ch.append(f"[0:a]atrim=start={ini},asetpts=PTS-STARTPTS[az]"); partes.append("[az]")
    ch.append(f"{''.join(partes)}concat=n={len(partes)}:v=0:a=1[a]")
    run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(ch),
         "-map", "[a]", "-c:a", "pcm_s16le", f"{OUT}/audio_final.wav"])
    print("audio ok")


def legendas():
    """Reposiciona o SRT (tempos da narração editada) na timeline do vídeo e gera ASS."""
    import re
    tl = json.load(open(f"{E}/audio/timeline.json"))
    f7 = [f for c in tl["cenas"] if c["cena"] == 7 for f in c["frases"]]
    def remap(t):
        if t < 209.27:
            return t
        if t >= 243.62:
            return t + SHIFT8
        for (nome, v), f in zip(C7, f7):
            if t <= f["fim_s"] + 0.3:
                return v + (t - f["inicio_s"])
        return t
    txt = open(f"{E}/audio/legendas.srt", encoding="utf-8").read().strip()
    blocos = re.split(r"\n\s*\n", txt)
    def ts(s):
        h, m, r = s.split(":"); sec, ms = r.split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
    def fmt_srt(t):
        ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
    def fmt_ass(t):
        cs = int(round(t * 100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"
    srt, ass = [], []
    for k, b in enumerate(blocos):
        ls = b.splitlines()
        a, z = [ts(x.strip()) for x in ls[1].split("-->")]
        a2, z2 = remap(a), remap(z)
        a2 += sum(d for (_, at, d, _) in INS if a >= at); z2 += sum(d for (_, at, d, _) in INS if a >= at)
        if z2 - a2 > 7 or z2 <= a2:  # bloco atravessou o corte da cena 7: usa duração original
            z2 = a2 + (z - a)
        texto = ls[2:]
        srt.append(f"{k + 1}\n{fmt_srt(a2)} --> {fmt_srt(z2)}\n" + "\n".join(texto))
        ass.append(f"Dialogue: 0,{fmt_ass(a2)},{fmt_ass(z2)},L,,0,0,0,,{'\\N'.join(texto)}")
    open(f"{OUT}/legendas_video.srt", "w", encoding="utf-8").write("\n\n".join(srt) + "\n")
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Inter SemiBold,46,&H00FFFFFF,&H00FFFFFF,&H5A121A26,&H00000000,0,0,0,0,100,100,0,0,3,14,0,2,120,120,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    open(f"{OUT}/legendas.ass", "w", encoding="utf-8").write(head + "\n".join(ass) + "\n")
    print("legendas", len(ass))


def final():
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{OUT}/lista.txt",
         "-c", "copy", f"{OUT}/video_sem_audio.mp4"])
    legendas()
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/video_sem_audio.mp4", "-i", f"{OUT}/audio_final.wav",
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
         "-movflags", "+faststart", f"{OUT}/AeroLab_sem_legenda.mp4"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/AeroLab_sem_legenda.mp4",
         "-vf", f"ass={OUT}/legendas.ass:fontsdir=/usr/share/fonts/opentype/inter",
         "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
         "-c:a", "copy", "-movflags", "+faststart", f"{OUT}/AeroLab_com_legenda.mp4"])
    print("final ok")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    so = None
    if "--so" in sys.argv:
        so = {int(x) for x in sys.argv[sys.argv.index("--so") + 1].split(",")}
    if modo in ("segmentos", "tudo"):
        segmentos(so)
    if modo in ("audio", "tudo"):
        audio()
    if modo in ("legendas",):
        legendas()
    if modo in ("final", "tudo"):
        final()
