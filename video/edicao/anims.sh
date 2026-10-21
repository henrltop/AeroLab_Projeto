cd /home/claude/edit/anim
r(){ python3 render.py "$1" "$2" final/$1.mp4 "$3" > final/$1.log 2>&1 && echo "OK $1" >> final/status.txt || echo "FALHOU $1" >> final/status.txt; }
r sistema 4.98 '{"medir":0.2,"decidir":1.3,"acionar":2.4,"realimentacao":3.5}'
r esquema 13.77 '{"sensor":0.35,"pwm":3.7,"potencia":7.58,"terra":10.8}'
r marca 20.86 '{"marca":0.2,"passagem":1.5,"rpm":6.1,"exemplo":13.31}'
r codigo_leitura 8.17 '{"leitura":0.35,"bloco":5.23,"limites":6.4}'
r limiares 15.38 '{"limites":0.1,"entrada":1.2,"saida":5.0,"ruido":9.5}'
r compensacao 51.5 '{"erro":0.5,"sobe":10.64,"ganho":20.61,"acumula":28.74,"negativo":31.8,"margem":35.91}'
r codigo_controle 51.5 '{"erro":13.53,"ajuste":16.44,"acumula":28.74,"margem":35.91,"limite":45.81}'
echo FIM >> final/status.txt
