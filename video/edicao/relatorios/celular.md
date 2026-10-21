# Relatório: vídeos do celular

Dados completos (planos, trechos, rótulos, sincronia, áudio): `celular.json`. Quadros-chave: `frames/`. As provas de sincronia estão nos arquivos `frames/SYNC_*.jpg`.

## O que é cada clipe
| Clipe | Horário | Conteúdo | Corresponde a |
|---|---|---|---|
| **084854** (88,9 s) | 08:48:54–08:50:23 | Montagem funcionando. A fonte e a protoboard aparecem em 0–10 s, a tela do painel em 26–34 s e 61–66 s, e a ventoinha **acelerando** em plano estável em 35–61 s. | **Tela B** |
| **085323** (130,3 s, proxies) | 08:53:23–08:55:33 | Clipe de **detalhes com a ventoinha PARADA**: suporte, pá marcada, ESP32, MOSFET, sensor e fonte. | Nenhuma tela (fica entre B e C) |
| **091353** (66,8 s) | 09:13:53–09:15:00 | Notebook com o painel e a ventoinha no canto inferior esquerdo. Mostra os cliques 2000 e 100. Em 57–60 s há um close da ventoinha devagar. | **Tela C** |
| **091629** (37,3 s) | 09:16:29–09:17:06 | Plano fixo do notebook com a ventoinha no canto. Mostra o clique em PWM 100% e a ventoinha disparando. | **Tela A** |

## Sincronia (celular_t = tela_t + offset)
O offset foi medido pela tela do notebook filmada no celular: comparei o quadro em que um KPI ou o setpoint muda no celular com o quadro exato da mesma mudança na gravação de tela.
- **084854 ↔ B: +0,68 s (±0,08), confiança alta.**
  - Medido 180→240: B 28,87 = celular 29,48.
  - Medido 240→180: B 29,83 = celular 30,48.
  - Medido 2.280→2.460: B 62,80 = celular 63,53.
  - Há uma leve deriva. Use +0,65 no trecho 0–45 s e +0,72 no trecho 55–88 s.
  - Equivalências: clique 2000 = celular **42,35**, subida do PWM = **43,6**, clique 2500 = **58,9**.
  - O áudio confirma: o harmônico de 1 kHz do PWM fica mais forte a partir de ~43,7 s.
- **091353 ↔ C: +0,31 s (±0,05), confiança alta.**
  - Setpoint 1.600→2.000: C 22,13 = celular 22,48.
  - Setpoint 2.000→100: C 46,90 = celular 47,18.
  - O ALT+TAB de C fica fora do clipe do celular.
- **091629 ↔ A: +0,68 s (±0,03), confiança alta.**
  - PWM 10→100: A 14,90 = celular 15,58.
  - Medido 120→60: A 14,80 = celular 15,48.
  - O clique em 100% (A 14,75) cai no celular em 15,43 s.
- **085323 não sincroniza com A nem com C**, porque não houve gravação de tela naquele horário.
- ⚠ O cronômetro "00:00:SS" do gravador de tela aparece no celular, mas está **~1 s adiantado** em relação ao arquivo. Não use esse número para sincronizar.

## Melhores trechos (in–out em s do clipe)
- **V01 abertura:**
  - 091629 13,5–21,5: painel e ventoinha juntos, PWM 10→100%. É um plano fixo e a tela fica legível.
  - Alternativa: 084854 40,5–47,5, a ventoinha acelerando de 200 para 2000 RPM, em sincronia com B.
  - Alternativa: 084854 13,0–18,5, movimento da protoboard até a ventoinha girando.
- **V04 encerramento:**
  - 084854 67,0–73,5: ventoinha a ~2500 RPM, plano estável.
  - 084854 80,5–87,5: plano geral da montagem.
- **V05a pá marcada:**
  - **085323 39,5–43,0**: vista frontal, o dedo gira a pá e a fita branca aparece. Plano nítido. O rótulo vai em (0,50; 0,34).
  - 085323 55,5–59,0: close extremo da fita junto ao braço do sensor. O foco é suave.
  - 085323 1,0–5,5: vista 3/4 com a ventoinha parada.
- **V05b sensor no suporte:** 085323 92,0–97,5. O TCRT5000 fica sob o braço amarelo, em ~(0,49; 0,52). Há mãos no quadro e o foco é irregular.
- **V05c suporte inteiro:** **085323 20,0–26,5**. Plano estável e nítido, rótulo em ~(0,43; 0,60).
- **V06 conexões:**
  - **085323 69,5–74,5**: close do ESP32, onde "ESP32" está legível no módulo. Rótulo em (0,56; 0,45). O cabo USB fica em (0,15; 0,47).
  - **085323 82,2–84,0**: protoboard inteira. Plano curto, vale congelar o quadro. Rótulos:
    - ESP32 (0,24; 0,42)
    - MOSFET TO-220 com dissipador (0,54; 0,44)
    - resistores (0,67; 0,52)
    - conector da ventoinha (0,91; 0,84)
  - 085323 76–81,5: close do MOSFET e dos resistores. Tem movimento.
  - 085323 113,8–117: fonte com LED verde.
  - 084854 0,5–7,0: fonte e protoboard em plano aberto.

Identificação dos componentes:
- **ESP32:** segura.
- **IRLZ44N:** a marcação **não é legível**. Rotule "MOSFET" ou use o nome pelo que se sabe do projeto.
- **Resistores:** os valores não são legíveis.
- **TCRT5000:** a marcação não é legível.
- **Fonte:** a tensão não é legível.

## Áudio
- **Todos os clipes têm fala do usuário** (voz próxima, pico ~-13 a -18 dBFS). Não transcrevi as falas porque não há modelo ASR offline.
- Sempre que a ventoinha está ligada aparece um **assobio do PWM em 1 kHz** e harmônicos. O ruído aerodinâmico da ventoinha é fraco: a 4.400 RPM aparece um tom de ~660 Hz.
- Trechos sem voz:
  - 084854: **62,3–68,0** (2500 RPM), 42,5–45,6 e 47,0–50,4.
  - 091353: **21,3–35,2** (14 s, com teclas).
  - 091629: 31,8–37,2 (100%).
  - 085323: 89,6–100,6 (ventoinha parada).
- Recomendação: use o ambiente só como cama a -30/-35 dB, com passa-baixas ~800 Hz ou notch em 1/2/3 kHz.

## Privacidade e qualidade
- Os planos da tela do notebook mostram o caminho "C:/Users/Cyber/...", o avatar e a barra de tarefas. Corte ou desfoque o topo e a base da tela, ou use a gravação de tela.
- Mãos aparecem em vários planos de 085323. Não há nenhum rosto.
- A tela filmada fica lavada e superexposta, mas os números grandes são legíveis.

## O que FALTA
- Close **nítido com marcação legível** do IRLZ44N, dos resistores (220 Ω e 10 kΩ), do TCRT5000 e da tensão da fonte.
- Close da pá marcada **sem dedos e com foco firme**: o nítido tem só ~3,5 s, e o close extremo é suave.
- Sensor no suporte **sem mãos**.
- Em B não há um plano que mostre a tela e a ventoinha inteiras juntas. Essa combinação só existe em 091353 (C) e 091629 (A).
