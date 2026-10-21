(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.AeroSerial=api;})(globalThis,function(){
  class SerialLink{
    constructor(api,callbacks={}){this.api=api;this.cb=callbacks;this.port=null;this.reader=null;this.writer=null;this.task=null;this.closing=false;this.opening=false;}
    async open(){
      if(this.port||this.opening)throw Error('Já existe uma conexão em andamento.');
      if(!this.api)throw Error('Use Chrome ou Edge no computador, fora da prévia do chat.');
      this.opening=true;this.cb.state?.('opening');let port;
      try{
        port=await this.api.requestPort();
        await port.open({baudRate:115200});
        this.port=port;this.closing=false;this.writer=port.writable.getWriter();this.reader=port.readable.getReader();
        this.cb.state?.('connected',port.getInfo?.()||{});
        this.task=this.readLoop(port,this.reader);
      }catch(e){
        if(port){try{this.writer?.releaseLock();}catch{}try{this.reader?.releaseLock();}catch{}try{await port.close();}catch{}}
        this.port=null;this.writer=null;this.reader=null;this.cb.state?.('disconnected');throw e;
      }finally{this.opening=false;}
    }
    async send(text){if(!this.writer||this.closing)throw Error('Conecte o ESP32 antes de enviar um comando.');await this.writer.write(new TextEncoder().encode(text));}
    async readLoop(port,reader){
      let buffer='';const decoder=new TextDecoder();
      try{
        while(true){const {value,done}=await reader.read();if(done)break;buffer+=decoder.decode(value,{stream:true});let i;while((i=buffer.indexOf('\n'))>=0){const line=buffer.slice(0,i).replace(/\r$/,'');buffer=buffer.slice(i+1);if(line.trim())this.cb.line?.(line);}if(buffer.length>8192){buffer='';this.cb.error?.(Error('Linha serial muito longa; trecho descartado.'));}}
      }catch(e){if(!this.closing)this.cb.error?.(e);}
      finally{
        try{reader.releaseLock();}catch{}
        if(!this.closing&&this.port===port){
          try{this.writer?.releaseLock();}catch{}this.writer=null;this.reader=null;this.port=null;
          try{await port.close();}catch{}
          this.cb.state?.('disconnected');
        }
      }
    }
    async close(){
      if(!this.port)return;this.closing=true;const port=this.port;
      try{
        // Melhor esforço: fechar a porta não corta a alimentação de 12 V.
        if(this.writer){try{await this.writer.write(new TextEncoder().encode('0\n'));await new Promise(r=>setTimeout(r,150));}catch{}}
        try{await this.reader?.cancel();}catch{}
        try{await this.task;}catch{}
        try{this.writer?.releaseLock();}catch{}
        await port.close();
      }finally{this.port=null;this.reader=null;this.writer=null;this.task=null;this.closing=false;this.cb.state?.('disconnected');}
    }
  }
  return {SerialLink};
});
