#include <SPI.h>
#include <MFRC522.h>
#include <SD.h>
#include <ThreeWire.h>
#include <RtcDS1302.h>
#include <Ethernet.h>
#include <MQTT.h>
#include <virtuabotixRTC.h>
virtuabotixRTC myRTC(5, 7, 2);

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
byte ip[] = {192, 168, 0, 200};  // <- mudar para um IP na faixa da rede em que o ponto de acesso será configurado

#define SS_PIN 9
#define RST_PIN 8

//CLIENTES ETHERNET E MQTT
EthernetClient net;
MQTTClient client;

//LEITOR RFID
MFRC522 mfrc522(SS_PIN, RST_PIN); // criar a instancia MFRC522.

//RTC            D  C  R
ThreeWire myWire(7, 5, 2); //OBJETO DO TIPO ThreeWire
RtcDS1302<ThreeWire> Rtc(myWire); //OBJETO DO TIPO RtcDS1302

bool recebendo_csv = false;

void setup() {
  //USE ESTA FUNÇÃO QUANDO QUISER SETAR A HORA. COMENTE-A E SUBA O CÓDIGO NOVAMENTE, QUANDO TIVER SETADO.
  //myRTC.setDS1302Time(00, 54, 17, 6, 04, 03, 2022);
  
  Serial.begin(9600);
  SPI.begin(); // Inicia  SPI bus
  mfrc522.PCD_Init();  // Inicia MFRC522
  Rtc.Begin(); //INICIALIZA O RTC

  Serial.print("Compilado em: "); //IMPRIME O TEXTO NO MONITOR SERIAL
  RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__); //VARIÁVEL RECEBE DATA E HORA DE COMPILAÇÃO
  printDateTime(compiled); //PASSA OS PARÂMETROS PARA A FUNÇÃO printDateTime
  Serial.println(); //QUEBRA DE LINHA NA SERIAL
  Serial.println(); //QUEBRA DE LINHA NA SERIAL0

  if(Rtc.GetIsWriteProtected()){ //SE O RTC ESTIVER PROTEGIDO CONTRA GRAVAÇÃO, FAZ
    Serial.println("RTC está protegido contra gravação. Habilitando a gravação agora..."); //IMPRIME O TEXTO NO MONITOR SERIAL
    Rtc.SetIsWriteProtected(false); //HABILITA GRAVAÇÃO NO RTC
    Serial.println(); //QUEBRA DE LINHA NA SERIAL
  }

  if(!Rtc.GetIsRunning()){ //SE RTC NÃO ESTIVER SENDO EXECUTADO, FAZ
    Serial.println("RTC não está funcionando de forma contínua. Iniciando agora..."); //IMPRIME O TEXTO NO MONITOR SERIAL
    Rtc.SetIsRunning(true); //INICIALIZA O RTC
    Serial.println(); //QUEBRA DE LINHA NA SERIAL
  }

  RtcDateTime data = Rtc.GetDateTime(); //VARIÁVEL RECEBE INFORMAÇÕES
  
  Ethernet.begin(mac, ip); //INICIALIZANDO ETHERNET

  client.begin("mqtt.eclipseprojects.io", net);
  client.onMessage(messageReceived);

  // Inicializando cartão SD
  Serial.print("Inicializando cartão SD...");
  if (!SD.begin(4)) {
    Serial.println("A inicialização do cartão SD falhou!");
    while (1);
  }

  Serial.println("Cartão SD inicializado com sucesso.");
    
  Serial.println("Aproxime o seu cartão do leitor...");
  Serial.println();
  pinMode(6, OUTPUT); // Led verde
  pinMode(3, OUTPUT); // Led vermelho
}

void loop () {
  RtcDateTime data = Rtc.GetDateTime();
  printDateTime(data);

  bool temEtiqueta = false;
  bool etiquetaSelecionada = false;
  
  // Procura por novas etiquetas RFID e mantém os LEDs apagados, enquanto não os encontra
  if (!mfrc522.PICC_IsNewCardPresent()) {
    digitalWrite(6, LOW);
    digitalWrite(3, LOW);
    temEtiqueta = false;
  } else {
    temEtiqueta = true;
  }
  
  // Seleciona uma das etiquetas RFID
  if (!mfrc522.PICC_ReadCardSerial()) {
    etiquetaSelecionada = false;
  } else {
    etiquetaSelecionada = true;
  }

  client.loop();
  delay(10);
  
  // check if connected
  if (!client.connected()) {
    connect();
  }

  // Mostra UID da etiqueta RFID na serial
  String tag_lida = "";
  if (etiquetaSelecionada) {
    Serial.print("UID da etiqueta RFID:");
    byte letra;
    for (byte i = 0; i < mfrc522.uid.size; i++) {
       tag_lida.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
       tag_lida.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    tag_lida.toUpperCase();
    Serial.println(tag_lida);
  }

  if (tag_lida != "") {
    Serial.println(tag_lida);
    bool result = autenticaPorCsv(tag_lida, data);
    Serial.println(result);
    if (result) {
      digitalWrite(6, HIGH);
      delay(2000);
      digitalWrite(6, LOW);
    } else {
      for (int x = 0; x < 3; x++) {
        digitalWrite(3, HIGH);
        delay(300);
        digitalWrite(3, LOW);
        delay(300);
      }
    }
  }
}

bool autenticaPorCsv(String tag_lida, RtcDateTime data) {
  File CSV = SD.open("CADASTRO.CSV", FILE_READ);
  
  String dia = "";
  
  String hora_entrada = "";
  
  String hora_saida = "";
  
  String matricula = "";
  String ambiente = "";
  String tag_cadastrada = "";
    
  if (CSV) {
    int delimitador = 0;
    char caractere;
    // LÊ TODO O ARQUIVO, ATÉ QUE NÃO HAJA MAIS NADA NELE:
    while (CSV.available()) {
      caractere = CSV.read();
      if (caractere == ',' || caractere == ':') {
        delimitador++;
      } else if (caractere == ';') {
        if (autentica(data, dia, hora_entrada, hora_saida, matricula, ambiente, tag_lida, tag_cadastrada)) {
          CSV.close();
          return true;
        }
        
        delimitador = 0;

        dia = "";
        hora_entrada = "";
        hora_saida = "";
        
        matricula = "";
        ambiente = "";
        tag_cadastrada = "";

        // PARA PULAR A QUEBRA DE LINHA APÓS O ";"
        CSV.read();
        CSV.read();
        
      } else if (caractere != ';' && caractere != ',' && caractere != ':') {
        switch(delimitador) {
          case 0:
            dia += caractere;          
            break;
          case 1:
            hora_entrada += caractere;
            break;
          case 2:
            hora_entrada += caractere;
            break;
          case 3:
            hora_entrada += caractere;
            break;
          case 4:
            hora_saida += caractere;
            break;
          case 5:
            hora_saida += caractere;
            break;
          case 6:
            hora_saida += caractere;
            break; 
          case 7:
            matricula += caractere;
            break;
          case 8:
            ambiente += caractere;
            break;
          case 9:
            tag_cadastrada += caractere;
            break;
        }
      } else {
        
        dia = "";
        hora_entrada = "";
        hora_saida = "";
        
        matricula = "";
        ambiente = "";
        tag_cadastrada = "";
      }

    }
    // FECHA O ARQUIVO:
    CSV.close();
  } else {
    // EXIBE ESTE ERRO SE O ARQUIVO NÃO FOR ABERTO:
    Serial.println("Erro ao abrir o arquivo.");
  }

  return false;
}

bool autentica(RtcDateTime data, String dia, String hora_entrada, String hora_saida, String matricula, String ambiente, String tag_lida, String tag_cadastrada) {
  if (dia_atual(data) == dia && tag_lida == tag_cadastrada) {

    int hora = data.Hour();
    int minuto = data.Minute();
    int segundo = data.Second();
    
    String hora_atual = data.Hour() < 10 ? "0" + (String)data.Hour() : (String)data.Hour();
    String minuto_atual = data.Minute() < 10 ? "0" + (String)data.Minute() : (String)data.Minute();
    String segundo_atual = data.Second() < 10 ? "0" + (String)data.Second() : (String)data.Second();
    
    String horario_atual = hora_atual + minuto_atual + segundo_atual;

    if (horario_atual.toInt() >= hora_entrada.toInt() && horario_atual.toInt() <= hora_saida.toInt()) {
      return true;
    } else {
      return false;
    }

    hora_atual = "";
    minuto_atual = "";
    segundo_atual = "";

    horario_atual = "";
    
  } else {
    return false;
  }
}


#define countof(a) (sizeof(a) / sizeof(a[0]))

void printDateTime(const RtcDateTime& dt){
  char datestring[20]; //VARIÁVEL ARMAZENA AS INFORMAÇÕES DE DATA E HORA

  snprintf_P(datestring, 
          countof(datestring),
          PSTR("%02u/%02u/%04u %02u:%02u:%02u"), //FORMATO DE EXIBIÇÃO DAS INFORMAÇÕES
          dt.Day(), //DIA
          dt.Month(), //MÊS
          dt.Year(), //ANO
          dt.Hour(), //HORA
          dt.Minute(), //MINUTOS
          dt.Second() ); //SEGUNDOS
  Serial.println(datestring); //IMPRIME NO MONITOR SERIAL AS INFORMAÇÕES
}


String dia_atual(RtcDateTime data) {
  // FÓRMULA MATEMÁTICA PARA ENCONTRAR O DIA DA SEMANA A PARTIR DA DATA. DIVIDA K POR 7, E O RESTO DESSA DIVISÃO TE DIRÁ QUAL É O DIA:
  // 0 = SÁBADO; 1 = DOMINGO; 2 = SEGUNDA, ...

  int dia = data.Day();
  int mes;
  int ano;
  
  if (data.Month() == 1 || data.Month() == 2) {
    mes = data.Month() + 12;
    ano = data.Year() - 1;
  } else {
    mes = data.Month();
    ano = data.Year();
  }
  
  int k = dia + (2 * mes) + ((3 * (mes + 1))/5) + ano + (ano/4) - (ano/100) + (ano/400) + 2;
  int num_dia = k % 7;
  Serial.print("Num_dia: ");
  Serial.println(num_dia);
  
  switch(num_dia) {
    case 0:
      return "Sábado";
      break;
    case 1:
      return "Domingo";
      break;
    case 2:
      return "Segunda-feira";
      break;
    case 3:
      return "Terça-feira";
      break;
    case 4:
      return "Quarta-feira";
      break;
    case 5:
      return "Quinta-feira";
      break;
    case 6:
      return "Sexta-feira";
      break;
  }
}

void connect() {
  if (!client.connect("arduino-ifaccess", "public", "public")) {
    Serial.println("connecting...");
    delay(100);
  }

  Serial.println("\nconnected!");

  client.subscribe("IFAccess");
}

void messageReceived(String &topic, String &payload) {
  if (payload == "BEGIN") {
    recebendo_csv = true;
    if (SD.exists("CADASTRO.CSV")) {
      SD.remove("CADASTRO.CSV");
    }
    return;
  } else if (payload == "END") {
    recebendo_csv = false;
    return;
  }
  
  if(recebendo_csv) {
    File arquivo_csv = SD.open("CADASTRO.CSV", FILE_WRITE);
    if (arquivo_csv) {
      arquivo_csv.println(payload);
      arquivo_csv.close();
    }
  }
}
