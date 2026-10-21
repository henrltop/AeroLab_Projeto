# Painel local

Abra `dist/Painel_Ventoinha.html` no Chrome/Edge de computador. Para a placa, feche outros programas que usam a porta serial e conecte em 115200 baud.

Alternativa de abertura: `python3 web/server_local.py` a partir da raiz, ou o `.bat` nesta pasta no Windows. A demonstração contém dados simulados e fica identificada na tela.

O firmware principal está em `../firmware/Ventoinha_Percentual_RPM/`. A documentação atual está em `../docs/interface.md`. Build e testes, a partir da raiz:

```sh
node web/build.cjs
node --test web/tests/*.test.cjs
```

Sem instalação de pacotes ou dependências externas.
