# Explicação do firmware atual

Fonte principal: `firmware/Ventoinha_Percentual_RPM/Ventoinha_Percentual_RPM.ino`. O arquivo foi preservado, sem refatoração.

## Constantes e estados

| Nome | Função |
|---|---|
| `SENSOR = 4` | Entrada analógica do sensor |
| `VENTOINHA = 21` | Saída PWM para o MOSFET |
| `LIMITE_ENTRADA = 1300` | Detectar o estado de maior reflexão nesta montagem |
| `LIMITE_SAIDA = 2350` | Rearmar a próxima contagem |
| `PULSOS_POR_VOLTA = 1` | Uma marca por volta |
| `FREQUENCIA_PWM = 1000` | PWM em hertz |
| `marcaPresente` | Evitar múltiplas contagens durante a mesma passagem |
| `pulsos` | Contagem da janela de medição |
| `totalPassagens` | Contagem acumulada da sessão |
| `potencia` | Percentual inteiro aplicado; nome da variável, não potência medida em watts |
| `modoRPM` | Habilitar compensação automática |
| `rpmDesejado` | Setpoint |
| `controlePWM` | Acumulador decimal do percentual; começa em 100.0f |

## Aquisição e cálculo

`analogRead(SENSOR)` é executado continuamente no `loop()`. O ADC foi configurado para 12 bits: valores de 0 a 4095. `marcaPresente` e os dois limiares formam uma histerese de leitura.

Quando há uma nova entrada abaixo de 1300, o código soma um pulso e uma passagem. Só permite outra contagem depois de ultrapassar 2350.

`RPM = pulsos × 60000 / (intervalo_ms × pulsos_por_volta)`.

Uma janela de 1 s com um pulso por volta tem passos de aproximadamente 60 RPM. A aquisição é por consulta no laço, não interrupção. O serial e o tempo do laço podem afetar pulsos muito curtos; não foi determinado um limite experimental de frequência.

## Compensação

`controlarRPM(rpm, intervalo)` é chamado depois da janela de medição:

1. Retorna imediatamente se o modo RPM não estiver ativo.
2. Calcula `erro = rpmDesejado - rpmAtual`.
3. Se há RPM positivo e o erro está entre −60 e +60, mantém a saída.
4. Calcula `ajuste = erro × 0.005`. Se o RPM é zero, usa ajuste positivo de 5.
5. Limita o ajuste entre −5 e +5 pontos percentuais por segundo.
6. Acumula `controlePWM += ajuste × (intervalo / 1000.0f)` e limita a 0–100%.
7. Arredonda para percentual inteiro e aplica quando houver mudança.

É uma correção acumulativa baseada no erro, de natureza integral, com margem e saturação. Não é um PID completo. O ganho é escolhido para teste, não calculado a partir de uma identificação da planta.

Exemplo didático: erro +400 RPM → ajuste +2 pontos percentuais em 1 s; PWM de 50% passa a 52%, desde que os limites não interfiram. Isso não garante um aumento específico de RPM.

`ajustarVelocidade()` converte 0–100 para 0–255 com `map()` e escreve por `analogWrite()`. O sinal varia o tempo ligado; 50% de PWM não implica metade da rotação máxima.

## Serial

`lerComando()` lê caracteres com `Serial.read()` enquanto `Serial.available()` indicar dados. Acumula em `comando` e chama `executarComando()` ao receber `\n` ou `\r`.

`executarComando()` remove espaços, normaliza maiúsculas/minúsculas, verifica o sufixo `rpm` ou `%` e valida um inteiro com `strtol()`.

`50`/`50%` → manual; `1500rpm` → setpoint; `0`/`0rpm` → desligar e voltar ao manual. No modo RPM, se estava em zero, o sketch aplica 100% para partir.

## Detalhes de C++ para a apresentação

- `100.0f`: literal `float`; o `f` não é uma operação.
- `%.0f` em `Serial.printf`: exibe o número de ponto flutuante com zero casas decimais. A exibição arredondada não muda a variável.
- `unsigned long` e a subtração de `millis()` são usados para medir intervalos.
- O serial é impresso antes da nova correção de PWM, portanto a mudança normalmente aparece na amostra seguinte.
- A margem de ±60 RPM é uma decisão do controlador, não uma precisão certificada do sensor.

Os trechos para edição são extraídos automaticamente em `video/trechos_codigo/` e indexados em `indice.json`.
