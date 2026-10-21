#!/usr/bin/env bash
# Renderiza todas as animações com as durações padrão. Uso: ./todas.sh [nome...]
set -euo pipefail
cd "$(dirname "$0")"
python3 gen_fw.py >/dev/null
O=out
declare -A D=([sistema]=12 [esquema]=14 [marca]=14 [limiares]=14 [codigo_leitura]=8 [compensacao]=22 [codigo_controle]=16 [legenda]=6)
NOMES=("$@"); [ ${#NOMES[@]} -eq 0 ] && NOMES=(sistema esquema marca limiares codigo_leitura compensacao codigo_controle legenda titulo rotulos)
for n in "${NOMES[@]}"; do
  case $n in
    titulo)
      python3 render.py titulo 5 $O/titulo_alpha.mov --alpha
      python3 render.py titulo 5 $O/_tit --stills 2.5 --alpha >/dev/null
      mv $O/_tit/titulo_002.50.png $O/titulo_alpha.png && rmdir $O/_tit ;;
    rotulos) python3 rotulos.py $O/rotulos >/dev/null ;;
    legenda)
      python3 render.py legenda 6 $O/legenda.mp4
      python3 render.py legenda 6 $O/legenda_alpha.mov --alpha ;;
    *) python3 render.py $n ${D[$n]} $O/$n.mp4 ;;
  esac
done
