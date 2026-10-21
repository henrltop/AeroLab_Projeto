# Relatório: gravações de tela (painel AeroLab)

Dados completos (eventos, bboxes, crops, trechos com in/out): `telas.json`. Frames-chave: `frames/`.

Apelidos usados: **A** = "cideo ... PWM colocando em 100%" (36 s), **B** = "gravação tela controlando temperatura ..." (88 s), **C** = "video ... 1600 RPM ... 2000 ... 100 RMP" (72 s).

## Achados principais
- **Os dados são reais, não simulados.** Todas as gravações mostram a pílula "Recebendo dados", o texto "ESP32 via USB · atualização de aproximadamente 1 s" e "115200 baud". O botão "Ver demonstração" aparece desabilitado e não há aviso de simulação. O texto literal `esp32_usb` não aparece na tela.
- **C vai mesmo para 100 RPM, não para 1000.** O alvo passa de 2.000 para 100. O RPM medido cai para 120/60 e o PWM para em 10%. Isso acontece porque 60–120 está dentro da zona morta de ±60 em torno de 100, então o controlador deixa de ajustar. Além disso, 60 RPM é a resolução da medida (1 pulso/s). Vale uma frase na narração.
- **B trata de velocidade (modo RPM), não de temperatura.** O alvo vai de 200 para 2000 e depois para 2500.
- **O áudio dos três vídeos é silêncio digital.** Não há palma nem som. A sincronização com o celular tem que usar os eventos visuais:
  - B, clique "Aplicar 2000" em **41,7 s**: o card do setpoint muda em 41,9 s e o PWM começa a subir em 42,9 s. A ventoinha deve acelerar a partir de ~43 s.
  - B, clique "Aplicar 2500" em **58,2 s**: o PWM sobe a partir de 58,9 s.
  - Relógio de B: t=0 ≈ 08:48:55 (±2 s) em 21/10/2026.
- **Ordem real das gravações:** B (08:48), depois C (09:12–09:15), depois A (09:15–09:17). A começa com o alvo de 100 RPM que sobrou de C.
- **Rampa do firmware visível nos dados:** o PWM muda cerca de 5 p.p./s (B 43–48 s: 17→22→27→32→37%; C 47–56 s: 39→34→29→24→19%). Isso confere com o limite de ±5 p.p./s.

## Linha do tempo resumida
| Arq | t (s) | Evento |
|---|---|---|
| A | 0–13,6 | Parado. Modo Percentual (MANUAL), valor 100 já digitado. PWM 10%, medido 60/120. |
| A | 14,75 | **Clique "Aplicar percentual" 100%.** PWM 100% em 14,9 s; o setpoint vira "—". |
| A | 15,8 / 16,8 / 17,8 / 18,8 | RPM 1.860 / 4.080 / 4.500 / 4.560 (pico). Depois fica entre 4.200 e 4.440. |
| B | 0–39,5 | Parado: alvo 200, medido 180/240, PWM 11–12%. |
| B | 41,7 | **Aplicar 2000.** RPM 540 (44,8 s), 1.080 (47 s), 1.680 (49 s), 2.040 (52 s). PWM estabiliza em 41–42%. |
| B | 58,2 | **Aplicar 2500.** RPM 2.220 (61 s), 2.460 (63 s). Regime de 2.400–2.520, PWM 48→50%. |
| C | 0–16 | Alvo 1.600, medido 1.560/1.620, PWM 38%. |
| C | 22,0 | **Aplicar 2000.** Chega a 1.980 em ~28 s. PWM 44–45%. |
| C | 46,75 | **Aplicar 100.** PWM 44→10%. RPM chega a 240 em 55 s e a 120 em 57 s. |
| C | 69,0–69,7 | **ALT+TAB: cortar.** |

## Sobreposições e trechos a evitar
- **Barra do Chrome (y<87) em todos os vídeos.** Mostra o caminho `C:/Users/Cyber/...` (nome de usuário), o avatar do perfil e "Peça ao Gemini". Os crops propostos já a excluem.
- **Barra de tarefas do Windows em B (y>1152).** Mostra relógio/data e os ícones do Spotify e do ChatGPT.
- **ALT+TAB em C, 69,0–69,7 s.** Expõe as janelas Claude, ChatGPT, "Aura · computador de sala", Spotify e Explorador de Arquivos. Não usar.
- **Tooltips do gráfico em A:** 20,8–22,5, 25,8–30,5 e 33,8–34,6 s.
- **Toasts de confirmação no canto inferior direito:** A 15–20,5 s; B ~42–47 e ~58–61 s; C 22–27 e 47–53 s. São informativos e podem ficar.
- **Trechos parados:** A 0–13,6 s, B 0–39,5 s e C 28–43 s.
- **Eixo Y do gráfico reescala sozinho** (em A: 2.500→5.000→5.500).

## Geometria (pixels do original; em C, subtrair 6 de y)
- KPIs: 268,366–1854,505
- Card do gráfico: 268,528–1513,1062
- Legenda: 288,618–628,642
- Área do gráfico: 290,655–1500,985
- Card de controle: 1535,528–1855,1062
- Seletor de modo: 1562,622–1828,660
- Valor: 1562,688–1828,780
- Botão Aplicar: 1561,875–1827,915
- Toast: 1697,1080–1878,1127

**Crops 16:9 para escalar a 1920×1080.** Nenhum corta a legenda. Para conferir, veja `frames/GEOMETRIA_bboxes_e_crops_sobre_A_25s.png`.
- `painel` x226 y176 1664×936 (×1,154): visão geral sem navegador.
- `dados` x272 y262 1578×888 (×1,217): pílula "Recebendo dados" + KPIs + gráfico + controle. **Recomendado para a cena 7.**
- `grafico` x269 y450 1244×700 (×1,543): o topo pega a base dos KPIs. Cobrir y 450–515 com uma faixa #F4F6FA ou aceitar como está.
- `controle` x1080 y540 816×459 (×2,35): para a cena 5. Fica um pouco suave; a alternativa é usar o card de controle como PiP.
- `tela_sem_navegador` x15 y87 1888×1062 (×1,017): quase a tela inteira, com a sidebar.

## Trechos sugeridos
- **Abertura:** A 14,4–20,7 (crop `grafico`, 1x): o PWM salta e o azul dispara. Alternativa: C 46,5–54,0 (descida 2000→100).
- **Cena 5:**
  - A 4,0–9,0 (crop `controle`): modo Percentual, 100%, slider/presets.
  - C 16,0–22,6: modo RPM alvo, valor muda para 2000 e há o clique em Aplicar.
  - Nenhuma gravação mostra a troca de aba do seletor, então use seta/realce no seletor.
- **Cena 7** (crop `dados`, tudo a 1x salvo o indicado):
  1. A 13,5–20,7 (7,2 s): modo percentual 100%.
  2. B 40,0–54,0 (14 s): RPM 200→2000. É o vídeo sincronizado com o celular.
  3. B 56,5–66,0 (9,5 s): 2000→2500.
  4. C 45,5–58,0 (12,5 s): 2000→100.
  5. *Opcional:* C 58,0–68,0 **acelerado 2x** (5 s, rotular "x2"): 100 RPM com PWM 10%. Parar antes de 68,9.

  Isso dá 48–53 s. Para chegar a 60–70 s, acrescente B 66–80 a 2x (7 s) ou C 19,5–29 a 1x (1600→2000). Os tempos de resposta ficam preservados porque todo o resto roda a 1x.
