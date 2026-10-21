# Relatório — agente de ÁUDIO

## Entregas (em /home/claude/edit/audio/)
- `narracao_editada.wav`: 48 kHz, mono, PCM 24-bit, **4:26,05 (266,05 s)**
- `edl.json`: 45 trechos em ordem, com cena, frase do roteiro, início/fim no arquivo original, texto falado e o tempo no áudio editado
- `timeline.json`: início e fim da fala de cada cena e de cada frase no áudio editado, mais a duração total
- `legendas.srt`: 83 blocos, pt-BR, no máximo 2 linhas de até 38 caracteres, cada bloco entre 1,0 e 6,0 s
- `work/`: scripts (`seeds.py` traz a escolha das tomadas; `build.py`, `master.sh` e `outputs.py` refazem tudo), transcrições e o modelo

## Duração e tempos (áudio editado)
Total de 4:26,05, abaixo da meta de 5:05, com ~39 s de folga. Nenhuma pausa precisou ser apertada.

| Cena | início (s) | fim (s) |
|---|---|---|
| 1 | 0,07 | 21,67 |
| 2 | 22,67 | 61,95 |
| 3 | 62,95 | 94,80 |
| 4 | 95,80 | 134,01 |
| 5 | 135,01 | 157,27 |
| 6 | 158,27 | 208,77 |
| 7 | 209,77 | 243,12 |
| 8 | 244,12 | 265,94 |

Os tempos marcam o início e o fim da fala. Entre cenas há ~1,0 s de silêncio gerado, entre parágrafos ~0,7 s e entre frases ~0,35 s, sempre medidos de fala a fala.

## Transcrição
- Para baixar modelos, huggingface.co, openaipublic e modelscope foram **bloqueados pelo proxy (403)**.
- Usei faster-whisper com o **Whisper small (CTranslate2 int8)**. O modelo veio do registro **npm** (pacotes `@skillninja/shortmovie-telop-model-p0…p3`, licença MIT). O SHA-256 confere com o publicado no pacote (`ca732cb1…ce73`). Esse pacote é de terceiros: não é o repositório oficial da Systran.
- O áudio foi processado só localmente. Rodei com language=pt, word_timestamps, vad_filter e beam 5. Trechos ambíguos foram transcritos de novo isoladamente.
- O modelo medium não estava disponível.

## Verificação
- As bordas de corte são sempre em silêncio. Uso um detector de energia em banda larga e em 2,5–10 kHz (para pegar fricativas), com folga de 60 ms e micro-fades de 10 ms.
- O áudio final foi **transcrito de novo**. As 45 frases batem com o texto esperado, sem palavra cortada nem trecho duplicado. Os 12 trechos de borda duvidosa foram transcritos um a um: a primeira e a última palavra estão inteiras.
- Cliques: o pico de derivada a ±5 ms de cada emenda fica no máximo em 1,2× o p99 local (nas emendas é inaudível). Os únicos picos altos do arquivo são sibilantes que já existem na gravação original.
- Loudness: −16,0 LUFS integrado, true peak −1,5 dBTP, LRA 2,0 LU.

## Processamento
1. Highpass de 80 Hz.
2. Redução de ruído estacionária (spectral gating `noisereduce`, prop_decrease 0,75, perfil de ruído tirado de 30 s de pausas), cerca de −11 dB no ruído. O afftdn do ffmpeg quase não fez efeito neste ruído.
3. Cortes e montagem com as pausas geradas.
4. Expansor suave (agate com faixa limitada) e compressor leve 2,5:1.
5. loudnorm em 2 passadas, linear.

## Frases do roteiro AUSENTES ou diferentes (importante)
- **Cena 1:** ele não diz "**e uma interface**". A fala é "um ESP32, um sensor óptico, pra poder medir e controlar a velocidade dessa ventoinha". Ele também diz "Esse **é** o desafio" (o roteiro tem "foi").
- **Cena 2:** falta "**de doze volts**" na frase do MOSFET. Os 12 V aparecem na frase seguinte.
- **Cena 3:** em vez de "calcula o RPM: rotações por minuto" ele diz "calcula a quantidade de rotações por minuto". O exemplo termina em "1800 rotações por minuto, mais ou menos" (não diz "RPM").
- **Cena 5:** "Cinquenta por cento de PWM não quer dizer metade da velocidade **máxima**". Ele diz só "metade da velocidade" e completa com "Isso depende muito de ventoinha para ventoinha".
- **Cena 6:** na frase do ganho ele diz "a força **de** correção". Na justificativa dos 60 RPM, as duas transcrições ouviram "um pulso a mais **de** um segundo" (o roteiro tem "em um segundo"). A legenda segue o que foi falado. Vale ouvir em ~200–203 s do editado.
- **Cena 8:** "O código, (o) painel e o modelo 3D vão estar no repositório do GitHub, que o link está bem aqui na descrição".
- **Cena 7, linha laranja:** ele diz "o azul é o RPM medido" (no roteiro, "A azul").
- **Cena 6, ordem das tomadas:** a última tomada completa (~352–369 s do original) diz "o erro é calculado com o erro desejado menos o **erro** medido", o que é tecnicamente impreciso. Usei a 3ª tomada ("o erro é desejado menos medido: mais 400 RPM", ~337–347 s) e completei com "como está abaixo do alvo… essa conta acontece bem aqui" da última tomada (~364–369 s). A emenda soa natural, mas vale ouvir em ~158–174 s do editado.
- **Cena 3, "O ESP32 conta essas passagens":** a 2ª tomada (usada) tem um "o… ESP32" com pequena hesitação no começo. Ficou dentro do corte e aparece como "O ESP32".

Nenhuma frase do roteiro ficou sem tomada utilizável.

## Improvisos MANTIDOS (no assunto, sem passar da meta)
- **C1:** "estudante de Engenharia de Controle e Automação do Instituto Federal". O nome do curso foi inferido do áudio ("engenharia e control automação"). **Confirme o nome do curso.**
- **C2:** "Assim a gente consegue fazer a contagem de quantas voltas a ventoinha deu."
- **C2:** "Quem decide, faz os cálculos, é o ESP32." (O ASR ouviu "decide fazer os cálculos".)
- **C2:** "…muito rapidamente, fazendo assim a gente consegue controlar a nossa ventoinha." Não dava para cortar limpo depois de "rapidamente": não há pausa.
- **C3:** "É essa conta que o ESP faz pra dizer pra gente qual a velocidade efetiva do nosso ventiladorzinho."
- **C4:** "…sem encostar no que gira, ele não pode encostar."
- **C5:** "No modo percentual, eu escolho direto o PWM. PWM, que é a fração…" (ele repete "PWM").
- **C7:** "…é o PWM, isso aqui no eixo da direita."
- **C7:** "O controle roda **100%** no ESP32."
- **C8:** encerramento "Bom, muito obrigado e aguardo vocês no próximo vídeo." Pode ser removido: é o último trecho do EDL (~263,4–266,0 s).

## Descartado
- Falsos começos e repetições: "quem aciona é o MOSFET IRLZ…", as várias tomadas de "No início o modelo…", "Na interface…", "Um exemplo…", "Depois o erro…", "Dentro de 60 RPM…", "A linha laranja…" e "A interface só envia…".
- "Com ganho de 0,05… Não."
- Comentários fora do roteiro: "Nesse caso, a gente não… Não, eu não gostei dessa parte", "ignore isso que eu estou falando", e o trecho sobre o sensor ficar tampado e a "parte aqui atrás" do suporte.
- Improvisos redundantes: "Bom, e o outro modo é o modo RPM" e "Eu escolho só a velocidade qualquer e ele com os cálculos dele consegue chegar…".
- Pigarros (~25 s e ~446 s do original).
- Pausas internas maiores que 0,75 s viraram ~0,45 s (frases 9, 20, 21 e 26 do EDL).

## Problemas de áudio
- **Ruído de fundo**: chiado/ronco de sala de banda larga entre 100 e 1000 Hz (ar-condicionado ou ventilador?), em ~−36 dBFS no original. A relação sinal-ruído era de ~20–25 dB. Depois do tratamento, o ruído nas micro-pausas dentro das frases fica em ~−38 dBFS, contra fala em ~−12 dBFS. Entre frases o silêncio é digital, por isso **com fone dá para notar o ruído "entrar e sair" a cada frase**. Se incomodar, há duas saídas: gerar um ruído de conforto sintético bem baixo nas pausas, ou tocar trilha de fundo baixa (que mascara). Não apliquei redução mais forte para não deixar a voz metálica.
- Sem clipping: o pico do original é 0,984 e nenhuma amostra chega a ±0,99. Volume do original adequado, mas a fala no começo de algumas frases é um pouco mais forte. A compressão leve resolveu (LRA 2 LU).

## Dúvidas para o Henrique
1. Qual o nome exato do curso ("Engenharia de Controle e Automação"?) e do Instituto Federal (só "Instituto Federal")?
2. Manter o encerramento "Bom, muito obrigado…"?
3. Ele diz "o próprio **ESP**" e "o **ESP** faz" (sem 32). A legenda segue a fala.
4. Ele diz "1800 rotações por minuto", não "RPM", e a legenda segue a fala. O texto na tela pode mostrar "1800 RPM".

## Ajuste: room tone nas pausas (pedido do editor)
- `narracao_editada_rt.wav`: os tempos são os mesmos do `timeline.json` e a duração é idêntica (266,05 s). As pausas geradas agora têm room tone real no lugar do silêncio digital. As emendas usam crossfade equal-power de 30 ms. Ficou em −16,1 LUFS e −1,7 dBTP.
- Origem do room tone: 13 trechos de 0,9–1,2 s sem fala, respiração ou clique, tirados do original (391,5, 230,9, 210,9, 244,4, 267,9, 121,8, 78,7, 226,3, 233,3, 535,6, 552,8, 382,7 e 386,5 s). Passaram pela mesma redução de ruído e pelo mesmo highpass, foram igualados em nível (±2 dB) e emendados com crossfade de 30 ms. O original não tem nenhum trecho limpo maior que ~1,5 s.
- Masterização: compressor e ganho linear fixo de +3,65 dB, com limitador a −2,8 dB, igual para todos os arquivos. **Tirei o expansor (agate)**: ele mesmo causava o ruído entrando e saindo. Não usei o loudnorm, porque ele caiu em modo dinâmico e daria ganhos diferentes ao room tone avulso.
- `roomtone_30s.wav`: tem **−38,0 dBFS RMS**, o mesmo nível medido nas pausas do arquivo final (−38,0 dBFS). O loop foi feito com crossfade do fim no início e processado em 3 cópias, das quais saiu a do meio, por isso a emenda do loop é inaudível.
- `frases/c7_01…c7_07` e `c8_01…c8_05`: mesmo ganho do arquivo final, cortadas nos limites do EDL (editado_inicio/editado_fim), com ~60–90 ms de folga de fundo em cada ponta e fades de 5 ms.
- Diferença que sobra: o fundo nas bordas das frases fica ~2 dB acima do das pausas (−36 contra −38 dBFS). Parte disso deve ser resto de respiração e decaimento da voz. Não deve ser perceptível.
