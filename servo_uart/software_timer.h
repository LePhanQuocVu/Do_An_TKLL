#ifndef SOFTWARE_TIMER_H_
#define SOFTWARE_TIMER_H_

#include "global.h"

int timer_servo_1_count;
uint8_t timer_servo_1_flag;
void set_timer_servo_1(int duration){
  timer_servo_1_flag = 0;
  timer_servo_1_count = duration;
}
uint8_t get_timer_servo_1(){
  return timer_servo_1_flag;
}

int timer_servo_2_count;
uint8_t timer_servo_2_flag;
void set_timer_servo_2(int duration){
  timer_servo_2_flag = 0;
  timer_servo_2_count = duration;
}
uint8_t get_timer_servo_2(){
  return timer_servo_2_flag;
}

int timer_servo_3_count;
uint8_t timer_servo_3_flag;
void set_timer_servo_3(int duration){
  timer_servo_3_flag = 0;
  timer_servo_3_count = duration;
}
uint8_t get_timer_servo_3(){
  return timer_servo_3_flag;
}

int timer_led_blink_count;
uint8_t timer_led_blink_flag;
void set_timer_led_blink(int duration){
  timer_led_blink_count = duration;
  timer_led_blink_flag = 0;
}
uint8_t get_timer_led_blink(){
  return timer_led_blink_flag;
}

int timer_lcd_count;
uint8_t timer_lcd_flag;
void set_time_lcd(int duration){
  timer_lcd_count = duration;
  timer_lcd_flag = 0;
}
uint8_t get_timer_lcd(){
  return timer_lcd_flag;
}

void timer_run(){
  timer_servo_1_count --;
  if(timer_servo_1_count <= 0){
    timer_servo_1_flag = 1;
  }

  timer_servo_2_count --;
  if(timer_servo_2_count <= 0){
    timer_servo_2_flag = 1;
  }

  timer_servo_3_count --;
  if(timer_servo_3_count <= 0){
    timer_servo_3_flag = 1;
  }

  timer_led_blink_count --;
  if(timer_led_blink_count <= 0){
    timer_led_blink_flag = 1;
  }

  timer_lcd_count --;
  if(timer_lcd_count <= 0){
    timer_lcd_flag = 1;
  }
}


#endif