
#include <Servo.h>
#include <SoftwareSerial.h>

// ===============================
// COMUNICACAO COM ESP32-CAM
// ===============================

// RX = D10 recebe da ESP32-CAM
// TX = D11 (nao utilizado neste projeto)
SoftwareSerial espSerial(10, 11);

// ===============================
// SERVOS
// ===============================

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

// ===============================
// PINOS DOS SERVOS
// ===============================

const int PINO_SERVO1 = 13;
const int PINO_SERVO2 = 6;
const int PINO_SERVO3 = 3;
const int PINO_SERVO4 = 9;

// ===============================
// POSICOES INICIAIS
// ===============================

int posicaoInicialServo1 = 21; // direita
int posicaoInicialServo2 = 24; // cima arduino
int posicaoInicialServo3 = 31; // esquerda
int posicaoInicialServo4 = 23; // baixo HC

// ===============================
// TEMPO DE MOVIMENTO
// ===============================

const unsigned long TEMPO_MOVIMENTO = 5000;

// ===============================
// EXECUTA MOVIMENTO 1
// Papel
// ===============================

void movimento1() {

  Serial.println("Movimento 1 - PAPEL");

  servo1.write(180);
  servo3.write(0);

  delay(TEMPO_MOVIMENTO);

  servo1.write(posicaoInicialServo1);
  servo3.write(posicaoInicialServo3);

  Serial.println("Servos voltaram a posicao inicial.");
}

// ===============================
// EXECUTA MOVIMENTO 2
// Plastico
// ===============================

void movimento2() {

  Serial.println("Movimento 2 - PLASTICO");

  servo2.write(150);
  servo4.write(0);

  delay(TEMPO_MOVIMENTO);

  servo2.write(posicaoInicialServo2);
  servo4.write(posicaoInicialServo4);

  Serial.println("Servos voltaram a posicao inicial.");
}

// ===============================
// EXECUTA MOVIMENTO 3
// Metal
// ===============================

void movimento3() {

  Serial.println("Movimento 3 - METAL");

  servo3.write(180);
  servo1.write(0);

  delay(TEMPO_MOVIMENTO);

  servo3.write(posicaoInicialServo3);
  servo1.write(posicaoInicialServo1);

  Serial.println("Servos voltaram a posicao inicial.");
}

// ===============================
// EXECUTA MOVIMENTO 4
// Nao reciclavel / nao identificado
// ===============================

void movimento4() {

  Serial.println("Movimento 4 - NAO RECICLAVEL");

  servo4.write(180);
  servo2.write(0);

  delay(TEMPO_MOVIMENTO);

  servo4.write(posicaoInicialServo4);
  servo2.write(posicaoInicialServo2);

  Serial.println("Servos voltaram a posicao inicial.");
}

// ===============================
// PROCESSA NUMERO RECEBIDO
// ===============================

void processarComando(char comando) {

  switch (comando) {

    case '1':
      movimento1();
      break;

    case '2':
      movimento2();
      break;

    case '3':
      movimento3();
      break;

    case '4':
      movimento4();
      break;

    default:
      Serial.print("Comando desconhecido: ");
      Serial.println(comando);
      break;
  }
}

// ===============================
// SETUP
// ===============================

void setup() {

  // Monitor Serial USB
  Serial.begin(9600);

  // Comunicacao com a ESP32-CAM
  espSerial.begin(9600);
  espSerial.setTimeout(100);

  // Conecta servos
  servo1.attach(PINO_SERVO1);
  servo2.attach(PINO_SERVO2);
  servo3.attach(PINO_SERVO3);
  servo4.attach(PINO_SERVO4);

  // Posicoes iniciais
  servo1.write(posicaoInicialServo1);
  servo2.write(posicaoInicialServo2);
  servo3.write(posicaoInicialServo3);
  servo4.write(posicaoInicialServo4);

  Serial.println("Sistema iniciado!");
  Serial.println("Aguardando comandos da ESP32-CAM...");
}

// ===============================
// LOOP
// ===============================

void loop() {

  // Verifica dados recebidos da ESP32-CAM
  while (espSerial.available() > 0) {

    char comando = espSerial.read();

    // Ignora quebras de linha enviadas por println()
    if (comando == '\n' || comando == '\r') {
      continue;
    }

    Serial.print("Recebido da ESP32-CAM: ");
    Serial.println(comando);

    processarComando(comando);
  }
}
