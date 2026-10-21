#include <Arduino.h>

const int SENSOR = 4;
const int VENTOINHA = 21;

// Mantidos do seu codigo que ja funciona.
const int LIMITE_ENTRADA = 1300;
const int LIMITE_SAIDA = 2350;
const int PULSOS_POR_VOLTA = 1; // Nove pas, mas apenas UMA marcada.
const int FREQUENCIA_PWM = 1000;

bool marcaPresente = false;
unsigned long pulsos = 0;
unsigned long totalPassagens = 0;
unsigned long ultimaMedicao = 0;

int potencia = 100;
String comando;

// Acrescimos para o modo de RPM desejado.
bool modoRPM = false;
long rpmDesejado = 0;
float controlePWM = 100.0f;
const float GANHO_RPM = 0.005f;
const float MARGEM_RPM = 60.0f;
const float AJUSTE_MAXIMO_POR_SEGUNDO = 5.0f;

void ajustarVelocidade(int percentual) {
  potencia = percentual;
  int pwm = map(percentual, 0, 100, 0, 255);
  analogWrite(VENTOINHA, pwm);
  Serial.printf("PWM ajustado para %d%%\n", potencia);
}

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

void executarComando() {
  comando.trim();
  comando.toLowerCase();
  if (comando.length() == 0) return;

  bool pedidoRPM = comando.endsWith("rpm");
  if (pedidoRPM) comando.remove(comando.length() - 3);
  else if (comando.endsWith("%")) comando.remove(comando.length() - 1);
  comando.trim();

  char *fim;
  long valor = strtol(comando.c_str(), &fim, 10);
  bool numeroValido = fim != comando.c_str() && *fim == '\0';

  if (numeroValido && pedidoRPM && valor > 0 && valor <= 50000) {
    modoRPM = true;
    rpmDesejado = valor;
    // Se estava desligada, inicia a partida em 100%.
    if (potencia == 0) ajustarVelocidade(100);
    controlePWM = potencia;
    Serial.printf("Modo RPM: alvo de %ld RPM\n", rpmDesejado);
  } else if (numeroValido &&
             ((!pedidoRPM && valor >= 0 && valor <= 100) ||
              (pedidoRPM && valor == 0))) {
    modoRPM = false;
    rpmDesejado = 0;
    ajustarVelocidade((int)valor);
    controlePWM = potencia;
  } else {
    Serial.println("Use 50, 50% ou 1500rpm. Envie 0 para desligar.");
  }
}

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

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(SENSOR, INPUT);
  pinMode(VENTOINHA, OUTPUT);
  digitalWrite(VENTOINHA, LOW);
  analogWriteResolution(VENTOINHA, 8);
  analogWriteFrequency(VENTOINHA, FREQUENCIA_PWM);
  delay(1000);

  Serial.println("Controle e leitura de RPM iniciados.");
  Serial.println("Sensor: GPIO4 | Ventoinha: GPIO21");
  Serial.println("Envie 50 ou 50% para PWM; 1500rpm para RPM desejado.");
  Serial.println("Envie 0 para desligar.");

  ajustarVelocidade(100);
  ultimaMedicao = millis();
}

void loop() {
  int leitura = analogRead(SENSOR);

  // Mesma contagem do codigo original.
  if (!marcaPresente && leitura < LIMITE_ENTRADA) {
    marcaPresente = true;
    pulsos++;
    totalPassagens++;
  }
  if (marcaPresente && leitura > LIMITE_SAIDA) {
    marcaPresente = false;
  }

  lerComando();
  unsigned long agora = millis();
  unsigned long intervalo = agora - ultimaMedicao;

  if (intervalo >= 1000) {
    float rpm = pulsos * 60000.0 /
                (intervalo * PULSOS_POR_VOLTA);

    Serial.printf("PWM: %d%% | RPM: %.0f | Passagens: %lu",
                  potencia, rpm, totalPassagens);
    if (modoRPM) Serial.printf(" | Alvo: %ld RPM", rpmDesejado);
    Serial.println();

    pulsos = 0;
    ultimaMedicao = agora;
    controlarRPM(rpm, intervalo);
  }
}
