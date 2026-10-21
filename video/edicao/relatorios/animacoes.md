# Animações — relatório

Pasta: `/home/claude/edit/anim/` · saídas em `out/` · descrição de cada uma em `anim.json` (lido diretamente das páginas).

## Como funciona
- Cada animação é `pages/<nome>.html` (HTML/SVG/CSS + `common.css`/`common.js`) com `render(t)` determinística; não há transições CSS nem relógio.
- `render.py <nome> <duracao_s> <saida.mp4> [beats_json] [--alpha [--prores]] [--scale 0.5] [--stills t1,t2]`
  - Playwright captura cada quadro (CDP, PNG 1920×1080) e passa a imagem para o ffmpeg → H.264 crf 18 yuv420p 30 fps (`+faststart`).
  - **Duração:** os beats padrão são escalados por `duracao/duracao_padrao`. **beats_json** (inline ou arquivo) define tempos **absolutos** em segundos para os beats que você informar (os outros continuam escalados). Exemplo:
    `python3 render.py compensacao 19.5 out/compensacao.mp4 '{"sobe":3.1,"ganho":6.2,"acumula":9.8,"negativo":12.4,"margem":15.0}'`
  - `--alpha` gera .mov QuickTime Animation (qtrle, argb) com fundo transparente; `--prores` gera ProRes 4444 em vez de qtrle.
- `todas.sh` renderiza tudo com as durações padrão (≈5 min com 2 CPUs; cerca de 12 quadros/s). `gen_fw.py` gera `pages/fw.js` com as linhas **exatas** do `.ino` (os cartões de código leem dali, então os números de linha são os reais). `gen_meta.py` gera o `anim.json`.

## Entregas (1920×1080, 30 fps)
| id | arquivo | dur. | beats padrão (s) | selo |
|---|---|---|---|---|
| A1 | sistema.mp4 | 12 | medir .3 · decidir 2.8 · acionar 5.4 · realimentacao 8.2 | — |
| A2 | esquema.mp4 | 14 | sensor .4 · pwm 3.8 · potencia 7.4 · terra 10.6 | — |
| A3 | marca.mp4 | 14 | marca .3 · passagem 2.2 · rpm 6 · exemplo 9 | ILUSTRAÇÃO → EXEMPLO DIDÁTICO |
| A4 | limiares.mp4 | 14 | limites .3 · entrada 4 · saida 7.2 · ruido 10.2 | ILUSTRAÇÃO |
| A5 | codigo_leitura.mp4 | 8 | leitura .2 · bloco 3.4 · limites 4.8 | — |
| A6 | compensacao.mp4 | 22 | erro .3 · sobe 3.6 · ganho 7 · acumula 11 · negativo 14.2 · margem 17.4 | EXEMPLO DIDÁTICO |
| A7 | codigo_controle.mp4 | 16 | erro .6 · ajuste 4 · acumula 7.4 · margem 10.8 · limite 13.6 | — |
| A8 | legenda.mp4 + legenda_alpha.mov | 6 | desejado .2 · medido 1.9 · pwm 3.6 | — |
| A9 | titulo_alpha.mov + titulo_alpha.png | 5 | entra .2 · pergunta .9 · sai 4.3 | — |
| A10 | rotulos/*.png (50) | — | 10 rótulos × 5 variantes (sem seta, seta baixo/cima/esq/dir) | — |

**A9:** saiu como **.mov qtrle com canal alfa** (painel escuro translúcido rgba(15,25,40,.72) no canto inferior esquerdo, y 560–830, com fade de entrada e saída) **e** como PNG estático RGBA (quadro cheio, 1920×1080).
**A10:** PNG RGBA recortado no tamanho do conteúdo (com margem para a sombra). As setas são brancas com sombra, pensadas para ficar sobre o vídeo real. TCRT5000/ESP32/IRLZ44N/Modo RPM/Modo Percentual têm um ponto colorido (azul/laranja/roxo). "Trecho acelerado 2×" é uma pílula escura; "Exemplo didático" é uma pílula cinza, no estilo do selo.

## Conteúdo e decisões
- **A1:** cada cartão ganha um contorno colorido enquanto é o assunto (MEDIR em azul, DECIDIR em laranja, ACIONAR em roxo). A seta azul de realimentação sai do ACIONAR e volta ao MEDIR, com o texto "A velocidade medida volta ao controlador".
- **A2:** redesenho fiel do `02_esquema_gpio21.svg`, com as mesmas conexões, rótulos ampliados (26–34 px no SVG, maiores com o zoom) e fonte Inter. Coloquei 4 etapas em vez de 3, porque o "GND comum" ficou como etapa própria, com zoom de volta à visão geral e os dois GNDs destacados. Também entraram uma legenda de etapa (título de 56 px e subtítulo de 40 px) e um tracejado animado no trecho ativo. O restante fica a 25%. As notas de rodapé do SVG original foram removidas para liberar a faixa inferior.
- **A3:** rotor de 9 pás girando a 0,5 volta/s (lento de propósito, para ler); a primeira passagem acontece 0,4 s após o beat `passagem`. O contador sobe no centro de cada pulso. O valor 1800 RPM aparece em **azul**, porque é um RPM medido; no SVG original estava em laranja.
- **A4:** o traço é desenhado com interpolação suave entre pontos-chave. A contagem segue a mesma lógica do firmware: só conta abaixo de 1300 se `marcaPresente` for falso e só rearma acima de 2350. Os beats ancoram os cruzamentos: `entrada` é a 1ª contagem, `saida` o 1º rearme e `ruido` a 2ª contagem (o repique de ruído vem cerca de 0,5 s depois e fica marcado com "não conta"). As cores dos limites são vermelho (ENTRADA, #C8443A) e verde-azulado (SAIDA, #118B80); A5 usa as mesmas.
- **A5/A7:** mostram as linhas reais. O código está a 64 px na linha 120, a 40 px no bloco 123–130 e a 36 px no bloco 35–53 (a linha 41, com 75 caracteres, precisa caber). Em A7, as linhas fora do destaque ficam a 28% e o quadro rola até a região destacada. Acrescentei um 5º destaque, **linhas 45–46 (limite ±5 p.p./s)**, porque a narração da cena 6 fala disso.
- **A6:** a sequência é a do pedido, mais um encadeamento didático coerente com o firmware: 400 → +2 (50→52%), medido 1750 → +1,25 (53%), 1900 → +0,5 (54%), 2150 → erro −150 → −0,75 (53%), e no fim 2030 → erro −30, dentro de ±60, sem ajuste. Fecha com "1 pulso a mais em 1 s = 60 RPM · correção máx. ±5 p.p./s". Separei acumula e negativo em dois beats.
- **Regras gerais:** todo texto de leitura tem ≥ 40 px; o selo tem 30 px, de propósito discreto. Nenhum conteúdo passa de y = 900, exceto partes de painel sem texto em A2 durante o zoom. As cores são as da ESPEC. A animação usa só easing cúbico in/out, com deslocamentos ≤ 40 px.

## Verificação
Conferi PNGs de vários tempos de cada animação, inclusive quadros extraídos dos .mp4 finais, procurando sobreposição, corte e legibilidade. Corrigi: texto vazando do card (A3, A4), traço visível sobre o exemplo (A3), fórmula sobreposta à faixa de margem (A6) e salto de layout na borda ativa (A1). Também confirmei com ffprobe que todos os arquivos estão em 1920×1080 a 30 fps, que os .mov são qtrle argb com alfa real (pixel do canto = 0,0,0,0) e que a sobrescrita de beats funciona (teste `sistema 9 '{"realimentacao":6}'`).

## Limitações
- Durações muito curtas comprimem as transições, que têm tempo fixo de 0,5–1,2 s. Use pelo menos ~70% da duração padrão.
- Em A3 a rotação é lenta e não representa 30 voltas/s; isso fica claro pelo selo ILUSTRAÇÃO/EXEMPLO DIDÁTICO.
- `test/` guarda os quadros de verificação e pode ser apagada.
