# Validação do pacote — 21/10/2026

## Conferido nesta organização

- Os 14 testes existentes do painel passaram em Node.js: parser, comandos, CSV, transporte serial simulado, fechamento e estrutura HTML.
- O build recompôs o HTML e o SHA-256 permaneceu idêntico ao painel recuperado, versão com as cores distintas.
- O firmware principal é byte a byte idêntico tanto ao arquivo avulso recuperado quanto ao firmware do pacote anterior. Nenhuma lógica foi alterada para o vídeo.
- Seis trechos de código foram extraídos e comparados às linhas reais do firmware.
- Os 11 visuais SVG foram renderizados como PNG de 1920×1080. A conferência inclui dimensões, limites dos textos e inspeção visual dos diagramas e de um cartão de código.
- O storyboard começa em zero, tem cenas consecutivas e termina em 330 segundos. Isso é planejamento; a edição final depende da voz e das gravações reais.
- Os arquivos originais da mecânica foram preservados. O relatório `mecanica/v1_original/verificacao_malhas.json` é o relatório anterior; não é um novo ensaio físico.
- O manifesto SHA-256 acompanha os arquivos distribuídos, e a estrutura do ZIP foi verificada.

## Limites do que foi verificado

Henrique relatou que o sistema funcionou corretamente. Não houve neste ambiente nova conexão física ao ESP32, medição de corrente, ensaio de precisão ou caracterização da resposta da ventoinha.

Não foi recompilado o firmware com o toolchain Arduino nesta organização. A versão exata do core Arduino-ESP32 utilizada por Henrique não foi informada; preserve a configuração com que ele já compilou.

Não houve nova sessão de navegador conectada à placa. Os testes de transporte serial utilizam porta simulada; não equivalem a um ensaio USB real. Não foram produzidas capturas fictícias do painel.

O CAD é a V1 recuperada, com a estratégia óptica original por espaços. O controle atual usa uma marca por volta. Essa diferença está documentada e precisa ser respeitada na apresentação.

Não há vídeo, narração gravada, CSV experimental ou URL de repositório no material disponível. O pacote prepara a edição e o upload ao GitHub; não afirma tê-los concluído.
