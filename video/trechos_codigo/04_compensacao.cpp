void controlarRPM(float rpmAtual, unsigned long intervalo) {
  if (!modoRPM) return;

  float erro = rpmDesejado - rpmAtual;

  // A leitura de 1 pulso/volta em janelas de 1 s tem passos de ~60 RPM.
  if (rpmAtual > 0 && erro >= -MARGEM_RPM && erro <= MARGEM_RPM) return;

  float ajuste = erro * GANHO_RPM;
  if (rpmAtual == 0) ajuste = AJUSTE_MAXIMO_POR_SEGUNDO;
  ajuste = constrain(ajuste, -AJUSTE_MAXIMO_POR_SEGUNDO,
                     AJUSTE_MAXIMO_POR_SEGUNDO);

  controlePWM += ajuste * (intervalo / 1000.0f);
  controlePWM = constrain(controlePWM, 0.0f, 100.0f);
  int novoPercentual = (int)(controlePWM + 0.5f);

  if (novoPercentual != potencia) ajustarVelocidade(novoPercentual);
}
