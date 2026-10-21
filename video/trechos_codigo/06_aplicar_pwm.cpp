void ajustarVelocidade(int percentual) {
  potencia = percentual;
  int pwm = map(percentual, 0, 100, 0, 255);
  analogWrite(VENTOINHA, pwm);
  Serial.printf("PWM ajustado para %d%%\n", potencia);
}
