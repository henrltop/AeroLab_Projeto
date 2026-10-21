  if (!marcaPresente && leitura < LIMITE_ENTRADA) {
    marcaPresente = true;
    pulsos++;
    totalPassagens++;
  }
  if (marcaPresente && leitura > LIMITE_SAIDA) {
    marcaPresente = false;
  }
