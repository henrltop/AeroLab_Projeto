# Recursos visuais

- `visuais/`: 11 artes produzidas para este pacote, cada uma em SVG editável e PNG 1920×1080. Cinco explicam o sistema, esquema, contagem, compensação e cores; seis mostram trechos reais do código.
- `fotos_sensor/`: três fotografias originais fornecidas por Henrique, copiadas sem modificações.
- `esquemas_historicos/`: cinco imagens recuperadas das etapas anteriores; veja as diferenças em `../docs/hardware.md` antes de usar.

A prévia e os arquivos da mecânica estão em `../mecanica/v1_original/`.

As artes conceituais não são dados de bancada, capturas do painel, fotografias de hardware nem CAD do rotor. O novo esquema elétrico usa GPIO21 e transpõe a referência anterior; não foi confrontado com fotografia atual das conexões.

Para regenerar, rode `python3 tools/atualizar_trechos.py` e `python3 tools/gerar_visuais.py` a partir da raiz. O segundo script gera SVG com Python padrão; para gerar os PNGs requer Inkscape no PATH. Os PNGs prontos já estão incluídos, não é necessário instalar nada para usá-los no vídeo.

Os grupos SVG têm IDs que facilitam destacar partes. Os cartões de código preservam a indentação e têm indicação das linhas do firmware de origem.
