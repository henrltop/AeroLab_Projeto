# Roteiro de edição — alvo 5min30s

Texto falado: `narracao.txt` (versão final). Gravações: `checklist_gravacao.md`.
Tempos estimados; serão ajustados à voz gravada.

| Tempo | Cena | Imagem na tela | Texto curto na tela |
|---|---|---|---|
| 0:00–0:22 | 1. Resultado primeiro | V01 + trecho do painel (V03_tela); `apresentando` opcional | "2 fios. Como medir e controlar?" |
| 0:22–1:00 | 2. Mede, decide, aciona | Fotos do sensor, V06; `01_visao_sistema` por blocos; `02_esquema_gpio21` destacado em 3 etapas: sensor/GPIO4 → gate/GPIO21 → 12 V e GND comum | TCRT5000 · ESP32 · IRLZ44N |
| 1:00–1:45 | 3. Marca → volta | V05a (pá marcada) → animação: marca passa, contador +1; 30 × 60 = 1800 | 9 pás · 1 marca · 1 pulso/volta |
| 1:45–2:25 | 4. Suporte + leitura | V05b, V05c; render do STL integral rotulado "projeto original"; `codigo_01`, `codigo_02` com zoom; animação do sinal cruzando 1300/2350 | Limites 1300 / 2350 |
| 2:25–2:55 | 5. Dois modos | Trecho do painel (V03_tela) + `05_legenda_grafico` | PWM ≠ RPM garantido |
| 2:55–3:55 | 6. Compensação | Animação de `04_compensacao` (selo "exemplo"); `codigo_04` destacando linhas 38, 43, 48 e 41 | Erro = desejado − medido |
| 3:55–5:05 | 7. Demonstração | V03_tela em tela cheia + V03_ventoinha em janela pequena; trechos acelerados recebem rótulo | — (sem cobrir o gráfico) |
| 5:05–5:30 | 8. Fechamento | V04 + cartão do GitHub com QR code | Endereço do repositório |

Regras: animações conceituais com selo "exemplo"; nenhuma série de dados inventada; cores laranja (setpoint), azul (medido), roxo pontilhado (PWM, eixo direito).
