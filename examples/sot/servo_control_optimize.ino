#include <Servo.h>


Servo servo_base;  // create servo object to control a servo
Servo servo_up; 


int servo_base_min=0;
int servo_base_max=180;

int servo_up_min=30;
int servo_up_max=150;

int servo_base_default=90;
int servo_up_default=120;
int servo_base_now=servo_base_default;
int servo_up_now=servo_up_default;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  servo_base.attach(11);  // attaches the servo on pin 9 to the servo object
  servo_up.attach(6);
  servo_up.write(servo_up_default);
  servo_base.write(90);
}

void dealCommand(char command){
    Serial.println(command);
    switch(command){
      
      case '0':
        servo_base_now=servo_base_default;
        servo_up_now=servo_up_default;
        break;
      case '1':
        servo_base_now+=1;
        servo_up_now+=1;
        break;
      case '2':
        servo_base_now+=1;
        break;
      case '3':
        servo_base_now+=1;
        servo_up_now-=1;
        break;
      case '4':
        servo_up_now+=1;
        break;
      case '6':
        servo_up_now-=1;
        break;
      case '7':
        servo_base_now-=1;
        servo_up_now+=1;
        break;
      case '8':
        servo_base_now-=1;
        break;
      case '9':
        servo_base_now-=1;
        servo_up_now-=1;
        break;
    }
     if(servo_base_now<=servo_base_min){
          servo_base_now=servo_base_min;
     }
     if(servo_base_now>=servo_base_max){
          servo_base_now=servo_base_max;
     }
     
     if(servo_up_now<=servo_up_min){
          servo_up_now=servo_base_min;
     }
     if(servo_up_now>=servo_up_max){
          servo_up_now=servo_base_max;
     }
     servo_base.write(servo_base_now);
     servo_up.write(servo_up_now);
     Serial.println(servo_base_now);
     Serial.println(servo_up_now);
     delay(5);
}

char command;
void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0){
      command=Serial.read();
      if(command != '\n'){
           dealCommand(command);
      }
  }

}
