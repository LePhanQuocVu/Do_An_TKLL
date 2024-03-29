#ifndef LCD_H_
#define LCD_H_

#include "global.h"
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 20, 4);

uint16_t tron, vuong, tam_giac;
uint8_t arr[3];

void init_lcd(){
  tron = 0;
  vuong = 0;
  tam_giac = 0;

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Tron     : ");
  lcd.setCursor(0,1);
  lcd.print("Vuong    : ");
  lcd.setCursor(0,2);
  lcd.print("Tam giac : ");

  for(int i = 0; i < 3 ; i ++){
    arr[i] = 0; 
  }
}

void update(uint16_t object){
  for(int i = 2 ; i >= 0; i--){
    arr[i] = object % 10;
    object = object / 10;  
  }
}

void display(){
  if(get_timer_lcd()){
    set_time_lcd(10);
    //TODO
    update(tron);
    lcd.setCursor(12, 0);
    lcd.print(arr[0]);
    lcd.setCursor(13, 0);
    lcd.print(arr[1]);
    lcd.setCursor(14, 0);
    lcd.print(arr[2]);

    update(vuong);
    lcd.setCursor(12, 1);
    lcd.print(arr[0]);
    lcd.setCursor(13, 1);
    lcd.print(arr[1]);
    lcd.setCursor(14, 1);
    lcd.print(arr[2]);

    update(tam_giac);
    lcd.setCursor(12, 2);
    lcd.print(arr[0]);
    lcd.setCursor(13, 2);
    lcd.print(arr[1]);
    lcd.setCursor(14, 2);
    lcd.print(arr[2]);
  }
}




#endif