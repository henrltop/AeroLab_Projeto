(function(){
'use strict';
const $=id=>document.getElementById(id), P=AeroProtocol;
const state={source:'none',status:'disconnected',samples:[],logs:[],last:null,lastAt:0,started:0,mode:'pwm',draft:{pwm:50,rpm:1500},confirmedMode:'pwm',target:null,pwm:null,pending:null,pendingTimer:null,paused:false,pauseAt:0,window:120,visible:{rpm:true,target:true,pwm:true},hover:null,demo:null};
const number=new Intl.NumberFormat('pt-BR',{maximumFractionDigits:0});
let toastTimer, demoTimer, drawQueued=false;
const colors={rpm:'#2478c8',target:'#c66a16',pwm:'#8656b9'};
const timeText=t=>new Date(t).toLocaleTimeString('pt-BR',{hour12:false});
function toast(message,error=false){clearTimeout(toastTimer);$('toast').textContent=message;$('toast').classList.toggle('error',error);$('toast').classList.remove('hidden');toastTimer=setTimeout(()=>$('toast').classList.add('hidden'),6500);}
function log(text,type='rx'){
 const item={t:Date.now(),text:String(text),type};state.logs.push(item);if(state.logs.length>100)state.logs.shift();
 const el=$('serialLog'), nearBottom=el.scrollHeight-el.scrollTop-el.clientHeight<45;
 if(el.querySelector('.log-placeholder'))el.textContent='';
 const row=document.createElement('div');row.className='log-line '+type;
 const clock=document.createElement('span');clock.className='log-time';clock.textContent=timeText(item.t);
 const body=document.createElement('span');body.className='log-text';body.textContent=(type==='tx'?'→ ':'')+item.text;
 row.append(clock,body);el.append(row);while(el.children.length>100)el.firstElementChild.remove();if(nearBottom)el.scrollTop=el.scrollHeight;
 $('logCount').textContent=state.logs.length+' eventos';
}
function clearPending(){clearTimeout(state.pendingTimer);state.pending=null;$('pendingBanner').classList.add('hidden');}
function addSample(data,t=Date.now()){
 if(!state.started)state.started=t;
 const sample={...data,t,source:state.source==='demo'?'simulado':'esp32_usb'};
 state.samples.push(sample);if(state.samples.length>12000)state.samples.shift();state.last=sample;state.lastAt=t;state.pwm=data.pwm;state.confirmedMode=data.mode;state.target=data.target;
 if(state.pending&&((state.pending.mode==='rpm'&&data.target===state.pending.value)||(state.pending.mode==='pwm'&&data.mode==='pwm'&&data.pwm===state.pending.value)))clearPending();
 renderMetrics();updateStatus();scheduleDraw();
}
function acceptLine(line){
 log(line);const event=P.parseLine(line);if(!event)return;
 if(event.type==='sample'){addSample(event);return;}
 if(event.type==='rpm_ack'){state.confirmedMode='rpm';state.target=event.target;if(state.pending?.mode==='rpm'&&state.pending.value===event.target){clearPending();toast('Alvo de '+number.format(event.target)+' RPM confirmado.');}}
 if(event.type==='pwm_ack'){state.pwm=event.pwm;if(state.pending?.mode==='pwm'&&state.pending.value===event.pwm){state.confirmedMode='pwm';state.target=null;clearPending();toast(event.pwm===0?'Comando de parada confirmado.':'PWM de '+event.pwm+'% confirmado.');}}
 if(event.type==='rejected'){clearPending();toast('O ESP32 rejeitou o comando. Confira o sketch completo incluído no pacote.',true);}
 if(event.type==='boot'){state.confirmedMode='pwm';state.target=null;clearPending();log('Placa reiniciada. Aguardando telemetria; nenhum comando foi reaplicado.','event');}
 renderMetrics();
}
function resetSession(source){clearPending();state.source=source;state.samples=[];state.logs=[];state.last=null;state.lastAt=0;state.started=Date.now();state.target=null;state.pwm=null;state.confirmedMode='pwm';state.paused=false;state.hover=null;$('serialLog').innerHTML='<div class="log-placeholder">As leituras e os comandos enviados aparecerão aqui.</div>';$('logCount').textContent='0 eventos';$('pauseBtn').textContent='Ⅱ';$('pausedBadge').classList.add('hidden');renderMetrics();scheduleDraw();}
function controlsEnabled(){return state.source==='demo'||state.status==='connected';}
function updateStatus(){
 const pill=$('connectionPill'), label=pill.querySelector('span');pill.className='status-pill';
 let text='Desconectado',detail='Conecte por USB para receber os dados reais.';
 if(state.source==='demo'){text='Demonstração';detail='Simulação local · dados e comandos fictícios';pill.classList.add('demo');}
 else if(state.status==='opening'){text='Selecionando porta';detail='Escolha o ESP32 na janela do navegador.';}
 else if(state.status==='connected'){
  if(!state.lastAt){text='USB conectado';detail='Aguardando a primeira leitura. A placa pode reiniciar ao conectar.';}
  else if(Date.now()-state.lastAt>4500){text='Sem telemetria';detail='USB aberto, mas sem novas leituras. Confira o sketch e a conexão.';pill.classList.add('stale');}
  else{text='Recebendo dados';detail='ESP32 via USB · atualização de aproximadamente 1 s';pill.classList.add('live');}
 }
 label.textContent=text;$('connectionDetail').textContent=detail;
 $('connectBtn').querySelector('span').textContent=state.status==='connected'?'Desconectar':state.status==='opening'?'Conectando…':'Conectar ESP32';
 $('connectBtn').disabled=state.status==='opening';$('demoBtn').disabled=state.status==='connected'||state.status==='opening';$('demoBtn').textContent=state.source==='demo'?'Encerrar demonstração':'Ver demonstração';
 $('applyBtn').disabled=!controlsEnabled();$('stopBtn').disabled=!controlsEnabled();$('demoBanner').classList.toggle('hidden',state.source!=='demo');
 $('pauseBtn').disabled=!state.samples.length;$('exportBtn').disabled=!state.samples.length;
 if(state.lastAt)$('lastUpdate').textContent=(state.source==='demo'?'Simulação':'Última leitura')+' · '+timeText(state.lastAt);else $('lastUpdate').textContent='Nenhuma leitura recebida';
}
function renderMetrics(){
 const last=state.last;
 $('rpmMetric').textContent=last?number.format(last.rpm):'—';$('pwmMetric').textContent=state.pwm==null?'—':number.format(state.pwm);
 $('targetMetric').textContent=state.confirmedMode==='rpm'&&state.target!=null?number.format(state.target):'—';$('passesMetric').textContent=last?number.format(last.passes):'—';
 $('pwmMeter').style.width=(state.pwm??0)+'%';$('targetFoot').textContent=state.confirmedMode==='rpm'?'Alvo confirmado pelo controlador':'Defina e aplique um RPM alvo';
 $('activeModeBadge').textContent=state.confirmedMode==='rpm'?'RPM ATIVO':'MANUAL';
 if(last){const error=state.confirmedMode==='rpm'&&state.target!=null?last.rpm-state.target:null;$('rpmFoot').textContent=error==null?(state.source==='demo'?'Leitura simulada':'Leitura do TCRT5000'):(Math.abs(error)<=60?'Próximo do alvo':(error>0?'+':'')+number.format(error)+' RPM em relação ao alvo');}else $('rpmFoot').textContent='Aguardando primeira leitura';
 $('pwmFoot').textContent=state.source==='demo'?'PWM simulado':'Comando informado pelo ESP32';
 $('samplesLabel').textContent=number.format(state.samples.length)+' amostras na sessão';$('chartEmpty').classList.toggle('hidden',state.samples.length>0);$('exportBtn').disabled=!state.samples.length;
 updateDraftStyles();
}
function selectMode(mode){state.mode=mode;const rpm=mode==='rpm';document.querySelector('.control-panel').classList.toggle('rpm-mode',rpm);$('modePwm').classList.toggle('selected',!rpm);$('modeRpm').classList.toggle('selected',rpm);$('modePwm').setAttribute('aria-pressed',String(!rpm));$('modeRpm').setAttribute('aria-pressed',String(rpm));$('controlModeLabel').textContent=rpm?'Rotação desejada':'Percentual de PWM';$('setpointUnit').textContent=rpm?'RPM':'%';$('setpointInput').max=rpm?'50000':'100';$('setpointInput').setAttribute('aria-label',rpm?'RPM desejado':'Percentual de PWM desejado');$('applyBtn').querySelector('span').textContent=rpm?'Aplicar RPM alvo':'Aplicar percentual';$('controlHint').textContent=rpm?'O controlador ajusta o PWM gradualmente. O alvo precisa estar na faixa alcançável da ventoinha.':'O percentual define o PWM. A rotação resultante é medida pelo sensor.';
 $('presets').textContent='';for(const value of rpm?[1000,1500,2000,2500]:[25,50,75,100]){const b=document.createElement('button');b.dataset.value=value;b.textContent=number.format(value)+(rpm?'':'%');b.addEventListener('click',()=>setDraft(value));$('presets').append(b);}setDraft(state.draft[mode]);}
function setDraft(value){state.draft[state.mode]=value;$('setpointInput').value=value;updateDraftStyles();}
function updateDraftStyles(){const rpm=state.mode==='rpm';const value=Number($('setpointInput').value);const max=rpm?Math.min(50000,Math.max(3000,Math.ceil(Math.max(value,1)/1000)*1000)):100;$('setpointSlider').max=max;$('setpointSlider').step=rpm?50:1;$('setpointSlider').value=Number.isFinite(value)?Math.min(value,max):0;$('sliderMaxLabel').textContent=number.format(max)+(rpm?' RPM':'%');const percent=Math.max(0,Math.min(100,(value/max)*100));$('setpointSlider').style.background=`linear-gradient(90deg,#2b9987 ${percent}%,#e5eeeb ${percent}%)`;document.querySelectorAll('#presets button').forEach(b=>b.classList.toggle('chosen',Number(b.dataset.value)===value));}
async function sendControl(mode,value){
 if(mode==='rpm'&&Number(value)===0)mode='pwm';
 let encoded;try{encoded=P.encodeCommand(mode,value);}catch(e){toast(e.message,true);return;}
 if(!controlsEnabled()){toast('Conecte o ESP32 ou inicie a demonstração.',true);return;}
 const n=Number(value);clearPending();state.pending={mode,value:n};$('pendingBanner').textContent='Enviando '+(mode==='rpm'?number.format(n)+' RPM':n+'% de PWM')+' · aguardando confirmação do ESP32';$('pendingBanner').classList.remove('hidden');
 log(encoded.trim(),'tx');
 try{
  if(state.source==='demo'){
   if(mode==='rpm'&&n>0){state.demo.mode='rpm';state.demo.target=n;if(state.demo.pwm===0)state.demo.pwm=100;acceptLine('Modo RPM: alvo de '+n+' RPM');}
   else{state.demo.mode='pwm';state.demo.target=null;state.demo.pwm=n;acceptLine('PWM ajustado para '+n+'%');}
   clearPending();renderMetrics();return;
  }
  await link.send(encoded);
  if(state.pending)state.pendingTimer=setTimeout(()=>{if(state.pending){clearPending();toast('Comando enviado, mas sem confirmação. Confira o registro e o firmware.',true);}},4000);
 }catch(e){clearPending();toast('Não foi possível enviar: '+e.message,true);}
}
const link=new AeroSerial.SerialLink(navigator.serial,{
 line:acceptLine,
 state:(status)=>{
  if(status==='connected'){stopDemo(false);resetSession('usb');state.status=status;log('Porta USB aberta a 115200 baud.','event');}
  else{state.status=status;if(status==='disconnected'&&state.source==='usb'){clearPending();log('Conexão USB encerrada. Fechar a porta não corta a fonte de 12 V.','event');}}
  updateStatus();
 },error:e=>{log('USB: '+e.message,'event');toast('Falha na comunicação USB. Confira o registro serial.',true);}
});
async function connectClick(){
 if(state.status==='connected'){try{await link.close();toast('Porta fechada. Foi tentado o envio de 0% antes de desconectar.');}catch(e){toast('Falha ao fechar a porta: '+e.message,true);}return;}
 if(!('serial' in navigator)){toast('Abra o painel no Chrome ou Edge do computador para conectar por USB.',true);$('helpDialog').showModal();return;}
 if(!window.isSecureContext){toast('Abra o arquivo local ou execute o iniciador para acessar em localhost.',true);return;}
 try{await link.open();}catch(e){if(e.name==='NotFoundError')toast('Nenhuma porta foi selecionada.');else toast('Não foi possível abrir a porta. Feche o Monitor Serial da IDE e tente novamente. '+e.message,true);updateStatus();}
}
function stopDemo(reset=true){clearInterval(demoTimer);demoTimer=null;if(state.source==='demo'){if(reset){resetSession('none');state.status='disconnected';}state.demo=null;}updateStatus();}
function startDemo(){
 if(state.status==='connected'||state.status==='opening')return;
 if(state.source==='demo'){stopDemo();return;}
 resetSession('demo');state.status='disconnected';state.demo={pwm:69,rpm:2000,mode:'rpm',target:2000,passes:0};
 const now=Date.now();for(let i=0;i<90;i++){const target=i<30?1400:2000;const pwm=i<30?48:i<43?55+(i-30):69;const rpm=Math.round((pwm*29+Math.sin(i*.3)*35)/60)*60;const s={rpm,pwm,target,mode:'rpm',passes:Math.max(0,Math.round(i*28))};addSample(s,now-(89-i)*1000);}
 state.started=now-89000;state.demo.passes=state.last.passes;log('Demonstração iniciada. Todos os dados desta sessão são simulados.','event');
 demoTimer=setInterval(()=>{
  const m=state.demo;if(!m)return;
  if(m.mode==='rpm'){const error=m.target-m.rpm;if(Math.abs(error)>60)m.pwm=Math.max(0,Math.min(100,m.pwm+Math.max(-5,Math.min(5,error*.005))));}
  const expected=m.pwm<17?0:m.pwm*29;m.rpm=Math.max(0,m.rpm+(expected-m.rpm)*.65+Math.sin(Date.now()/2100)*12);const rpm=Math.round(m.rpm/60)*60;m.passes+=Math.round(rpm/60);
  acceptLine(`PWM: ${Math.round(m.pwm)}% | RPM: ${rpm} | Passagens: ${m.passes}`+(m.mode==='rpm'?` | Alvo: ${m.target} RPM`:''));
 },1000);updateStatus();
}
function download(text,type,name){const url=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function exportCsv(){if(!state.samples.length)return;const stamp=new Date().toISOString().replace(/[:.]/g,'-');download(P.csv(state.samples),'text/csv;charset=utf-8',`AeroLab_${state.source==='demo'?'SIMULACAO':'ESP32'}_${stamp}.csv`);toast('CSV exportado com '+state.samples.length+' amostras.');}
function scheduleDraw(){if(drawQueued)return;drawQueued=true;requestAnimationFrame(()=>{drawQueued=false;drawChart();});}
function chartData(){const end=state.paused?state.pauseAt:Date.now(),start=end-state.window*1000;return {end,start,points:state.samples.filter(s=>s.t>=start&&s.t<=end)};}
function drawChart(){
 const canvas=$('chart'),rect=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1;if(rect.width<20)return;const W=rect.width,H=rect.height;canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);const ctx=canvas.getContext('2d');ctx.scale(dpr,dpr);ctx.clearRect(0,0,W,H);
 const pad={l:44,r:37,t:22,b:35},w=W-pad.l-pad.r,h=H-pad.t-pad.b;const {start,end,points}=chartData();
 let peak=1000;for(const s of points){if(state.visible.rpm)peak=Math.max(peak,s.rpm);if(state.visible.target&&s.target!=null)peak=Math.max(peak,s.target);}const maxRPM=Math.ceil(peak*1.12/500)*500;
 const x=t=>pad.l+(t-start)/(end-start)*w,y=rpm=>pad.t+h-Math.max(0,rpm)/maxRPM*h,yp=pwm=>pad.t+h-pwm/100*h;
 ctx.font='9px Segoe UI, Arial';ctx.textBaseline='middle';
 for(let i=0;i<=4;i++){const yy=pad.t+h*i/4;ctx.strokeStyle='#edf1f2';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad.l,yy);ctx.lineTo(pad.l+w,yy);ctx.stroke();ctx.fillStyle='#a4b0b5';ctx.textAlign='right';ctx.fillText(number.format(maxRPM*(1-i/4)),pad.l-9,yy);ctx.textAlign='left';ctx.fillText(String(100-i*25)+'%',pad.l+w+8,yy);}
 ctx.fillStyle='#9eacb2';ctx.textAlign='left';ctx.fillText('RPM',pad.l-21,8);ctx.textAlign='right';ctx.fillStyle=colors.pwm;ctx.fillText('PWM',W-1,8);
 for(let i=0;i<=4;i++){const xx=pad.l+w*i/4;ctx.textAlign=i===0?'left':i===4?'right':'center';ctx.fillStyle='#a4b0b5';ctx.fillText(timeText(start+(end-start)*i/4),xx,H-13);}
 function chunks(key){const groups=[];let group=[];for(const s of points){if(s[key]==null||(group.length&&s.t-group[group.length-1].t>3500)){if(group.length)groups.push(group);group=[];}if(s[key]!=null)group.push(s);}if(group.length)groups.push(group);return groups;}
 if(state.visible.rpm){for(const group of chunks('rpm')){if(group.length<2)continue;ctx.beginPath();ctx.moveTo(x(group[0].t),pad.t+h);for(const s of group)ctx.lineTo(x(s.t),y(s.rpm));ctx.lineTo(x(group[group.length-1].t),pad.t+h);ctx.closePath();const gradient=ctx.createLinearGradient(0,pad.t,0,pad.t+h);gradient.addColorStop(0,'#2478c80b');gradient.addColorStop(1,'#2478c801');ctx.fillStyle=gradient;ctx.fill();}}
 for(const key of ['pwm','rpm','target']){if(!state.visible[key])continue;ctx.lineWidth=key==='target'?3.2:key==='rpm'?1.7:1.3;ctx.lineCap='round';ctx.strokeStyle=colors[key];ctx.setLineDash(key==='pwm'?[1,5]:[]);for(const group of chunks(key)){ctx.beginPath();for(let i=0;i<group.length;i++){const px=x(group[i].t),py=key==='pwm'?yp(group[i][key]):y(group[i][key]);if(i===0)ctx.moveTo(px,py);else{if(key!=='rpm')ctx.lineTo(px,key==='pwm'?yp(group[i-1][key]):y(group[i-1][key]));ctx.lineTo(px,py);}}ctx.stroke();}ctx.setLineDash([]);}
 if(state.visible.rpm&&points.length){const s=points[points.length-1];ctx.fillStyle=colors.rpm;ctx.beginPath();ctx.arc(x(s.t),y(s.rpm),3.2,0,Math.PI*2);ctx.fill();}
 if(state.hover!=null&&points.length){const time=start+Math.max(0,Math.min(1,(state.hover-pad.l)/w))*(end-start);let sample=points[0];for(const s of points)if(Math.abs(s.t-time)<Math.abs(sample.t-time))sample=s;const xx=x(sample.t);ctx.strokeStyle='#b4c9c3';ctx.lineWidth=1;ctx.setLineDash([3,4]);ctx.beginPath();ctx.moveTo(xx,pad.t);ctx.lineTo(xx,pad.t+h);ctx.stroke();ctx.setLineDash([]);const tip=$('chartTooltip');tip.textContent='';const title=document.createElement('strong');title.textContent=timeText(sample.t);tip.append(title);for(const [label,value]of [['RPM medido',number.format(sample.rpm)],['RPM desejado',sample.target==null?'—':number.format(sample.target)],['PWM',sample.pwm+'%']]){const row=document.createElement('div'),a=document.createElement('span'),b=document.createElement('b');a.textContent=label;b.textContent=value;row.append(a,b);tip.append(row);}tip.style.left=Math.max(8,Math.min(W-175,xx+12))+'px';tip.classList.remove('hidden');}else $('chartTooltip').classList.add('hidden');
}
$('connectBtn').addEventListener('click',connectClick);$('demoBtn').addEventListener('click',startDemo);$('emptyDemo').addEventListener('click',startDemo);$('exitDemo').addEventListener('click',()=>stopDemo());
$('modePwm').addEventListener('click',()=>selectMode('pwm'));$('modeRpm').addEventListener('click',()=>selectMode('rpm'));
$('setpointInput').addEventListener('input',()=>{state.draft[state.mode]=Number($('setpointInput').value);updateDraftStyles();});$('setpointInput').addEventListener('keydown',e=>{if(e.key==='Enter'&&controlsEnabled())sendControl(state.mode,$('setpointInput').value);});$('setpointSlider').addEventListener('input',()=>setDraft(Number($('setpointSlider').value)));
$('applyBtn').addEventListener('click',()=>sendControl(state.mode,$('setpointInput').value));$('stopBtn').addEventListener('click',()=>sendControl('pwm',0));
$('pauseBtn').addEventListener('click',()=>{state.paused=!state.paused;if(state.paused)state.pauseAt=Date.now();$('pauseBtn').textContent=state.paused?'▷':'Ⅱ';$('pauseBtn').setAttribute('aria-label',state.paused?'Retomar gráfico':'Pausar gráfico');$('pausedBadge').classList.toggle('hidden',!state.paused);state.hover=null;scheduleDraw();});
$('windowSelect').addEventListener('change',()=>{state.window=Number($('windowSelect').value);scheduleDraw();});document.querySelectorAll('[data-series]').forEach(b=>b.addEventListener('click',()=>{state.visible[b.dataset.series]=!state.visible[b.dataset.series];b.setAttribute('aria-pressed',String(state.visible[b.dataset.series]));scheduleDraw();}));
$('chart').addEventListener('pointermove',e=>{state.hover=e.clientX-$('chart').getBoundingClientRect().left;scheduleDraw();});$('chart').addEventListener('pointerleave',()=>{state.hover=null;scheduleDraw();});
$('exportBtn').addEventListener('click',exportCsv);$('clearLog').addEventListener('click',()=>{state.logs=[];$('serialLog').innerHTML='<div class="log-placeholder">Registro limpo. As próximas mensagens aparecerão aqui.</div>';$('logCount').textContent='0 eventos';});
for(const b of document.querySelectorAll('.help-trigger'))b.addEventListener('click',()=>$('helpDialog').showModal());$('closeHelp').addEventListener('click',()=>$('helpDialog').close());$('helpDialog').addEventListener('click',e=>{if(e.target===$('helpDialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}});
new ResizeObserver(scheduleDraw).observe($('chart').parentElement);
setInterval(()=>{updateStatus();if(state.started){const seconds=Math.floor((Date.now()-state.started)/1000);$('sessionTime').textContent='Sessão '+String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0');}if(!state.paused)scheduleDraw();},1000);
window.addEventListener('beforeunload',e=>{if(state.status==='connected'){e.preventDefault();e.returnValue='';}});
selectMode('rpm');renderMetrics();updateStatus();scheduleDraw();
})();
