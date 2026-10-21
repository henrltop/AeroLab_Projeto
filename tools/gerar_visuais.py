"""Gera SVGs editáveis e, com Inkscape disponível, PNGs 1920×1080.
Python 3; nenhuma imagem ou telemetria sintética é tratada como foto/medição.
"""
from pathlib import Path
import html, json, math, shutil, subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/visuais';OUT.mkdir(parents=True,exist_ok=True)
INK='#172b43';MUTED='#5b6d80';BG='#f5f7fb';BLUE='#2478c8';ORANGE='#c66a16';PURPLE='#8656b9';TEAL='#118b80';RED='#d54343'
def t(x,y,s,size=28,color=INK,weight=400,anchor=None,mono=False):
    return f'<text xml:space="preserve" x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+(' font-family="DejaVu Sans Mono, monospace"' if mono else '')+'>'+html.escape(s)+'</text>'
def rect(x,y,w,h,fill='white',stroke='#d8e0eb',radius=22):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def line(points,color=INK,width=6,dash=None):
    return '<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def circle(x,y,r,fill,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
def arrow(x1,y1,x2,y2,color=INK,width=6,dash=None):
    a=math.atan2(y2-y1,x2-x1);length=18
    return line([(x1,y1),(x2,y2)],color,width,dash)+line([(x2-length*math.cos(a-.45),y2-length*math.sin(a-.45)),(x2,y2),(x2-length*math.cos(a+.45),y2-length*math.sin(a+.45))],color,width)
def group(name,s):return f'<g id="{name}">{s}</g>'
def shell(title,sub,body,foot):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><title>'+html.escape(title)+'</title><rect width="1920" height="1080" fill="'+BG+'"/><g font-family="DejaVu Sans, sans-serif">'+t(70,90,title,46,weight=700)+t(70,142,sub,24,MUTED)+body+t(70,1016,foot,22,MUTED)+'</g></svg>'
def save(name,title,sub,body,foot):
    p=OUT/(name+'.svg');p.write_text(shell(title,sub,body,foot),encoding='utf-8')
    exe=shutil.which('inkscape')
    if exe:subprocess.run([exe,str(p),'--export-type=png','--export-filename='+str(p.with_suffix('.png')),'--export-width=1920','--export-height=1080'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def main():
    b=''
    cards=[(70,'MEDIR','TCRT5000','Uma marca → um pulso','GPIO4 · leitura analógica',BLUE),(690,'DECIDIR','ESP32','Desejado − medido = erro','Compensação no firmware',ORANGE),(1310,'ACIONAR','IRLZ44N','PWM → ventoinha de 12 V','GPIO21 · saída PWM',PURPLE)]
    for x,a,c,d,e,col in cards:
        b+=group(a.lower(),rect(x,245,540,385)+t(x+34,300,a,22,col,700)+t(x+34,380,c,44,weight=700)+t(x+34,452,d,27)+t(x+34,525,e,24,MUTED))
    b+=arrow(618,430,678,430,MUTED)+arrow(1238,430,1298,430,MUTED)
    b+=group('realimentacao',arrow(1580,700,340,700,BLUE)+line([(1580,638),(1580,700)],BLUE)+line([(340,700),(340,638)],BLUE)+t(960,756,'A velocidade medida retorna ao controlador',30,BLUE,600,'middle'))
    b+=group('usb',rect(630,810,660,110)+t(960,858,'PAINEL LOCAL · USB SERIAL',26,TEAL,700,'middle')+t(960,896,'Comandos e visualização · 115200 baud',22,MUTED,anchor='middle'))
    save('01_visao_sistema','AeroLab · medir, decidir e acionar','Visão funcional do projeto — controle realimentado de velocidade',b,'Diagrama funcional. A interface mostra os dados; a compensação automática acontece no ESP32.')

    b=rect(64,192,860,710)+rect(960,192,896,710)
    b+=t(98,245,'SENSOR AVULSO · GPIO4',29,BLUE,700)+t(994,245,'ACIONAMENTO · GPIO21',29,PURPLE,700)
    # Sensor: duas ramificações independentes e sinal no coletor.
    sensor=line([(180,310),(700,310)],RED)+t(110,320,'3V3',25,RED,700)
    sensor+=line([(350,310),(350,360)],RED)+rect(330,360,40,90,'#fff2cc','#a67a14',0)+line([(350,450),(350,540)],RED)+t(390,415,'220 Ω',25)
    sensor+=circle(350,580,40,'#cdebf7',BLUE)+t(350,588,'IR',25,BLUE,700,'middle')+line([(350,620),(350,770)],INK)+t(168,560,'Ânodo (+)',22)+t(160,646,'Cátodo (−)',22)
    sensor+=line([(700,310),(700,360)],RED)+rect(680,360,40,90,'#fff2cc','#a67a14',0)+line([(700,450),(700,540)],BLUE)+t(750,415,'10 kΩ',25)
    sensor+=circle(700,585,45,'#e5eaf0',INK)+t(700,594,'Foto',21,INK,600,'middle')+line([(700,630),(700,770)],INK)
    sensor+=line([(700,500),(835,500)],BLUE)+circle(700,500,7,BLUE)+t(795,477,'GPIO4',22,BLUE,700,'middle')
    sensor+=t(548,530,'Coletor',22)+t(745,660,'Emissor',22)+line([(180,770),(835,770)],INK)+t(180,815,'GND · mesmo referencial do ESP32',23,MUTED)
    sensor+=arrow(414,580,640,580,ORANGE,4,'6 9')+t(530,620,'reflexão',20,ORANGE,anchor='middle')
    b+=group('circuito_sensor',sensor)
    # Estágio de potência funcional: conexões por nome; não desenho de pernas físicas.
    power=t(1665,314,'+12 V',27,RED,700,'middle')+line([(1665,330),(1665,372)],RED)
    power+=rect(1555,372,220,106,'#fff',INK,10)+t(1665,418,'VENTOINHA',24,weight=700,anchor='middle')+t(1665,455,'12 V · 2 fios',22,MUTED,anchor='middle')
    power+=line([(1665,478),(1665,555)],BLUE)
    power+=rect(1515,555,260,150,'#26384c','#26384c',12)+t(1645,620,'IRLZ44N',29,'white',700,'middle')+t(1535,652,'G',22,'white',700)+t(1665,580,'D',22,'white',700,'middle')+t(1665,693,'S',22,'white',700,'middle')
    power+=t(1004,566,'GPIO21',25,PURPLE,700)+line([(1010,610),(1170,610)],PURPLE)+rect(1170,590,105,40,'#fff2cc','#a67a14',0)+t(1222,570,'220 Ω',24,anchor='middle')+line([(1275,610),(1515,610)],PURPLE)
    power+=circle(1400,610,7,PURPLE)+line([(1400,610),(1400,680)],INK)+rect(1380,680,40,70,'#fff2cc','#a67a14',0)+t(1326,720,'10 kΩ',23,anchor='end')+line([(1400,750),(1400,805)],INK)
    power+=line([(1665,705),(1665,805)],INK)+line([(1060,805),(1790,805)],INK)+circle(1400,805,7,INK)+circle(1665,805,7,INK)
    power+=t(1004,855,'GND comum: ESP32 + fonte (−) + sensor + source',23,MUTED)
    b+=group('circuito_mosfet',power)
    b+=t(70,956,'Referência atualizada do esquema anterior: GPIO25 → GPIO21. Resistores conforme documentação original.',24,MUTED)
    save('02_esquema_gpio21','Esquema de referência · sensor e acionamento','ESP32 por USB · TCRT5000 avulso em 3,3 V · fonte de 12 V para a ventoinha',b,'Funções elétricas, não ordem física das pernas. Conferir a montagem real; corrente e aquecimento não caracterizados.')

    b=rect(70,205,800,715)+rect(920,205,930,715)
    fan=circle(450,550,250,'#e7edf4')
    for i in range(9):
        a=2*math.pi*i/9
        pts=[]
        for r,ang in [(60,a-.15),(220,a-.15),(235,a+.30),(90,a+.48)]:pts.append((450+r*math.cos(ang),550+r*math.sin(ang)))
        fan+='<polygon points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'" fill="#9baec0"/>'
    fan+=circle(450,550,65,INK)+rect(618,535,42,34,'white','#627b94',3)
    b+=group('rotor_nove_pas',fan)+t(450,855,'9 pás · só uma marca refletiva',29,weight=600,anchor='middle')
    b+=group('pulso',t(970,296,'CADA VOLTA COMPLETA',25,BLUE,700)+t(970,368,'1 passagem → 1 pulso',43,weight=700)+line([(980,550),(1120,550),(1120,450),(1250,450),(1250,550),(1670,550)],BLUE,7)+t(980,625,'Conta uma borda; espera a marca sair.',27,MUTED)+t(980,714,'Exemplo: 30 pulsos em 1 s',31,weight=600)+t(980,778,'30 × 60 = 1800 RPM',42,ORANGE,700)+t(980,852,'PULSOS_POR_VOLTA = 1',25,BLUE,600,mono=True))
    save('03_um_pulso_por_volta','Uma marca transforma passagem em rotação','Ilustração conceitual — o rotor desenhado não é um CAD da ventoinha real',b,'Exemplo didático. A forma do pulso está simplificada; não representa uma captura do sinal analógico.')

    b=rect(70,225,540,210,'#fff7ed','#f0d3b5')+t(110,285,'DESEJADO · SETPOINT',25,ORANGE,700)+t(110,378,'2000 RPM',64,ORANGE,700)
    b+=rect(690,225,540,210,'#eff6ff','#c8dbed')+t(730,285,'MEDIDO',25,BLUE,700)+t(730,378,'1600 RPM',64,BLUE,700)
    b+=rect(1310,225,540,210)+t(1350,285,'ERRO = DESEJADO − MEDIDO',22,MUTED,700)+t(1350,378,'+400 RPM',60,weight=700)
    b+=group('calculo',t(960,550,'400 × 0,005 = +2 pontos percentuais/s',43,PURPLE,700,'middle')+t(960,625,'Após 1 s: PWM de 50% → 52%',37,weight=600,anchor='middle'))
    b+=rect(230,710,1460,185)+t(280,770,'Abaixo do alvo: aumenta PWM. Acima do alvo: diminui PWM.',31)+t(280,832,'Margem ±60 RPM · Correção máxima ±5 p.p./s · Saída entre 0 e 100%',27,MUTED)
    save('04_compensacao','Como o erro corrige o acionamento','EXEMPLO DIDÁTICO · valores ilustrativos, sem dados experimentais',b,'O ganho é um ajuste do controlador. A mesma mudança de PWM não garante uma mudança fixa de RPM.')

    b=rect(70,220,1780,690)
    items=[(360,ORANGE,8,None,'RPM desejado','Referência principal · eixo esquerdo'),(555,BLUE,5,None,'RPM medido','Velocidade calculada pelo sensor · eixo esquerdo'),(750,PURPLE,5,'2 15','PWM aplicado','Percentual de acionamento · eixo direito, 0–100%')]
    for y,col,w,dash,title,sub in items:
        b+=line([(130,y),(420,y)],col,w,dash)+t(480,y+10,title,41,col,700)+t(480,y+67,sub,27,MUTED)
    save('05_legenda_grafico','Três variáveis, três leituras','As cores seguem o painel AeroLab incluído neste pacote',b,'Legenda, sem série de dados. A demonstração real deve vir da interface conectada ao ESP32.')

    index=json.loads((ROOT/'video/trechos_codigo/indice.json').read_text())
    titles=['Leitura do sensor','Contagem com histerese','Cálculo de RPM','Compensação automática','Recebimento pela serial','Aplicação do PWM']
    for i,(item,title) in enumerate(zip(index,titles),1):
        lines=(ROOT/'video/trechos_codigo'/item['arquivo']).read_text().splitlines()
        size=29 if len(lines)<=16 else 24
        step=min(48,650/max(1,len(lines)))
        b=rect(70,205,1780,720,'#16263a','#16263a')
        for j,l in enumerate(lines):
            b+=t(103,260+j*step,str(item['linha_inicial']+j),19,'#7e98b0',mono=True)+t(170,260+j*step,l,size,'#eaf1fa',mono=True)
        save(f'codigo_{i:02}',title,'Trecho real do firmware principal · código preservado',b,f"Fonte: {item['origem']} · linhas {item['linha_inicial']}–{item['linha_final']}")
    print('11 SVGs gerados'+(' e PNGs renderizados.' if shutil.which('inkscape') else '; instale Inkscape para renderizar PNGs.'))

if __name__=='__main__':main()
