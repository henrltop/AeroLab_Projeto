# Interface e protocolo

Painel HTML/CSS/JavaScript local, sem CDN ou backend remoto. Conexão USB por Web Serial em 115200 baud; o controle em malha fechada é do firmware, não do navegador.

## Comandos reais (terminados por nova linha)

| Texto enviado | Ação |
|---|---|
| `50\n` | PWM manual 50% |
| `50%\n` | Mesmo comando aceito pelo firmware |
| `1500rpm\n` | Setpoint de 1500 RPM |
| `0\n` | Parar e sair do modo RPM |

O painel usa `50\n` para percentual e `1500rpm\n` para RPM. O limite 50000 do campo RPM é validação do protocolo e não um desempenho confirmado.

## Linhas reconhecidas — exemplos didáticos

```text
PWM: 50% | RPM: 1680 | Passagens: 144
PWM: 72% | RPM: 1974 | Passagens: 920 | Alvo: 2000 RPM
```

Os números acima não são dados experimentais armazenados. O parser também reconhece confirmações de comando, início da placa e rejeições.

## Uso

- Aplicar envia o comando; mover o slider sozinho não envia.
- Gráfico: desejado laranja forte, medido azul e PWM roxo pontilhado no eixo direito.
- Janelas visuais de 60, 120 e 300 s; legenda permite ocultar séries.
- Pausar congela a visualização, mantendo aquisição e controle.
- CSV usa `;`, timestamp do computador, origem, RPM, alvo, PWM e passagens.
- Origem `simulado` identifica demonstração; `esp32_usb` identifica USB real.
- Até 12000 amostras em memória; recarregar perde a sessão. Exportar antes de fechar.
- Demonstração é simulada e não envia comandos à placa.
- Desconectar tenta enviar zero; perda de cabo ou fechamento do navegador não garante parada física. O firmware não implementa watchdog de comunicação.

`src/protocol.js`: protocolo e CSV; `src/serial.js`: transporte; `src/app.js`: estado, controles e desenho; `src/template.html` e `styles.css`: apresentação. `build.cjs` reúne tudo em um HTML.
