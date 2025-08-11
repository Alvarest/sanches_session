const int muxPins[4] = {2,3,4,5};
const int shiftPin = 6;
const int analogPins[3] = {A0, A1, A2};
int i, selector, bit; // Variables para los bucles 
int shiftValue, analogValue;

void setup() {
  for (i = 0; i < 4; i = i+1){
    pinMode(muxPins[i], OUTPUT);
  }
  pinMode(shiftPin, INPUT);
  Serial.begin(115200);
}

void loop() {
  for (selector = 0; selector < 16; selector = selector+1){
    for (bit = 0; bit < 4; bit = bit+1){
      digitalWrite(muxPins[bit], (selector >> bit) & 1);
      // Mueve los bits de selector un numero de veces igual a bit y luego hace un 
      // AND bit a bit con 1, con lo que seleccionamos el valor del ultimo
      // bit del número. Espero que funcione bien me lo he copiado de internet.
    }
    
    shiftValue = digitalRead(shiftPin);

    for (i = 0; i < 3; i = i+1){ // Para cada entrada analogica
      analogValue = analogRead(analogPins[i]);
      int32_t data[4];
      data[0] = shiftValue;
      data[1] = selector;
      data[3] = i;
      data[4] = analogValue;

      Serial.write((uint8_t*)data, sizeof(data));
    }

    delayMicroseconds(100); // He leido que lo mejor es darle un tiempo a los multiplexores 
                            // asi que he puesto este delay. Espero que sea suficiente.
  }
}
