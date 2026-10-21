void lerComando() {
  while (Serial.available()) {
    char caractere = Serial.read();
    if (caractere == '\n' || caractere == '\r') {
      executarComando();
      comando = "";
    } else if (comando.length() < 20) {
      comando += caractere;
    }
  }
}
