"""Extrai blocos reais do firmware sem modificá-lo. Python 3."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
source=root/'firmware/Ventoinha_Percentual_RPM/Ventoinha_Percentual_RPM.ino'
lines=source.read_text(encoding='utf-8').splitlines()
specs=[('01_leitura','int leitura = analogRead(SENSOR);','int leitura = analogRead(SENSOR);'),('02_contagem','if (!marcaPresente && leitura < LIMITE_ENTRADA) {','  lerComando();'),('03_calculo_rpm','float rpm = pulsos * 60000.0 /','    Serial.printf("PWM: %d%%'),('04_compensacao','void controlarRPM(float rpmAtual, unsigned long intervalo) {','void executarComando() {'),('05_receber_serial','void lerComando() {','void setup() {'),('06_aplicar_pwm','void ajustarVelocidade(int percentual) {','void controlarRPM(')]
dest=root/'video/trechos_codigo';dest.mkdir(parents=True,exist_ok=True)
index=[]
for name,start,end in specs:
    a=next(i for i,l in enumerate(lines) if start in l)
    b=a+1 if start==end else next(i for i in range(a+1,len(lines)) if end in lines[i])
    while b>a and not lines[b-1].strip(): b-=1
    snippet='\n'.join(lines[a:b])+'\n'
    (dest/(name+'.cpp')).write_text(snippet,encoding='utf-8')
    index.append({'id':name,'arquivo':name+'.cpp','origem':source.relative_to(root).as_posix(),'linha_inicial':a+1,'linha_final':b})
(dest/'indice.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Seis trechos extraídos do firmware principal.')
