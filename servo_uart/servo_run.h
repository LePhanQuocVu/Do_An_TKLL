#ifndef SERVO_RUN_H_
#define SERVO_RUN_H_

#include "global.h"


#define SERVO_1 2
#define SERVO_2 3
#define SERVO_3 4

Servo dong_co_1;
Servo dong_co_2;
Servo dong_co_3;

void init_servo(){
  dong_co_1.attach(SERVO_1);
  dong_co_2.attach(SERVO_2);
  dong_co_3.attach(SERVO_3);

  dong_co_1.write(30);
  dong_co_2.write(30);
  dong_co_3.write(30);
}

#endif