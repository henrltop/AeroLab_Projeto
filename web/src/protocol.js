(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.AeroProtocol=api;})(globalThis,function(){
  function num(s){return Number(String(s).replace(',','.'));}
  function parseLine(line){
    const s=String(line).trim();
    const m=s.match(/PWM:\s*(\d+(?:[.,]\d+)?)%\s*\|\s*RPM:\s*(\d+(?:[.,]\d+)?)\s*\|\s*Passagens:\s*(\d+)/i);
    if(m){const target=s.match(/\bAlvo:\s*(\d+)\s*RPM/i);const data={rpm:num(m[2]),pwm:num(m[1]),passes:num(m[3]),target:target?num(target[1]):null,mode:target?'rpm':'pwm'};if(data.pwm>100||!Number.isSafeInteger(data.passes))return null;return {type:'sample',...data};}
    const r=s.match(/Modo RPM:\s*alvo de\s*(\d+)\s*RPM/i);if(r)return {type:'rpm_ack',target:num(r[1])};
    const p=s.match(/PWM ajustado para\s*(\d+)%/i);if(p&&num(p[1])<=100)return {type:'pwm_ack',pwm:num(p[1])};
    if(/^(Use 50|Digite somente|Comando muito longo|Primeiro envie)/i.test(s))return {type:'rejected',message:s};
    if(/^rst:|^ets Jul|^entry 0x/i.test(s))return {type:'boot'};
    return null;
  }
  function encodeCommand(mode,value){
    const n=Number(value);if(!Number.isInteger(n)||n<0||n>(mode==='rpm'?50000:100)||!['pwm','rpm'].includes(mode))throw Error('Informe um valor inteiro dentro da faixa permitida.');
    return mode==='rpm'?`${n}rpm\n`:`${n}\n`;
  }
  function csv(samples){
    return '\uFEFFsep=;\r\ntimestamp_iso;origem;rpm_medido;rpm_alvo;pwm_percentual;passagens\r\n'+samples.map(s=>[new Date(s.t).toISOString(),s.source,s.rpm,s.target??'',s.pwm,s.passes].join(';')).join('\r\n');
  }
  return {parseLine,encodeCommand,csv};
});
