#include "global.h"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  pinMode(LED_BLINK, OUTPUT);

  init_servo();
  set_timer_led_blink(10);

  init_lcd();
  set_time_lcd(10);
}


uint8_t state_led_blink = 0;
void blink_led(){
  if(get_timer_led_blink() == 1){
    set_timer_led_blink(100);
    //TODO
    switch(state_led_blink){
      case 0:
        Serial.println("ON");
        digitalWrite(LED_BLINK, HIGH);
        state_led_blink = 1;
      break;
      case 1:
        Serial.println("OFF");
        digitalWrite(LED_BLINK, LOW);
        state_led_blink = 0;
      break;
      default: break;
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

  timer_run();
  blink_led();


  recv_uart();
  uart_handle_servo_1();
  uart_handle_servo_2();
  uart_handle_servo_3();
  
  
  display();

  delay(10);
}
