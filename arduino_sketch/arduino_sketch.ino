#define R_DIODE 6
#define Y_DIODE 5
#define G_DIODE 3

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(R_DIODE, OUTPUT);
  pinMode(Y_DIODE, OUTPUT);
  pinMode(G_DIODE, OUTPUT);
  setDiodes(LOW, LOW, LOW);
}

void serialEvent(){
  setDiodes(LOW, LOW, LOW); //reset state
  while (Serial.available()){
    char c = (char)Serial.read();
    switch(c){
      case 'r':
      case 'R':
        setDiodes(HIGH, LOW, LOW);
        break;
      case 'y':
      case 'Y':
        setDiodes(LOW, HIGH, LOW);
        break;
      case 'g':
      case 'G':
        setDiodes(LOW, LOW, HIGH);
        break;
    }
    Serial.write(c);
  }
}

void loop() {

}

void setDiodes(int r, int y, int g) {
  digitalWrite(R_DIODE, r);
  digitalWrite(Y_DIODE, y);
  digitalWrite(G_DIODE, g);
}

void pwmDiodes(int r, int y, int g) {
  analogWrite(R_DIODE, r);
  analogWrite(Y_DIODE, y);
  analogWrite(G_DIODE, g);
}


