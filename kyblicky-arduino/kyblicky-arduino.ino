#define NUM_BUTTONS 4
#define DEBOUNCE 90

const int buttonPins[NUM_BUTTONS] = {4, 5, 6, 7};


unsigned long buttonTimes[NUM_BUTTONS] = {0};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {
  // Read the state of each button
  for (int i = 0; i < NUM_BUTTONS; i++) {
    int state = digitalRead(buttonPins[i]);
    if (state == LOW) {
      if (buttonTimes[i] == 0) {
        //Serial.print("================================");
        Serial.println(i);
        buttonTimes[i] = millis();
      }
    } else {
      if (buttonTimes[i] != 0 && buttonTimes[i] + DEBOUNCE < millis()) {
        buttonTimes[i] = 0;
        //Serial.print("clear ");
        //Serial.println(i);
      }
    }


  }

  /*
    for (int i = 0; i < NUM_BUTTONS; i++) {
      Serial.print(i);
      Serial.print(" ");
      Serial.print(buttonTimes[i]);
      Serial.print("\t");

    }
    Serial.println();
  */
}
