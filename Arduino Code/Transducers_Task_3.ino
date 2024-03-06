int flexs = A0;
int data = 0;
int FSR5;
int Buzzer=8;



void setup() {
  Serial.begin(9600);
  pinMode(flexs,INPUT);
  pinMode(Buzzer,OUTPUT);
}

void loop() {
  FSR5= analogRead(A5);
  FSR5 = map(FSR5,0,1023,0,800);
  data = analogRead(flexs);
  data = map(data,0,400,0,100);
  // Serial.print("Flex Value = ");

  if (data>49)
  {
    digitalWrite(Buzzer,HIGH);
  }
    else{
    digitalWrite(Buzzer,LOW);
    }
  Serial.print(data);
  Serial.print('/');
  // Serial.print("FSR Value = ");
  Serial.println(FSR5);
  delay(100);
}
