# RELATÓRIO — Render 3D do suporte (peça integral)

Entrada: `proj/mecanica/v1_original/stl/00_conjunto_integral_FIXO.stl` (1 884 triângulos, malha fechada/watertight, 1 corpo só, volume ≈ 22,3 cm³).

## Dimensões (bounding box, mm)
| Eixo | mín | máx | extensão |
|---|---|---|---|
| X | −32,9 | 32,9 | **65,8** |
| Y | −32,9 | 52,0 | **84,9** |
| Z | 0,0 | 31,6 | **31,6** |

Leitura da geometria (por cortes em Z):
- Moldura quadrada externa 65,8 × 65,8 mm, entre Z 10 e 28 (≈18 mm de profundidade), abertura interna ≈ 59 × 59 mm (para a ventoinha 58 × 58 × 15). Eixo da ventoinha = Z.
- Bloco de fixação no topo (Y 29–52) com furo passante de parafuso em X=0, Y≈42.
- Braço em Z 0–3 (lado Z−): placa com rasgo de ajuste (Y 36–48) e bloco com **bolsão retangular** em Y≈19 (raio ≈19 mm do centro = região das pás). → braço do sensor (frente).
- Braço em Z 28,5–31,6 (lado Z+): placa com rasgo e almofada plana 14 × 12 mm sem furo → braço traseiro (alvo branco da ideia original).

## Destaque (laranja #F0A050)
Destacada apenas a **cavidade do sensor**, identificada geometricamente: bolsão retangular de **10,4 × 5,4 mm** (Z 4,5–10, aberto para o lado da ventoinha) com janela passante menor de **8,8 × 3,4 mm** (Z 0–4,5) e degrau em Z=4,5. Compatível com o corpo do TCRT5000 (~10,2 × 5,8 mm). Foram coloridas só as 24 faces das paredes internas e do degrau (filtro por caixa |x|<5,3, 16,2<y<21,8, z<10 + normal horizontal ou degrau +Z); o resto da malha permanece no cinza-azulado #4F6A86. Nenhuma ventoinha, sensor ou peça extra foi desenhada. Legenda "cavidade do sensor" aparece sob o rótulo e some (fade) quando o lado do sensor fica de costas no turntable.

## Saídas (`/home/claude/edit/stl/out/`)
- `suporte_turntable.mp4` — 1920×1080, 30 fps, 10,0 s (300 quadros), H.264 crf 18 yuv420p. Giro de 240° (de −35° a +205°) com ease cosseno in/out e 0,6 s parado em cada ponta; câmera em perspectiva (FOV 26°, elevação 17°). Peça ocupa aprox. y 105–850 px; faixa y>900 livre.
- `suporte_vista_frontal.png` — lado do sensor (−10°, elevação 16°).
- `suporte_vista_3-4.png` — vista 3/4 (−38°, elevação 22°).
- Rótulo canto superior esquerdo: "Modelo 3D do suporte (peça integral)" (Inter 40 px, cartão branco).

## Como foi feito
three.js 0.160.0 + STLLoader em página local (`work/index.html`), servida por http local e renderizada quadro a quadro com Playwright/Chromium (SwiftShader), codificada com ffmpeg. Material MeshStandard fosco (roughness 0,85), luz hemisférica + key/fill/rim, sombra suave PCF num plano de sombra (ShadowMaterial 13%), arestas >30° com linhas finas escuras. A orientação mostra o bloco de fixação para cima (suposição de apresentação; o STL não define "cima").
Scripts: `work/render.py` (`test` | `stills` | `video`), malha dividida em `work/main.stl` + `work/cavity.stl` (mesmas coordenadas, centralizadas).
