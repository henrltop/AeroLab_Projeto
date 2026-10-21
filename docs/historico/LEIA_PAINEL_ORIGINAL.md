# AeroLab — painel da ventoinha

Interface local para a montagem do Henrique: ventoinha de 12 V e dois fios, sensor TCRT5000 avulso no GPIO4 e IRLZ44N comandado pelo GPIO21. A contagem continua em **1 pulso por volta**, pois só uma das nove pás tem marcação.

## Começar pelo painel
1. Abra `dist/Painel_Ventoinha.html` no **Chrome ou Edge do computador**. O HTML é independente, não baixa bibliotecas e pode ser usado sem internet. Na prévia do chat, a conexão USB pode estar bloqueada: baixe o arquivo e abra no navegador.
2. Clique em **Ver demonstração** se quiser conhecer os gráficos e os controles sem uma placa. A faixa amarela identifica dados simulados. A demonstração nunca envia comandos ao hardware.
3. Para usar a montagem real, conecte o ESP32 por USB e **feche o Monitor Serial e o Plotter Serial da Arduino IDE**, além de outros programas que usem a mesma porta.
4. Clique em **Conectar ESP32**, escolha a porta da placa e aguarde a primeira leitura. A comunicação usa 115200 baud.
5. Selecione **Percentual** ou **RPM alvo**, ajuste o valor e clique em **Aplicar**. Mover o controle deslizante não envia comandos até aplicar. O atalho Enter no campo numérico também aplica o valor.
6. **Parar ventoinha** envia 0% ao ESP32. O comando é confirmado pela resposta serial, quando recebida.

Se a conexão pelo arquivo local for bloqueada no seu navegador, extraia o pacote e execute `Iniciar_Painel_Windows.bat`. Com Python 3 instalado, ele abre um servidor somente em `127.0.0.1`, em uma porta disponível. Mantenha a janela aberta enquanto usa o painel. No Linux/macOS, o equivalente é `python3 server_local.py` e abrir o endereço no Chrome.

## Firmware e o erro no anexo
O texto anexado era um log de compilação, não um sketch completo: o código estava começando com uma chave `}` e faltavam as declarações iniciais. O pacote inclui:

`firmware/Ventoinha_Percentual_RPM/Ventoinha_Percentual_RPM.ino`

Abra esse `.ino` completo na Arduino IDE e envie para a placa, se necessário. Não acrescente ao final de um sketch incompleto. O arquivo deve começar com `#include <Arduino.h>`.

O sketch incluído é o código completo anterior, com os mesmos pinos, limiares 1300/2350, PWM de 1000 Hz, uma marca por volta e modos percentual/RPM. Não foi alterada a eletrônica nem a contagem para criar a interface. O painel também reconhece as leituras do sketch original de percentual; para aceitar comandos de RPM, o firmware precisa ter o modo RPM.

**Ao iniciar ou reiniciar, o sketch incluído aplica 100% de PWM**, como no código anterior. Abrir uma porta USB pode reiniciar algumas placas. A interface não reenvia automaticamente um ponto de operação depois de uma reinicialização.

## O que aparece no gráfico
- **Laranja, linha contínua mais espessa:** RPM desejado (setpoint) confirmado pelo firmware, eixo esquerdo. Aparece apenas durante o modo RPM.
- **Azul, linha fina:** RPM medido pelo sensor, eixo esquerdo.
- **Roxo pontilhado:** PWM aplicado, eixo direito de 0–100%.
- O setpoint ocupa o primeiro cartão, e o controle começa visualmente no modo RPM alvo. Isso não envia comandos automaticamente nem altera o modo do firmware até você aplicar um valor.
- O gráfico pode mostrar os últimos 60, 120 ou 300 segundos.
- Passe o mouse para ver os valores de cada amostra e clique na legenda para ocultar/mostrar uma variável.
- **Pausar gráfico** congela apenas a visualização: aquisição, controle e registro continuam funcionando.
- Os cartões mostram RPM medido, RPM desejado, PWM e passagens ópticas informadas pelo ESP32. Sem telemetria, o painel não inventa leituras.

A chegada dos dados depende da janela de medição do seu sketch, aproximadamente uma amostra por segundo. Com um pulso por volta e uma janela de um segundo, a leitura tem passos próximos de 60 RPM. O controlador de RPM ajusta o PWM gradualmente, limitado à capacidade real da ventoinha; 50% de PWM não significa necessariamente metade do RPM máximo.

## CSV e registro
O CSV exporta todas as amostras mantidas na sessão, com timestamp do computador, origem, RPM medido, alvo, PWM e passagens. O separador é ponto e vírgula. A origem `simulado` identifica demonstração; `esp32_usb` identifica a conexão real.

Não há envio de dados para um servidor externo. A sessão fica apenas na memória do navegador e é perdida ao recarregar/fechar. O limite é de 12.000 amostras mais recentes (cerca de 3 h 20 min em 1 Hz). Exporte o CSV antes de trocar de sessão, entrar na demonstração ou fechar o painel.

O registro mostra as últimas 100 mensagens recebidas, comandos enviados e eventos da conexão. Limpar o registro não apaga as amostras do gráfico. Uma linha `PWM ajustado...` durante o modo RPM pode ser ajuste automático do controlador, e não uma troca para manual.

## Desconexão
Antes de desconectar, use **Parar ventoinha** e confira o RPM diminuindo. O botão Desconectar tenta enviar 0% antes de fechar a porta, mas isso não garante entrega se o cabo ou a comunicação já falharam. Fechar o navegador, pausar o gráfico ou fechar a porta **não corta fisicamente a fonte de 12 V**. Em perda de comunicação, os valores exibidos são as últimas leituras recebidas, não novas medições.

## Arquivos para edição
- `src/template.html`: estrutura da tela.
- `src/styles.css`: estilo responsivo.
- `src/protocol.js`: leitura das linhas seriais, comandos e CSV.
- `src/serial.js`: conexão Web Serial e tratamento dos fragmentos recebidos.
- `src/app.js`: controles, gráfico, demonstração e estado da interface.
- `build.cjs`: gera o HTML independente em `dist/` (Node.js, sem instalar pacotes).
- `tests/`: testes do protocolo, conexão com porta simulada e estrutura do HTML.

Para gerar o HTML: `node build.cjs`.
Para executar os testes: `node --test tests/*.test.cjs`.

## Validação realizada
Passaram 14 testes automatizados: leitura das mensagens reais do sketch, distinção entre RPM e percentual, validação dos valores, exportação CSV, reconstrução de mensagens fragmentadas, liberação da porta ao desconectar, parada antes do fechamento e referências dos elementos da tela. A sintaxe dos arquivos JavaScript foi conferida.

A interface não foi exercitada em um navegador controlado neste ambiente, nem conectada a um ESP32 físico. O firmware foi incluído completo, mas não recompilado neste ambiente, que não tem o toolchain Arduino instalado. A confirmação final do gráfico real e da atuação deve ser feita na sua bancada.

Referência da API Web Serial: https://developer.chrome.com/docs/capabilities/serial
