# O que gravar — passo a passo

**Regra geral:** grave primeiro as **imagens**, sem se preocupar com o áudio (pode ficar em silêncio; o som ambiente será descartado). Depois grave a **narração** separada, lendo `narracao.txt`. A cena 7 é narrada assistindo à gravação da demonstração.

Coloque tudo em `video/entrada/` com os nomes abaixo. Celular sempre **na horizontal**, 1080p, 30 fps, foco travado (toque e segure na tela). Grave cada plano com 3–5 s sobrando no começo e no fim.

## Parte A — Imagens da bancada (≈ 15 min)

| Arquivo | O que mostrar | Duração | Como |
|---|---|---|---|
| `V05a_pa_marcada.mp4` | Ventoinha **desligada**, close da pá marcada; gire devagar com o dedo até a marca parar na frente do sensor | 15 s | Bem perto, luz forte de lado |
| `V05b_sensor_suporte.mp4` | Sensor encaixado no suporte, de frente para as pás | 10 s | Movimento lento de um lado para o outro |
| `V05c_suporte_inteiro.mp4` | Suporte impresso com a ventoinha, dando a volta na peça | 15 s | Volta lenta, ou gire a peça na mão |
| `V06_conexoes.mp4` | ESP32 → IRLZ44N → resistores → fios do sensor e da fonte | 20 s | Panorâmica lenta, parando 2 s em cada componente |
| `V01_funcionando.mp4` | Plano geral: montagem + notebook com o painel, ventoinha girando | 20 s | Tripé ou celular apoiado, sem mexer |
| `V04_final.mp4` | Montagem completa, ventoinha girando, câmera se afastando devagar | 10 s | Pode ser o mesmo enquadramento do V01 |

Fotos também servem (`foto_*.jpg`) se o vídeo tremer: ESP32, IRLZ44N, montagem vista de cima.

## Parte B — Demonstração (o mais importante)

Duas gravações **ao mesmo tempo**:

1. **Tela** → `V03_tela.mp4`: Chrome em tela cheia com o painel conectado. No Windows, use **Win+Alt+R** (Barra de Jogos) ou o OBS. Janela do gráfico em 60 s.
2. **Celular** → `V03_ventoinha.mp4`: celular parado, mostrando a ventoinha (e, se der, o notebook ao fundo).

Antes de começar: inicie as duas gravações e **bata uma palma** perto do notebook (serve para sincronizar).

Roteiro de cliques (sem falar nada):

1. Modo **Percentual** → aplicar um valor que você já testou (ex.: o que der rotação média) → **espere 15 s**.
2. Aplicar outro percentual → **espere 15 s**.
3. Trocar para o modo **RPM** → aplicar um alvo que a ventoinha atinge → **espere 20 s**.
4. Aplicar outro alvo (subir ou descer uns 300–500 RPM) → **espere 20 s**.
5. Parar.

Mexa o mouse só para clicar. Não esconda a legenda do gráfico. Se algo der errado, grave de novo inteiro: são só 2 minutos.

## Parte C — Narração (≈ 15 min)

- Leia `narracao.txt`, **um arquivo por cena**: `cena1.wav` … `cena8.wav` (m4a do celular também serve).
- Celular a ~20 cm da boca, quarto com cortina/roupas por perto, ventoinha e ventilador **desligados**.
- Fale no seu ritmo normal. Deixe **1 s de silêncio entre parágrafos**.
- Errou? Pare, respire e repita a frase inteira. Eu corto o erro.
- **Cena 7:** abra `V03_tela.mp4` e narre enquanto assiste, falando cada frase quando a ação acontece na tela.

## Opcional

- `apresentando.mp4`: você olhando para a câmera, 5 s, sem falar (entra sob a frase "Eu sou Henrique").

## Checklist antes de me avisar

- [ ] 6 vídeos da Parte A
- [ ] `V03_tela.mp4` + `V03_ventoinha.mp4` com a palma
- [ ] `cena1` a `cena8`
