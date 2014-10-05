
#ifndef SERIAL_RATE
#define SERIAL_RATE         115200
#endif

#ifndef SERIAL_TIMEOUT
#define SERIAL_TIMEOUT      5
#endif


#include <Servo.h>

Servo servo0;
Servo servo1;
Servo servo2;

void setup() {

    Serial.begin(SERIAL_RATE);
    Serial.setTimeout(SERIAL_TIMEOUT);

    servo0.attach(9);
    servo1.attach(10);
    servo2.attach(11);

    int cmd = readData();
    for (int i = 0; i < cmd; i++) {
        pinMode(readData(), OUTPUT);
    }
}

void loop() {
    switch (readData()) {
        case 0 :
            Serial.println("Got into 0 case!");
            //set digital low
            digitalWrite(readData(), LOW); break;
        case 1 :
            Serial.println("Got into 1 case!");
            //set digital high
            digitalWrite(readData(), HIGH); break;
        case 2 :
            Serial.println("Got into 2 case!");
            //get digital value
            Serial.println(digitalRead(readData())); break;
        case 3 :
            Serial.println("Got into 3 case!");
            // set analog value
            analogWrite(readData(), readData()); break;
        case 4 :
            Serial.println("Got into 4 case!");
            //read analog value
            Serial.println(analogRead(readData())); break;
        case 5 :
            Serial.println("Got into servo case!");
            //read analog value
            switch(readData()){
                case 0:
                    Serial.println("Got into 5:0 case!");
                    servo0.write(readData());
                    Serial.println("Wrote a thing\n");
                    break;
                case 1:
                    servo1.write(readData());
                    break;
                case 2:
                    servo2.write(readData());
                    break;
            }
        case 99:
            //just dummy to cancel the current read, needed to prevent lock 
            //when the PC side dropped the "w" that we sent
            break;
    }
}

char readData() {
    Serial.println("w");
    while(1) {
        if(Serial.available() > 0) {
            return Serial.parseInt();
        }
    }
}