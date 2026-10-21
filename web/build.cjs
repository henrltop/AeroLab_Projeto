const fs=require('node:fs'),path=require('node:path');
const root=__dirname;let html=fs.readFileSync(path.join(root,'src/template.html'),'utf8');
for(const [key,file]of [['CSS','styles.css'],['PROTOCOL','protocol.js'],['SERIAL','serial.js'],['APP','app.js']]){const content=fs.readFileSync(path.join(root,'src',file),'utf8');if(key!=='CSS'&&/<\/script/i.test(content))throw Error('Script contém fechamento HTML inesperado');html=html.replace(`/*__${key}__*/`,()=>content);}
if(/\/\*__[A-Z]+__\*\//.test(html))throw Error('Placeholder não substituído');
fs.mkdirSync(path.join(root,'dist'),{recursive:true});fs.writeFileSync(path.join(root,'dist/Painel_Ventoinha.html'),html);console.log('HTML independente gerado:',Buffer.byteLength(html),'bytes');
