const byte PinForce = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int force = analogRead(PinForce); 
  Serial.println(force);             // send to PC as text line
  delay(300);                        // ~3 readings per second
}
