
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
    
    int dc0 = 3;
    int dc1 = 5;
    int dc2 = 6;

    servo0.attach(9);
    servo1.attach(10);
    servo2.attach(11);

    int cmd = readData();
    for (int i = 0; i < cmd; i++) {
        pinMode(readData(), OUTPUT);
    }

    pinMode(dc0, OUTPUT);
    pinMode(dc1, OUTPUT);
    pinMode(dc2, OUTPUT);
}

void loop() {
    switch (readData()) {
        case 0 :
            //set digital low
            digitalWrite(readData(), LOW); break;
        case 1 :
            //set digital high
            digitalWrite(readData(), HIGH); break;
        case 2 :
            //get digital value
            Serial.println(digitalRead(readData())); break;
        case 3 :
            // set analog value
            analogWrite(readData(), readData()); break;
        case 4 :
            //read analog value
            Serial.println(analogRead(readData())); break;
        case 5 :
            //read analog value
            switch(readData()){
                case 0:
                    servo0.write(readData());
                case 1:
                    servo1.write(readData());
                case 2:
                    servo2.write(readData());
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