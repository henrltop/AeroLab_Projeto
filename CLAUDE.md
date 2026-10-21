# AeroLab — instruções ao agente

Henrique está preparando um vídeo acadêmico de até 6 minutos e o repositório deste projeto. O hardware já funcionou, segundo seu relato. A tarefa atual é editar/apresentar e organizar, sem alterar o funcionamento.

## Leia primeiro

1. `README.md`
2. `video/PROMPT_CLAUDE.md`
3. `video/materiais.json`, `video/config.json` e `video/storyboard.csv`
4. `video/roteiro.md` e `video/narracao.txt`
5. `docs/hardware.md`, `docs/codigo.md`, `docs/interface.md`

## Verdades que não devem mudar na edição

- Ventoinha 12 V, dois fios; sensor avulso GPIO4; IRLZ44N comandado por GPIO21.
- Nove pás, mas só uma marca: **1 pulso/volta** no firmware principal.
- Desejado laranja, medido azul, PWM roxo pontilhado/eixo direito.
- Controle automático no ESP32; interface local por USB serial.
- Correção acumulativa, ganho 0.005, margem ±60 e máximo 5 pontos percentuais/s. Não dizer PID completo, precisão garantida ou erro zero.
- Não confundir `historico/` com firmware principal. Os arquivos desse diretório descrevem outra estratégia.
- Esquemas históricos usam GPIO25 e um deles usa módulo digital. Preferir o esquema novo GPIO21, que é referência documentada, não um levantamento físico.
- CAD V1 foi criado para leitura de espaços com fundo branco; não alegar que mostra exatamente a configuração óptica final. O usuário passou depois para uma marca. A aparência final deve vir da montagem real.
- A corrente da fonte, versão exata da placa/core e URL do GitHub não foram informadas.

## Trabalho esperado

Faça inventário e proponha uma timeline antes de renderizar. Use as artes PNG 1920×1080 e fontes SVG editáveis em `assets/visuais/`. Confira as pendências, solicite somente os materiais ausentes e avance no que já for possível.

Detecte as ferramentas disponíveis no computador e escolha um fluxo de edição reproduzível. Não presuma que Remotion, FFmpeg, Blender ou OpenSCAD estejam instalados. Não faça upload de fotos, voz ou vídeo para serviços externos sem orientação do usuário.

Não mude firmware, protocolo ou painel para produzir resultados mais bonitos. Não apresente dados simulados, gráficos desenhados, CAD ou exemplos numéricos como testes físicos. A demonstração do painel é explicitamente simulada.

Saída pretendida: MP4 1920×1080, até 360 s, narração clara, legendas revisadas e projeto de edição reproduzível em `video/edicao/`. Saídas em `video/saida/`, ignoradas no Git. `github_url` fica vazio até Henrique fornecer o endereço real; não gerar QR code de exemplo.

Documente o que foi realmente conferido. Testes do painel: `node --test web/tests/*.test.cjs`. Build: `node web/build.cjs`. Firmware e CAD preservados; não afirme recompilação física ou nova validação de bancada.
