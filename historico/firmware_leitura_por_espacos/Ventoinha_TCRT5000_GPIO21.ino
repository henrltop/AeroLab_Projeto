#include <Arduino.h>
#include <algorithm>
#include <stdlib.h>

// Montagem do Henrique: TCRT5000 avulso e IRLZ44N.
const int PINO_SENSOR = 4;
const int PINO_MOSFET = 21;
const int FREQUENCIA_PWM = 1000; // Valor inicial; depende da ventoinha de 2 fios.
const int CONTRASTE_MINIMO = 150; // Escala ADC de 0 a 4095.

// Configure pelo Monitor Serial: pN, onde N e o numero real de
// ciclos pa/espaco detectados em uma volta completa.
unsigned int pulsosPorVolta = 0; // Zero impede exibir um RPM incorreto.
unsigned int pwmPercentual = 0;
unsigned long pulsosJanela = 0;
unsigned long totalPassagens = 0;
unsigned long ultimaMedicao = 0;
int limiteBaixo = 0;
int limiteAlto = 0;
bool calibrado = false;
bool estadoBaixo = false;
String comando;
bool comandoLongo = false;

void ajustarPWM(unsigned int percentual) {
  pwmPercentual = percentual;
  analogWrite(PINO_MOSFET, (percentual * 255UL + 50) / 100);
  Serial.printf("PWM: %u%%\n", pwmPercentual);
}

void zerarContagem() {
  totalPassagens = 0;
  pulsosJanela = 0;
  ultimaMedicao = millis();
  if (calibrado) {
    estadoBaixo = analogRead(PINO_SENSOR) <
                  (limiteBaixo + limiteAlto) / 2;
  }
}

void calibrarSensor() {
  ajustarPWM(0);
  calibrado = false;
  Serial.println("Motor desligado. Aguarde a ventoinha parar.");
  delay(2000);
  Serial.println("Gire manualmente varias voltas durante os proximos 8 s.");
  Serial.println("O sensor precisa ver tanto as pas quanto o fundo branco.");

  const int N = 320;
  uint16_t amostras[N];
  for (int i = 0; i < N; i++) {
    amostras[i] = analogRead(PINO_SENSOR);
    delay(25);
  }
  std::sort(amostras, amostras + N);
  // Percentis 10 e 90 reduzem a influencia de leituras isoladas.
  int baixo = amostras[N / 10];
  int alto = amostras[N * 9 / 10];
  int contraste = alto - baixo;
  Serial.printf("ADC baixo: %d | alto: %d | contraste: %d\n",
                baixo, alto, contraste);

  if (contraste < CONTRASTE_MINIMO) {
    Serial.println("Contraste insuficiente. Confira alinhamento e fundo branco.");
    Serial.println("Ajuste a montagem e envie c para repetir. Motor permanece desligado.");
    zerarContagem();
    return;
  }

  limiteBaixo = baixo + contraste * 35 / 100;
  limiteAlto = baixo + contraste * 65 / 100;
  calibrado = true;
  zerarContagem();
  Serial.printf("Calibrado! Limites: %d / %d\n", limiteBaixo, limiteAlto);
  Serial.println("Envie z, gire UMA volta manual e confira as passagens.");
  Serial.println("Configure pN e depois envie 100 para ligar o motor.");
}

bool lerNumero(const String &texto, long &valor) {
  const char *inicio = texto.c_str();
  char *fim;
  valor = strtol(inicio, &fim, 10);
  return fim != inicio && *fim == '\0';
}

void executarComando(String texto) {
  texto.trim();
  texto.toLowerCase();
  if (!texto.length()) return;
  if (texto == "c") {
    calibrarSensor();
    return;
  }
  if (texto == "z") {
    zerarContagem();
    Serial.println("Contagem zerada.");
    return;
  }

  long valor;
  if (texto.startsWith("p")) {
    String numero = texto.substring(1);
    numero.trim();
    if (lerNumero(numero, valor) && valor >= 1 && valor <= 100) {
      pulsosPorVolta = (unsigned int)valor;
      pulsosJanela = 0;
      ultimaMedicao = millis();
      Serial.printf("Pulsos por volta: %u\n", pulsosPorVolta);
    } else {
      Serial.println("Use pN, com N entre 1 e 100, conforme seu teste manual.");
    }
    return;
  }

  if (lerNumero(texto, valor) && valor >= 0 && valor <= 100) {
    if (valor > 0 && !calibrado) {
      Serial.println("Primeiro envie c para calibrar o sensor com o motor parado.");
    } else {
      ajustarPWM((unsigned int)valor);
    }
    return;
  }
  Serial.println("Comandos: c = calibrar | z = zerar | pN = pulsos/volta | 0..100 = PWM");
}

void lerSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (comandoLongo) {
        Serial.println("Comando muito longo; tente novamente.");
      } else {
        executarComando(comando);
      }
      comando = "";
      comandoLongo = false;
    } else if (comando.length() < 20 && !comandoLongo) {
      comando += c;
    } else {
      comandoLongo = true;
    }
  }
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(PINO_SENSOR, INPUT);
  pinMode(PINO_MOSFET, OUTPUT);
  digitalWrite(PINO_MOSFET, LOW);
  analogWriteResolution(PINO_MOSFET, 8);
  analogWriteFrequency(PINO_MOSFET, FREQUENCIA_PWM);
  analogWrite(PINO_MOSFET, 0);
  comando.reserve(24);
  delay(1000);
  ultimaMedicao = millis();
  Serial.println("TCRT5000: GPIO4 | IRLZ44N: GPIO21 | Serial: 115200");
  Serial.println("Selecione Nova linha no Monitor Serial.");
  Serial.println("Motor inicia DESLIGADO. Envie c para calibrar.");
}

void loop() {
  lerSerial();
  int leitura = analogRead(PINO_SENSOR);

  if (calibrado) {
    // Uma borda por ciclo: funciona com pa clara OU fundo branco mais claro.
    // A montagem precisa produzir um unico ciclo por pa/espaco.
    if (!estadoBaixo && leitura < limiteBaixo) {
      estadoBaixo = true;
      pulsosJanela++;
      totalPassagens++;
    } else if (estadoBaixo && leitura > limiteAlto) {
      estadoBaixo = false;
    }
  }

  unsigned long agora = millis();
  unsigned long intervalo = agora - ultimaMedicao;
  if (intervalo >= 1000) {
    Serial.printf("PWM: %u%% | ADC: %d | Passagens: %lu",
                  pwmPercentual, leitura, totalPassagens);
    if (!calibrado) {
      Serial.println(" | Sensor nao calibrado: envie c");
    } else if (pulsosPorVolta == 0) {
      Serial.println(" | RPM: configure pN");
    } else {
      float rpm = pulsosJanela * 60000.0 /
                  (intervalo * (float)pulsosPorVolta);
      Serial.printf(" | RPM: %.0f\n", rpm);
    }
    pulsosJanela = 0;
    ultimaMedicao = agora;
  }
}
