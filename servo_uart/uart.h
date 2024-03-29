#ifndef UART_H_
#define UART_H_

#include "global.h"
#include "servo_run.h"
#include "lcd.h"

uint8_t servo_state[3] = {0, 0, 0};


void uart_handle_servo_1(){
  switch(servo_state[0]){
    case 1:// Day vat
      dong_co_1.write(45);
      //set timer for waiting servo run
      set_timer_servo_1(30);
      servo_state[0] = 0;
      break;
    case 0:
      //return servo
      if(get_timer_servo_1() == 1){
        dong_co_1.write(0);
      }
      break;
    default: break;
  }
}

void uart_handle_servo_2(){
  switch(servo_state[1]){
    case 1:// Day vat
      dong_co_2.write(45);
      //set timer for waiting servo run
      set_timer_servo_2(30);
      servo_state[1] = 0;
      break;
    case 0:
      //return servo
      if(get_timer_servo_2() == 1){
        dong_co_2.write(0);
      }
      break;
    default: break;
  }
}

void uart_handle_servo_3(){
  switch(servo_state[2]){
    case 1:// Day vat
      dong_co_3.write(45);
      //set timer for waiting servo run
      set_timer_servo_3(30);
      servo_state[2] = 0;
      break;
    case 0:
      //return servo
      if(get_timer_servo_3() == 1){
        dong_co_3.write(0);
      }
      break;
    default: break;
  }
}


void recv_uart(){
  if(Serial.available()){
    String du_lieu = "";
    du_lieu = Serial.readStringUntil('\r');
    if(du_lieu == "1"){
      servo_state[0] = 1;
      //increase value of tron by one
      tron ++;
    }else if(du_lieu == "2"){
      servo_state[1] = 1;
      //increase value of vuong by one
      vuong ++;
    }else if(du_lieu == "3"){
      servo_state[2] = 1;
      //increase value of tam giac by one
      tam_giac ++;
    }
  }
}


#endif