#include <AFMotor.h>
#include <Servo.h>
//장애물 인식 x 1
//장애물 인식 했을 떄 0
//검은색이 1
//흰색 0
//defining pins and variables
#define left A0
#define right A5
const int spd = 220;
int L;
int R;
int i;
int input_data=0;
Servo myservo;

//defining motors
AF_DCMotor motor1(1, MOTOR12_1KHZ); 
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_1KHZ);
AF_DCMotor motor4(4, MOTOR34_1KHZ);
void runforward(){
      motor1.run(FORWARD);
      motor1.setSpeed(150);
      motor2.run(FORWARD);
      motor2.setSpeed(150);
      motor3.run(FORWARD);
      motor3.setSpeed(150);
      motor4.run(FORWARD);
      motor4.setSpeed(150);
      }

void turn_left(){
      motor1.run(BACKWARD);
      motor1.setSpeed(spd);
      motor2.run(BACKWARD);
      motor2.setSpeed(spd);
      motor3.run(FORWARD);
      motor3.setSpeed(spd);
      motor4.run(FORWARD);
      motor4.setSpeed(spd);
      }
void turn_right(){
      motor1.run(FORWARD);
      motor1.setSpeed(spd);
      motor2.run(FORWARD);
      motor2.setSpeed(spd);
      motor3.run(BACKWARD);
      motor3.setSpeed(spd);
      motor4.run(BACKWARD);
      motor4.setSpeed(spd);
      }
void Stop(){
      motor1.run(RELEASE);
      motor1.setSpeed(0);
      motor2.run(RELEASE);
      motor2.setSpeed(0);
      motor3.run(RELEASE);
      motor3.setSpeed(0);
      motor4.run(RELEASE);
      motor4.setSpeed(0);
      }
void line_trace(int l,int r){
      int iter = 0;
      if(l==1 && r==1){
          runforward();
      }
      else if(l==1 && !r==1){
        do{
          turn_right();
          delay(100);
          iter++; 
        }while(iter<5);
      }
      else if(!l==1 && r==1){
        do{
          turn_left();
          delay(100);
          iter++; 
        }while(iter<5);
      }
      else if(!l==1 && !r==1){
          Stop();
      }
}

void setup() {
  pinMode(left,INPUT);
  pinMode(right,INPUT);
  myservo.write(0);
  myservo.attach(9);
  Serial.begin(9600);
  Serial.setTimeout(300);
}

void loop(){
    if(Serial.available()>0){
      String str_data = Serial.readString();
      Serial.println(str_data);
      input_data=str_data.toInt();
      if(input_data == 1){        
        myservo.write(0);
      }
      else if(input_data > 1){
        Stop();
        myservo.write(input_data);
      }
      else{
        Stop();  
      }
    }else{
      if(input_data == 1){  
        L = digitalRead(left);  
        R = digitalRead(right);      
        line_trace(L,R);
      }
      
      delay(50);
    }
}
