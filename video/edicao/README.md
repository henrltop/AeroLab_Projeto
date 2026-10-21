# Projeto de edição — AeroLab

Fluxo: FFmpeg + animações HTML/SVG capturadas com Playwright/Chromium.

- `montar.py` — timeline completa (todos os planos, tempos, crops, rótulos). `python3 montar.py tudo`
- `anims.sh` — re-renderiza as animações com os tempos exatos da narração (usa `anim/render.py`).
- `anim/` — fontes das animações (páginas HTML em `pages/`, `render.py`).
- `stl/` — render do suporte a partir do STL integral (three.js).
- `overlays.py`, `ov/` — painel lateral da demonstração e cartão do repositório.
- `edl.json` / `timeline.json` — cortes da narração (arquivo original → editado) e tempos por frase.
- `legendas_video.srt` — legendas na timeline final (enviar ao YouTube). `legendas.ass` — estilo das legendas embutidas.
- `relatorios/` — análises de áudio, telas, celular, animações e STL.

Caminhos no script apontam para o ambiente onde foi renderizado (/home/claude/edit); ajuste `E` e `P` para rodar em outra máquina.
Mídias brutas ficam em `../entrada/` e renders em `../saida/` (fora do Git).
