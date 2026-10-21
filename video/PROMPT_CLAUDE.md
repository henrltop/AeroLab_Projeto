# Pedido de edição — vídeo AeroLab

Quero criar um vídeo acadêmico dinâmico de até seis minutos sobre meu projeto de controle e medição da velocidade de uma ventoinha. Mire em 5min30s, deixando margem para pausas e transições.

Sou Henrique. O projeto já funcionou na minha montagem. Quero gravar a narração e algumas imagens reais e combinar isso com os materiais desta pasta. Não quero aparecer falando durante o vídeo inteiro.

## Sua primeira resposta

Leia `../CLAUDE.md` (na raiz do projeto) e confira os arquivos. Entregue um inventário, uma proposta de montagem e uma lista curta dos materiais ausentes. Converse comigo sobre como gravar o que falta e como melhorar o ritmo. Já existe uma estrutura em `storyboard.csv`, mas ajuste os tempos à gravação real da voz.

## História

Comece pelo resultado funcionando: ventoinha e gráfico. Apresente o desafio de medir rotação com apenas dois fios. Mostre sensor, ESP32, MOSFET e esquema. Explique a única marca por volta, os dois limiares, o cálculo de RPM e a correção automática. Mostre o suporte 3D como etapa de fabricação e termine com uma demonstração real dos modos percentual e RPM. GitHub só no fim, se eu fornecer a URL.

## Recursos visuais

- `../assets/visuais/01_visao_sistema`: leitura, decisão e acionamento; grupos editáveis no SVG.
- `02_esquema_gpio21`: referência elétrica com sensor avulso, GPIO4 e PWM21. Destacar por etapas, não mostrar tudo com texto minúsculo.
- `03_um_pulso_por_volta`: exemplo conceitual de uma marca e um evento; nove pás ilustradas.
- `04_compensacao`: exemplo didático 2000−1600=400 RPM e correção +2 p.p./s. Não são medições.
- `05_legenda_grafico`: manter as cores e eixos corretos.
- `codigo_01` a `codigo_06`: cartões com trechos reais, extraídos do firmware e indexados em `trechos_codigo/indice.json`.
- `../mecanica/v1_original/Previa_Suporte_V1.png`: CAD da V1, que é histórica e foi concebida para fundo branco; não representa automaticamente a posição óptica final. Existem STL e SCAD se for possível renderizar novas vistas verdadeiras.
- `../assets/fotos_sensor/`: fotos reais do sensor avulso.
- `../assets/esquemas_historicos/`: imagens antigas para uma eventual evolução do projeto; têm diferenças documentadas em `../docs/hardware.md`.

Os SVGs podem ser editados/anima­dos por grupos. Se só usar PNG, faça panorâmicas e aproximações suaves. Uma animação 3D deve vir do STL/SCAD real, não de perspectiva inventada de uma imagem. Não gere fotografias falsas da montagem.

## Narração e demonstração

Use `narracao.txt` como texto limpo para eu gravar. `roteiro.md` contém sugestões de cena. Não é preciso eu aparecer o tempo todo; podemos usar minha imagem apenas na abertura/encerramento e narração nos demais momentos.

Na demonstração, use gravação real do painel e da ventoinha. Preserve o tempo relevante de resposta. Se acelerar, rotule. Se eu ainda não enviar essa gravação, monte a sequência com uma pendência claramente identificada; não preencha com telemetria falsa. Não esconda o aviso de simulação do modo demo.

## Edição

1920×1080, horizontal, 30 fps como padrão do projeto; adapte cortes às fontes sem acelerar a fala. Até 360 s incluindo créditos. A timeline inicial tem 330 s; revise depois de medir a narração, sem usar os tempos estimados como legenda sincronizada.

Use legendas em português, duas linhas no máximo e margens confortáveis. Textos curtos, alto contraste e zoom legível no código. Evite sobrepor legenda à informação do gráfico. Mantenha laranja para alvo, azul para medido e roxo pontilhado para PWM.

Prefiro música discreta ou nenhuma a uma trilha que dispute com a voz. Reduza ruído sem voz artificial; não clone minha voz sem eu pedir. Evite vinhetas longas, excesso de transições, imagens genéricas de tecnologia e gráficos fictícios.

## Implementação e entrega

Inspecione ambiente e ferramentas antes de escolher FFmpeg, Remotion ou outro fluxo. Guarde fontes de edição em `edicao/`, bruto em `entrada/` e renders em `saida/`. Não instale ferramentas ou use serviços externos por suposição se houver impacto relevante no ambiente ou privacidade.

Faça uma primeira prévia, me mostre pendências e depois ajuste a edição. Verifique duração final, áudio, legendas, legibilidade, nomes dos componentes, cores, um pulso por volta e pinos. Só gere QR code quando `config.json` tiver o endereço real do GitHub e confira o destino.

O repositório ainda não foi publicado. Há instruções em `../docs/github.md`. Não invente URL nem afirme publicação. Preserve o código funcional existente.
